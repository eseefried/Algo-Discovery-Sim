"""One shared Transformers/PEFT model behind the swarm's local chat API.

GPU dependencies are imported only at startup; ordinary pipeline installations and
offline contract tests do not need PyTorch. Run with scripts/serve_nemotron.sh.
"""

import argparse
import json
import threading
import time
from contextlib import nullcontext
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

DEFAULT_ADAPTER = Path(
    "/mnt/zgx1-shared/nemotron-bolt-e4b-quantum-lora-20261101T010128Z-5eb582d7"
)


def format_enforcer_bridge():
    """Bridge LMFE's Transformers-4 import to the Transformers-5 class location.

    Keep this compatibility alias in-process; never patch installed package files.
    """
    import transformers.tokenization_utils as legacy_tokenizers
    from transformers.tokenization_utils_base import PreTrainedTokenizerBase

    if not hasattr(legacy_tokenizers, "PreTrainedTokenizerBase"):
        legacy_tokenizers.PreTrainedTokenizerBase = PreTrainedTokenizerBase
    from lmformatenforcer.integrations import transformers as bridge

    return bridge


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: list[Message] = Field(min_length=1)
    max_tokens: int = Field(default=4096, ge=1, le=16384)
    response_format: dict | None = None
    stream: Literal[False] = False
    temperature: float = Field(default=0, ge=0, le=2)
    repetition_penalty: float = Field(default=1, ge=1, le=2)
    seed: int = Field(default=0, ge=0, le=2147483647)
    max_time_seconds: float | None = Field(default=None, ge=1, le=600)
    use_adapter: bool = True  # Set by the server's model-name mapping, not the caller.


def check_adapter(adapter: Path) -> dict:
    # Check readability before importing/downloading any large dependencies or weights.
    with (adapter / "adapter_model.safetensors").open("rb") as weights:
        weights.read(8)
    return json.loads((adapter / "adapter_config.json").read_text())


class TransformersModel:
    def __init__(self, adapter: Path, attention: str = "mixed"):
        config = check_adapter(adapter)
        import torch
        import transformers
        from peft import PeftModel

        if not torch.cuda.is_available():
            raise RuntimeError("CUDA-enabled PyTorch is required; refusing CPU fallback.")
        # Match the model class used by this adapter's training recipe.
        base = transformers.AutoModelForCausalLM.from_pretrained(
            config["base_model_name_or_path"], device_map="auto", dtype=torch.bfloat16,
            # Audio lacks SDPA support; our text-only workload can still use
            # optimized attention without forcing the unused towers to use it.
            attn_implementation=({"": "eager", "text_config": "sdpa",
                                  "audio_config": "eager", "vision_config": "eager"}
                                 if attention == "mixed" else "eager"),
        )
        self.model = PeftModel.from_pretrained(base, str(adapter)).eval()
        attached = sum(name.endswith("lora_A.default") for name, _ in self.model.named_modules())
        if attached != 258:
            raise RuntimeError(f"Expected 258 trained LoRA modules; attached {attached}.")
        print(f"LoRA modules attached: {attached}", flush=True)
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(str(adapter))
        self.format_bridge = format_enforcer_bridge()
        # Building Gemma's large vocabulary trie is expensive; share it across requests.
        self.tokenizer_data = self.format_bridge.build_token_enforcer_tokenizer_data(self.tokenizer)
        self.torch = torch

    def generate(self, request: ChatRequest, schema: dict | None) -> dict:
        messages = [m.model_dump() for m in request.messages]
        if schema is not None:
            instruction = "Return only JSON matching this schema: " + json.dumps(schema)
            if messages[0]["role"] == "system":
                messages[0]["content"] += "\n" + instruction
            else:
                messages.insert(0, {"role": "system", "content": instruction})
        inputs = self.tokenizer.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, enable_thinking=False,
            return_tensors="pt", return_dict=True,
        ).to(self.model.device)
        count = inputs["input_ids"].shape[-1]
        context_limit = getattr(self.model.config.get_text_config(), "max_position_embeddings", 65536)
        if count + request.max_tokens > context_limit:
            raise HTTPException(400, "Input plus requested output exceeds model context.")
        kwargs = {"do_sample": request.temperature > 0,
                  "repetition_penalty": request.repetition_penalty}
        if schema is not None:
            from lmformatenforcer import JsonSchemaParser

            kwargs["prefix_allowed_tokens_fn"] = self.format_bridge.build_transformers_prefix_allowed_tokens_fn(
                self.tokenizer_data, JsonSchemaParser(schema)
            )
        else:
            # Exact training stop-token contract for unmodified LaTeX output.
            kwargs["eos_token_id"] = [self.tokenizer.convert_tokens_to_ids("<turn|>"),
                                      self.tokenizer.eos_token_id]
        if request.temperature > 0:
            kwargs.update(temperature=request.temperature, top_p=0.9)
        if request.max_time_seconds is not None:
            kwargs["max_time"] = request.max_time_seconds
        self.torch.manual_seed(request.seed)
        adapter_context = nullcontext() if request.use_adapter else self.model.disable_adapter()
        started = time.monotonic()
        with adapter_context, self.torch.inference_mode():
            output = self.model.generate(
                **inputs, max_new_tokens=request.max_tokens, **kwargs,
                pad_token_id=(self.tokenizer.pad_token_id if self.tokenizer.pad_token_id is not None
                              else self.tokenizer.eos_token_id),
            )
        tokens = output[0, count:]
        content = self.tokenizer.decode(tokens, skip_special_tokens=True)
        eos = self.model.generation_config.eos_token_id
        eos_ids = eos if isinstance(eos, list) else [eos]
        finished = bool(len(tokens)) and int(tokens[-1]) in eos_ids
        return {
            "model": request.model,
            "adapter_enabled": request.use_adapter,
            "generation_seconds": round(time.monotonic() - started, 3),
            "choices": [{"finish_reason": "stop" if finished else "length",
                         "message": {"role": "assistant", "content": content}}],
            "usage": {"prompt_tokens": count, "completion_tokens": len(tokens),
                      "total_tokens": count + len(tokens)},
        }


