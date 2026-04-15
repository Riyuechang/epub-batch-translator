import tomllib
from pathlib import Path

from config import config
from utils.dataclass_tools import dataclass_pre_init, set_dataclass_value


LANGUAGE_PATH = Path("./ui/language")


@dataclass_pre_init
class SettingsMenu:
    menu_name: str
    reset_ui: str

@dataclass_pre_init
class MenuBar:
    settings_menu: SettingsMenu
    language: str
    about: str

@dataclass_pre_init
class FolderOptions:
    subfolder: str

@dataclass_pre_init
class EpubWidget:
    select_all_epub_files: str
    folder_path: str

@dataclass_pre_init
class GlossaryWidget:
    auto_glossary: str
    folder_path: str

@dataclass_pre_init
class ProcessingTab:
    tab_name: str
    select_translator: str
    no_task: str
    auto_processing: str
    extract_content: str
    calculate_similarity: str
    content_chunking: str
    translate: str
    alignment_check: str
    replace_translation: str

@dataclass_pre_init
class TranslationTag:
    content: str
    glossary: str
    history: str

@dataclass_pre_init
class GlossaryTag:
    source_text: str
    translation: str
    annotation: str

@dataclass_pre_init
class PromptsOptions:
    dynamic_glossary: str

@dataclass_pre_init
class PromptsTab:
    tab_name: str
    translation_prompt: str
    translation_prompt_example: str
    translation_tag: TranslationTag
    glossary_prompt: str
    glossary_prompt_example: str
    glossary_tag: GlossaryTag
    options: PromptsOptions

@dataclass_pre_init
class ParameterFileLabel:
    text: str

@dataclass_pre_init
class LlmApiTab:
    tab_name: str

@dataclass_pre_init
class VllmTab:
    tab_name: str

@dataclass_pre_init
class WarningMessage:
    title: str
    message: str
    confirm: str
    cancel: str

@dataclass_pre_init
class SystemMessage:
    message: str

@dataclass_pre_init
class AboutMessage:
    title: str
    message: str
    confirm: str

@dataclass_pre_init
class SaveMessage:
    warning: WarningMessage
    system: SystemMessage

@dataclass_pre_init
class Language:
    menu_bar: MenuBar
    folder_options: FolderOptions
    epub_widget: EpubWidget
    glossary_widget: GlossaryWidget
    parameter_file_label: ParameterFileLabel
    processing_tab: ProcessingTab
    prompts_tab: PromptsTab
    llm_api_tab: LlmApiTab
    vllm_tab: VllmTab
    reset_ui_message: WarningMessage
    about_message: AboutMessage
    save_message: SaveMessage
    delete_warning_message: WarningMessage

    def __post_init__(self):
        self.load_language(config.ui.language)

    def load_language(self, ui_language: str):
        with LANGUAGE_PATH.joinpath(f"{ui_language}.toml").open("rb") as file:
            language_data: dict[str, dict[str, str]] = tomllib.load(file)

        set_dataclass_value(self, language_data)


language = Language()