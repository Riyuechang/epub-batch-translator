import tomllib
from pathlib import Path

from config import config
from utils.dataclass_tools import dataclass_pre_init, set_dataclass_value


LANGUAGE_PATH = Path("./ui/language")


@dataclass_pre_init
class FrontPage:
    select_all_epub_flies: str
    open_epub_folder: str
    language: str
    stage_none: str
    auto_processing: str
    extract_content: str
    calculate_similarity: str
    content_chunking: str
    translate: str
    alignment_check: str
    replace_translation: str

@dataclass_pre_init
class Prompt:
    tab_name: str

@dataclass_pre_init
class Api:
    tab_name: str

@dataclass_pre_init
class Vllm:
    tab_name: str

@dataclass_pre_init
class Language:
    front_page: FrontPage
    prompt: Prompt
    llm_api: Api
    vllm: Vllm

    def __post_init__(self):
        self.load_language(config.ui.language)

    def load_language(self, ui_language: str):
        with LANGUAGE_PATH.joinpath(f"{ui_language}.toml").open("rb") as file:
            language_data: dict[str, dict[str, str]] = tomllib.load(file)

        set_dataclass_value(self, language_data)


language = Language()