def create_app(backend, model_name: str = "nemotron-quantum", *,
               serve_base: bool = False) -> FastAPI:
    app = FastAPI()
    lock = threading.Lock()

    @app.get("/v1/models")
    def models():
        names = [model_name] + ([model_name + "-base"] if serve_base else [])
        return {"object": "list", "data": [{"id": name, "object": "model"} for name in names]}

    @app.post("/v1/chat/completions")
    def chat(request: ChatRequest):
        if request.model != model_name and not (serve_base and request.model == model_name + "-base"):
            raise HTTPException(404, "Unknown served model.")
        request.use_adapter = request.model == model_name
        fmt = request.response_format
        schema = None
        if fmt is not None and fmt != {"type": "text"}:
            nested = fmt.get("json_schema")
            schema = nested.get("schema") if isinstance(nested, dict) else None
            if fmt.get("type") != "json_schema" or not isinstance(schema, dict):
                raise HTTPException(400, "Use a JSON Schema response_format or plain text.")
        # One model instance, serialized GPU generation; agents can queue concurrently.
        with lock:
            return backend.generate(request, schema)

    return app


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adapter", type=Path, default=DEFAULT_ADAPTER)
    parser.add_argument("--model-name", default="nemotron-quantum")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--attention", choices=["mixed", "eager"], default="mixed")
    parser.add_argument("--serve-base", action="store_true", help="Expose a -base alias with LoRA disabled for diagnostics")
    parser.add_argument("--check", action="store_true", help="Check weight access without loading")
    args = parser.parse_args()
    try:
        check_adapter(args.adapter)
    except OSError as exc:
        parser.exit(1, f"Adapter is not readable: {exc}\n")
    if args.check:
        print("Adapter readable.")
        return
    import uvicorn

    model = TransformersModel(args.adapter, attention=args.attention)
    uvicorn.run(create_app(model, args.model_name, serve_base=args.serve_base),
                host="127.0.0.1", port=args.port, workers=1)


if __name__ == "__main__":
    main()
