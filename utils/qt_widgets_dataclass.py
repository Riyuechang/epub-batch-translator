from dataclasses import dataclass

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QWidget, 
    QLabel,
    QPushButton,
    QLineEdit, 
    QPlainTextEdit, 
    QComboBox,
    QCheckBox
)


@dataclass
class SelectPathWidget:
    layout: QHBoxLayout
    file_combo_box: QComboBox
    path_label: QLabel
    path_line_edit: QLineEdit
    refresh_button: QPushButton
    open_folder_button: QPushButton
    subfolder_check_box: QCheckBox

@dataclass
class CopyLineEdit:
    line_edit: QLineEdit
    action: QAction

@dataclass
class ParamsFileWidget:
    layout: QHBoxLayout | QVBoxLayout
    file_label: QLabel
    file_combo_box: QComboBox
    refresh_button: QPushButton
    save_button: QPushButton
    delete_button: QPushButton

@dataclass
class PromptParamsWidget:
    translation_prompt: QPlainTextEdit
    glossary_prompt: QLineEdit

@dataclass
class VllmParamsWidget:
    widget: QWidget
    model: QLineEdit
    tokenizer: QLineEdit
    dtype: QLineEdit
    kv_cache_dtype: QLineEdit
    kv_offloading_size: QLineEdit
    kv_offloading_backend: QLineEdit
    quantization: QLineEdit
    gpu_memory_utilization: QLineEdit
    max_model_len: QLineEdit
    max_num_batched_tokens: QLineEdit
    max_num_seqs: QLineEdit
    enable_chunked_prefill: QCheckBox
    enable_prefix_caching: QCheckBox
    enforce_eager: QCheckBox

    #runner: QLineEdit
    #language_model_only: QCheckBox
    #async_scheduling: QCheckBox

    #trust_remote_code: QCheckBox
    #pipeline_parallel_size: QLineEdit
    #tensor_parallel_size: QLineEdit
    #enable_expert_parallel: QCheckBox
    #seed: QLineEdit