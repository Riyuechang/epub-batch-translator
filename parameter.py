import tomllib
from typing import Any
from pathlib import Path
from dataclasses import dataclass

from utils.dataclass_tools import dataclass_pre_init, set_dataclass_value


VLLM_PARAMS_PATH = Path("./default_params/vllm.toml")


@dataclass_pre_init
class TagValue:
    tag: str
    value: Any

@dataclass_pre_init
class VllmParams:
    model: TagValue
    tokenizer: TagValue
    dtype: TagValue
    kv_cache_dtype: TagValue
    kv_offloading_size: TagValue
    kv_offloading_backend: TagValue
    quantization: TagValue
    gpu_memory_utilization: TagValue
    max_model_len: TagValue
    max_num_batched_tokens: TagValue
    max_num_seqs: TagValue
    enable_chunked_prefill: TagValue
    enable_prefix_caching: TagValue
    enforce_eager: TagValue

    #runner: TagValue
    #language_model_only: TagValue
    #async_scheduling: TagValue

    #trust_remote_code: TagValue
    #pipeline_parallel_size: TagValue
    #tensor_parallel_size: TagValue
    #enable_expert_parallel: TagValue
    #seed: TagValue

    def __post_init__(self):
        self.load_params()

    def load_params(self):
        with VLLM_PARAMS_PATH.open("rb") as file:
            params: dict[str, dict[str, str | int | float | bool]] = tomllib.load(file)

        set_dataclass_value(self, params)

@dataclass
class Params:
    vllm: VllmParams


params = Params(vllm=VllmParams())