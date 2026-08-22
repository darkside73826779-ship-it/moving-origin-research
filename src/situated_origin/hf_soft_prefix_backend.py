"""Single-model activation-level memory backend for the moving-origin alpha.

The base language model is immutable.  Only small origin-indexed soft-prefix
tensors are optimized.  Recalled event text is never appended to the model
prompt: selected prefixes enter through ``inputs_embeds``.

Torch, Transformers, and safetensors are imported lazily so the model-neutral
runtime and its custody-free test suite remain dependency-free.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any


class SoftPrefixBackendError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class PrefixTrainingResult:
    prefix: Any
    initial_loss: float
    final_loss: float
    gradient_norm: float
    steps: int
    tensor_sha256: str


@dataclass(frozen=True)
class PrefixGenerationResult:
    text: str
    token_ids: tuple[int, ...]
    public_prompt_token_ids_sha256: str
    prefix_tensor_sha256: str
    activation_delta_norm: float


class SoftPrefixTensorCodec:
    """Canonical safetensors byte codec for one fixed-shape prefix tensor."""

    def __init__(self, *, prefix_tokens: int, hidden_size: int, model_identity: str) -> None:
        if prefix_tokens < 1 or hidden_size < 1 or not model_identity:
            raise SoftPrefixBackendError("PREFIX_CODEC_CONFIG_INVALID")
        self.prefix_tokens = int(prefix_tokens)
        self.hidden_size = int(hidden_size)
        self.model_identity = model_identity
        self.identity_sha256 = _sha(
            _canonical(
                {
                    "schema_version": "soft-prefix-tensor-codec-v1",
                    "prefix_tokens": self.prefix_tokens,
                    "hidden_size": self.hidden_size,
                    "model_identity": self.model_identity,
                    "tensor_key": "soft_prefix",
                }
            )
        )

    def to_bytes(self, value: object) -> bytes:
        try:
            from safetensors.torch import save
        except ImportError as exc:
            raise SoftPrefixBackendError("SAFETENSORS_UNAVAILABLE") from exc
        shape = getattr(value, "shape", None)
        if shape != (1, self.prefix_tokens, self.hidden_size):
            raise SoftPrefixBackendError("PREFIX_SHAPE_INVALID")
        tensor = value.detach().to(device="cpu").contiguous()
        return save({"soft_prefix": tensor})

    def from_bytes(self, data: bytes) -> object:
        if type(data) is not bytes:
            raise SoftPrefixBackendError("PREFIX_BYTES_REQUIRED")
        try:
            from safetensors.torch import load
        except ImportError as exc:
            raise SoftPrefixBackendError("SAFETENSORS_UNAVAILABLE") from exc
        values = load(data)
        if set(values) != {"soft_prefix"}:
            raise SoftPrefixBackendError("PREFIX_FILE_INVALID")
        value = values["soft_prefix"]
        if value.shape != (1, self.prefix_tokens, self.hidden_size):
            raise SoftPrefixBackendError("PREFIX_SHAPE_INVALID")
        if self.to_bytes(value) != data:
            raise SoftPrefixBackendError("PREFIX_CODEC_NONCANONICAL")
        return value


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class FrozenQwenSoftPrefixBackend:
    """Frozen Qwen execution with bounded trainable soft-prefix state."""

    def __init__(
        self,
        model_path: str | Path,
        *,
        prefix_tokens: int = 16,
        learning_rate: float = 0.05,
        default_steps: int = 12,
        max_new_tokens: int = 24,
        device: str = "cuda",
        dequantize_fp8: bool = True,
    ) -> None:
        if type(prefix_tokens) is not int or not 1 <= prefix_tokens <= 64:
            raise SoftPrefixBackendError("PREFIX_TOKEN_COUNT_INVALID")
        if learning_rate <= 0 or default_steps < 1 or max_new_tokens < 1:
            raise SoftPrefixBackendError("PREFIX_CONTROL_INVALID")
        self.model_path = str(Path(model_path))
        self.prefix_tokens = prefix_tokens
        self.learning_rate = float(learning_rate)
        self.default_steps = int(default_steps)
        self.max_new_tokens = int(max_new_tokens)
        self.device = device
        self.dequantize_fp8 = bool(dequantize_fp8)
        self.torch: Any = None
        self.tokenizer: Any = None
        self.model: Any = None
        self.replaced_fp8_linears = 0

    def load(self) -> None:
        if self.model is not None:
            return
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise SoftPrefixBackendError("MODEL_DEPENDENCY_UNAVAILABLE") from exc
        if self.device == "cuda" and torch.cuda.is_available() is not True:
            raise SoftPrefixBackendError("CUDA_UNAVAILABLE")
        tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            local_files_only=True,
            trust_remote_code=False,
            use_fast=True,
        )
        model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            local_files_only=True,
            trust_remote_code=False,
            dtype="auto",
            device_map=self.device,
            attn_implementation="eager",
            low_cpu_mem_usage=True,
        )
        if self.dequantize_fp8:
            self.replaced_fp8_linears = self._dequantize_fp8_linears(model, torch)
            if self.replaced_fp8_linears < 1:
                raise SoftPrefixBackendError("FP8_DEQUANTIZATION_NOT_APPLIED")
        model.eval()
        for parameter in model.parameters():
            parameter.requires_grad_(False)
        self.torch, self.tokenizer, self.model = torch, tokenizer, model

    @classmethod
    def _dequantize_fp8_linears(cls, module: Any, torch: Any) -> int:
        try:
            from transformers.integrations.finegrained_fp8 import FP8Linear
        except ImportError as exc:
            raise SoftPrefixBackendError("FP8_RUNTIME_UNAVAILABLE") from exc
        replaced = 0
        for name, child in list(module.named_children()):
            if isinstance(child, FP8Linear):
                rows, columns = child.weight.shape
                block_rows, block_columns = child.block_size
                if rows % block_rows or columns % block_columns:
                    raise SoftPrefixBackendError("FP8_BLOCK_SHAPE_INVALID")
                replacement = torch.nn.Linear(
                    columns,
                    rows,
                    bias=child.bias is not None,
                    device=child.weight.device,
                    dtype=torch.bfloat16,
                )
                with torch.no_grad():
                    blocks = child.weight.float().reshape(
                        rows // block_rows,
                        block_rows,
                        columns // block_columns,
                        block_columns,
                    )
                    scales = child.weight_scale_inv.float().reshape(
                        rows // block_rows, columns // block_columns
                    )
                    replacement.weight.copy_(
                        (blocks * scales[:, None, :, None])
                        .reshape(rows, columns)
                        .to(torch.bfloat16)
                    )
                    if child.bias is not None:
                        replacement.bias.copy_(child.bias.to(torch.bfloat16))
                replacement.requires_grad_(False)
                module._modules[name] = replacement
                replaced += 1
                del child, blocks, scales
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            else:
                replaced += cls._dequantize_fp8_linears(child, torch)
        return replaced

    def _require_loaded(self) -> None:
        if self.model is None or self.tokenizer is None or self.torch is None:
            raise SoftPrefixBackendError("MODEL_NOT_LOADED")

    def _ids(self, text: str, *, special: bool) -> Any:
        if type(text) is not str or not text:
            raise SoftPrefixBackendError("TEXT_REQUIRED")
        return self.tokenizer(
            text, return_tensors="pt", add_special_tokens=special
        )["input_ids"].to(self.device)

    def seed_prefix(self, event_text: str) -> Any:
        self._require_loaded()
        torch = self.torch
        event_ids = self._ids(event_text, special=True)
        with torch.no_grad():
            event_embeddings = self.model.get_input_embeddings()(event_ids).detach()
        count = event_embeddings.shape[1]
        if count < 1:
            raise SoftPrefixBackendError("EVENT_TOKENIZATION_EMPTY")
        if count == 1:
            positions = torch.zeros(self.prefix_tokens, dtype=torch.long, device=self.device)
        else:
            positions = torch.linspace(
                0, count - 1, steps=self.prefix_tokens, device=self.device
            ).round().long()
        return event_embeddings.index_select(1, positions).clone()

    def train_prefix(
        self,
        *,
        event_text: str,
        cue_text: str,
        target_text: str,
        steps: int | None = None,
    ) -> PrefixTrainingResult:
        self._require_loaded()
        torch = self.torch
        step_count = self.default_steps if steps is None else int(steps)
        if step_count < 1 or step_count > 256:
            raise SoftPrefixBackendError("PREFIX_STEP_COUNT_INVALID")
        cue_ids = self._ids(cue_text, special=True)
        target_ids = self._ids(target_text, special=False)
        sequence_ids = torch.cat((cue_ids, target_ids), dim=1)
        with torch.no_grad():
            sequence_embeddings = self.model.get_input_embeddings()(sequence_ids).detach()
        prefix = torch.nn.Parameter(self.seed_prefix(event_text))
        labels = torch.cat(
            (
                torch.full(
                    (1, self.prefix_tokens + cue_ids.shape[1]),
                    -100,
                    device=self.device,
                    dtype=sequence_ids.dtype,
                ),
                target_ids,
            ),
            dim=1,
        )
        attention_mask = torch.ones(
            (1, self.prefix_tokens + sequence_ids.shape[1]),
            device=self.device,
            dtype=torch.long,
        )
        optimizer = torch.optim.AdamW([prefix], lr=self.learning_rate, weight_decay=0.0)
        initial_loss = final_loss = 0.0
        last_gradient_norm = 0.0
        for index in range(step_count):
            optimizer.zero_grad(set_to_none=True)
            output = self.model(
                inputs_embeds=torch.cat((prefix, sequence_embeddings), dim=1),
                attention_mask=attention_mask,
                labels=labels,
                use_cache=False,
            )
            loss = output.loss
            if torch.isfinite(loss).item() is not True:
                raise SoftPrefixBackendError("PREFIX_LOSS_NONFINITE")
            if index == 0:
                initial_loss = float(loss.detach().float().item())
            loss.backward()
            if prefix.grad is None or torch.isfinite(prefix.grad).all().item() is not True:
                raise SoftPrefixBackendError("PREFIX_GRADIENT_NONFINITE")
            last_gradient_norm = float(prefix.grad.float().norm().item())
            if last_gradient_norm <= 0:
                raise SoftPrefixBackendError("PREFIX_GRADIENT_ZERO")
            torch.nn.utils.clip_grad_norm_([prefix], max_norm=1.0)
            optimizer.step()
            final_loss = float(loss.detach().float().item())
        result = prefix.detach().to(device="cpu").contiguous()
        raw = result.view(torch.uint8).numpy().tobytes()
        return PrefixTrainingResult(
            prefix=result,
            initial_loss=initial_loss,
            final_loss=final_loss,
            gradient_norm=last_gradient_norm,
            steps=step_count,
            tensor_sha256=_sha(raw),
        )

    def generate(
        self,
        public_prompt: str,
        *,
        prefix: Any | None,
        max_new_tokens: int | None = None,
    ) -> PrefixGenerationResult:
        self._require_loaded()
        torch = self.torch
        token_limit = self.max_new_tokens if max_new_tokens is None else int(max_new_tokens)
        if not 1 <= token_limit <= 256:
            raise SoftPrefixBackendError("GENERATION_TOKEN_LIMIT_INVALID")
        prompt_ids = self._ids(public_prompt, special=True)
        return self._generate_ids(prompt_ids, prefix=prefix, token_limit=token_limit)

    def generate_chat(
        self,
        messages: tuple[dict[str, str], ...],
        *,
        prefix: Any | None,
        max_new_tokens: int | None = None,
    ) -> PrefixGenerationResult:
        """Generate through the checkpoint's native instruction template."""

        self._require_loaded()
        token_limit = self.max_new_tokens if max_new_tokens is None else int(max_new_tokens)
        if not 1 <= token_limit <= 256:
            raise SoftPrefixBackendError("GENERATION_TOKEN_LIMIT_INVALID")
        if (
            not isinstance(messages, tuple)
            or not messages
            or any(
                not isinstance(row, dict)
                or set(row) != {"role", "content"}
                or row["role"] not in {"system", "user", "assistant"}
                or type(row["content"]) is not str
                or not row["content"]
                for row in messages
            )
        ):
            raise SoftPrefixBackendError("CHAT_MESSAGES_INVALID")
        prompt_ids = self.tokenizer.apply_chat_template(
            list(messages),
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt",
        )
        if isinstance(prompt_ids, dict):
            prompt_ids = prompt_ids["input_ids"]
        prompt_ids = prompt_ids.to(self.device)
        return self._generate_ids(prompt_ids, prefix=prefix, token_limit=token_limit)

    def _generate_ids(
        self,
        prompt_ids: Any,
        *,
        prefix: Any | None,
        token_limit: int,
    ) -> PrefixGenerationResult:
        torch = self.torch
        prompt_digest = _sha(
            _canonical([int(item) for item in prompt_ids[0].detach().cpu().tolist()])
        )
        with torch.no_grad():
            prompt_embeddings = self.model.get_input_embeddings()(prompt_ids).detach()
            if prefix is None:
                prefix_device = prompt_embeddings[:, :0]
                prefix_digest = _sha(b"")
            else:
                if getattr(prefix, "ndim", None) != 3 or prefix.shape[0] != 1:
                    raise SoftPrefixBackendError("PREFIX_SHAPE_INVALID")
                prefix_device = prefix.to(
                    device=self.device, dtype=prompt_embeddings.dtype
                )
                if prefix_device.shape[-1] != prompt_embeddings.shape[-1]:
                    raise SoftPrefixBackendError("PREFIX_HIDDEN_SIZE_INVALID")
                prefix_digest = _sha(
                    prefix_device.detach().cpu().contiguous().view(torch.uint8).numpy().tobytes()
                )
            combined = torch.cat((prefix_device, prompt_embeddings), dim=1)
            activation_delta_norm = 0.0
            if prefix is not None:
                base_probe = self.model(
                    input_ids=prompt_ids,
                    attention_mask=torch.ones_like(prompt_ids),
                    use_cache=False,
                    output_hidden_states=True,
                )
                memory_probe = self.model(
                    inputs_embeds=combined,
                    attention_mask=torch.ones(
                        combined.shape[:2], device=self.device, dtype=torch.long
                    ),
                    use_cache=False,
                    output_hidden_states=True,
                )
                activation_delta_norm = float(
                    (
                        memory_probe.hidden_states[1][:, -1, :].float()
                        - base_probe.hidden_states[1][:, -1, :].float()
                    )
                    .norm()
                    .item()
                )
            attention_mask = torch.ones(
                combined.shape[:2], device=self.device, dtype=torch.long
            )
            output = self.model(
                inputs_embeds=combined,
                attention_mask=attention_mask,
                use_cache=True,
            )
            cache = output.past_key_values
            next_id = output.logits[:, -1, :].argmax(dim=-1, keepdim=True)
            generated: list[int] = []
            eos_ids = self.tokenizer.eos_token_id
            eos_set = {int(eos_ids)} if type(eos_ids) is int else set(eos_ids or ())
            for _ in range(token_limit):
                value = int(next_id.item())
                if value in eos_set:
                    break
                generated.append(value)
                attention_mask = torch.cat(
                    (
                        attention_mask,
                        torch.ones((1, 1), device=self.device, dtype=torch.long),
                    ),
                    dim=1,
                )
                output = self.model(
                    input_ids=next_id,
                    attention_mask=attention_mask,
                    past_key_values=cache,
                    use_cache=True,
                )
                cache = output.past_key_values
                next_id = output.logits[:, -1, :].argmax(dim=-1, keepdim=True)
        text = self.tokenizer.decode(generated, skip_special_tokens=True)
        return PrefixGenerationResult(
            text=text,
            token_ids=tuple(generated),
            public_prompt_token_ids_sha256=prompt_digest,
            prefix_tensor_sha256=prefix_digest,
            activation_delta_norm=activation_delta_norm,
        )

    def save_prefix(self, path: str | Path, result: PrefixTrainingResult) -> dict[str, Any]:
        self._require_loaded()
        try:
            from safetensors.torch import save_file
        except ImportError as exc:
            raise SoftPrefixBackendError("SAFETENSORS_UNAVAILABLE") from exc
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        tensor = result.prefix.detach().to(device="cpu").contiguous()
        save_file({"soft_prefix": tensor}, str(target))
        raw = target.read_bytes()
        receipt = {
            "bytes": len(raw),
            "path_name": target.name,
            "prefix_tokens": int(tensor.shape[1]),
            "sha256": _sha(raw),
            "tensor_sha256": result.tensor_sha256,
        }
        target.with_suffix(target.suffix + ".json").write_bytes(_canonical(receipt) + b"\n")
        return receipt

    def load_prefix(self, path: str | Path) -> Any:
        self._require_loaded()
        try:
            from safetensors.torch import load_file
        except ImportError as exc:
            raise SoftPrefixBackendError("SAFETENSORS_UNAVAILABLE") from exc
        values = load_file(str(Path(path)), device="cpu")
        if set(values) != {"soft_prefix"}:
            raise SoftPrefixBackendError("PREFIX_FILE_INVALID")
        prefix = values["soft_prefix"]
        if prefix.ndim != 3 or prefix.shape[0] != 1 or prefix.shape[1] != self.prefix_tokens:
            raise SoftPrefixBackendError("PREFIX_SHAPE_INVALID")
        return prefix


__all__ = [
    "FrozenQwenSoftPrefixBackend",
    "PrefixGenerationResult",
    "PrefixTrainingResult",
    "SoftPrefixBackendError",
    "SoftPrefixTensorCodec",
]
