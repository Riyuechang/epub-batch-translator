import tomllib
from pathlib import Path
from dataclasses import dataclass, field

from config import config


LANGUAGE_PATH = Path("./ui/language")


@dataclass
class FrontPage:
    select_all_epub_flies:str
    open_epub_folder:str
    start_processing:str
    language: str
    stage_none: str

@dataclass
class Api:
    tab_name: str

@dataclass
class Vllm:
    tab_name: str

@dataclass
class Language:
    front_page: FrontPage = field(init=False)
    llm_api: Api = field(init=False)
    vllm: Vllm = field(init=False)

    def load_language(self, ui_language: str):
        with LANGUAGE_PATH.joinpath(f"{ui_language}.toml").open("rb") as file:
            language_data: dict[str, dict[str, str]] = tomllib.load(file)

        self.set_language(**language_data)

    def set_language(
        self,
        front_page: dict[str, str],
        llm_api: dict[str, str],
        vllm: dict[str, str]
    ):
        self.front_page = FrontPage(**front_page)
        self.llm_api = Api(**llm_api)
        self.vllm = Vllm(**vllm)


language = Language()
language.load_language(config.ui.language)