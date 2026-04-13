from typing import Literal

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QFormLayout, QWidget, QLineEdit, QCheckBox

from parameter import params, TagValue
from utils.qt_widgets_dataclass import VllmParamsWidget


LINE_EDIT_MAX_VALUE = 4096
CHECK_BOX_MIN_WIDTH = 96


def set_line_edit(layout: QFormLayout, parameter: TagValue, int_mode: bool = False):
    line_edit = QLineEdit()
    line_edit.setAlignment(Qt.AlignmentFlag.AlignRight)
    line_edit.setMinimumWidth(CHECK_BOX_MIN_WIDTH)
    layout.addRow(parameter.tag, line_edit)

    if parameter.value:
        line_edit.setText(str(parameter.value))

    if int_mode:
        line_edit.setValidator(QIntValidator(1, LINE_EDIT_MAX_VALUE))

    return line_edit

def set_check_box(layout: QFormLayout, parameter: TagValue):
    check_box = QCheckBox()
    check_box.setChecked(parameter.value)
    layout.addRow(parameter.tag, check_box)

    return check_box

def set_vllm_params_widget():
    layout = QFormLayout()
    layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

    widget = QWidget()
    widget.setLayout(layout)
    widget.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    model = set_line_edit(layout, params.vllm.model)
    tokenizer = set_line_edit(layout, params.vllm.tokenizer)
    dtype = set_line_edit(layout, params.vllm.dtype)
    quantization = set_line_edit(layout, params.vllm.quantization)

    kv_cache_dtype = set_line_edit(layout, params.vllm.kv_cache_dtype)
    kv_offloading_size = set_line_edit(layout, params.vllm.kv_offloading_size, int_mode=True)
    kv_offloading_backend = set_line_edit(layout, params.vllm.kv_offloading_backend)

    gpu_memory_utilization = set_line_edit(layout, params.vllm.gpu_memory_utilization, int_mode=True)
    max_model_len = set_line_edit(layout, params.vllm.max_model_len, int_mode=True)
    max_num_batched_tokens = set_line_edit(layout, params.vllm.max_num_batched_tokens, int_mode=True)
    max_num_seqs = set_line_edit(layout, params.vllm.max_num_seqs, int_mode=True)

    enable_chunked_prefill = set_check_box(layout, params.vllm.enable_chunked_prefill)
    enable_prefix_caching = set_check_box(layout, params.vllm.enable_prefix_caching)
    enforce_eager = set_check_box(layout, params.vllm.enforce_eager)

    return VllmParamsWidget(
        widget=widget,
        model=model,
        tokenizer=tokenizer,
        dtype=dtype,
        kv_cache_dtype=kv_cache_dtype,
        kv_offloading_size=kv_offloading_size,
        kv_offloading_backend=kv_offloading_backend,
        quantization=quantization,
        gpu_memory_utilization=gpu_memory_utilization,
        max_model_len=max_model_len,
        max_num_batched_tokens=max_num_batched_tokens,
        max_num_seqs=max_num_seqs,
        enable_chunked_prefill=enable_chunked_prefill,
        enable_prefix_caching=enable_prefix_caching,
        enforce_eager=enforce_eager
    )