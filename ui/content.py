import tomllib
from pathlib import Path
from dataclasses import dataclass

from config import config
from utils.tools import set_dataclass_value


LANGUAGE_PATH = Path("./ui/language")


@dataclass
class FrontPage:
    select_all_epub_flies: str = str
    open_epub_folder: str = str
    start_processing: str = str
    language: str = str
    stage_none: str = str

@dataclass
class Api:
    tab_name: str = str

@dataclass
class Vllm:
    tab_name: str = str

@dataclass
class Language:
    front_page: FrontPage = FrontPage
    llm_api: Api = Api
    vllm: Vllm = Vllm

    def __post_init__(self):
        self.load_language(config.ui.language)

    def load_language(self, ui_language: str):
        with LANGUAGE_PATH.joinpath(f"{ui_language}.toml").open("rb") as file:
            language_data: dict[str, dict[str, str]] = tomllib.load(file)

        set_dataclass_value(self, language_data)


language = Language()