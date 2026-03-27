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
class EpubWidget:
    select_all_epub_flies: str
    open_epub_folder: str
    subfolder: str

@dataclass_pre_init
class ProcessingStage:
    no_task: str
    auto_processing: str
    extract_content: str
    calculate_similarity: str
    content_chunking: str
    translate: str
    alignment_check: str
    replace_translation: str

@dataclass_pre_init
class PromptTab:
    tab_name: str

@dataclass_pre_init
class LlmApiTab:
    tab_name: str

@dataclass_pre_init
class VllmTab:
    tab_name: str

@dataclass_pre_init
class ResetUiMessage:
    title: str
    message: str
    confirm: str
    cancel: str

@dataclass_pre_init
class AboutMessage:
    title: str
    message: str
    confirm: str

@dataclass_pre_init
class Language:
    menu_bar: MenuBar
    epub_widget: EpubWidget
    processing_stage: ProcessingStage
    prompt_tab: PromptTab
    llm_api_tab: LlmApiTab
    vllm_tab: VllmTab
    reset_ui_message: ResetUiMessage
    about_message: AboutMessage

    def __post_init__(self):
        self.load_language(config.ui.language)

    def load_language(self, ui_language: str):
        with LANGUAGE_PATH.joinpath(f"{ui_language}.toml").open("rb") as file:
            language_data: dict[str, dict[str, str]] = tomllib.load(file)

        set_dataclass_value(self, language_data)


language = Language()