import tomllib

from config import config


class FrontPage:
    def __init__(
        self,
        select_all_epub_flies:str,
        open_epub_folder:str,
        start_processing:str,
        language: str
    ):
        self.select_all_epub_flies = select_all_epub_flies
        self.open_epub_folder = open_epub_folder
        self.start_processing = start_processing
        self.language = language

class Api:
    def __init__(
        self,
        tab_name: str
    ):
        self.tab_name = tab_name

class Vllm:
    def __init__(
        self,
        tab_name: str
    ):
        self.tab_name = tab_name

class Language:
    def __init__(self, language_path: str):
        with open(language_path, "rb") as file:
            language_data: dict[str, dict[str, str]] = tomllib.load(file)

        self.load_language(**language_data)

    def load_language(
        self,
        front_page: dict[str, str],
        llm_api: dict[str, str],
        vllm: dict[str, str]
    ):
        self.front_page = FrontPage(**front_page)
        self.llm_api = Api(**llm_api)
        self.vllm = Vllm(**vllm)


language = Language(f"./ui/language/{config.ui.language}.toml")