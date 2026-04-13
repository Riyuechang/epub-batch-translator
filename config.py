import json
import tomllib
from pathlib import Path
from dataclasses import asdict

from utils.dataclass_tools import dataclass_pre_init, set_dataclass_value


DEFAULT_CONFIG_PATH = Path("./default_config.toml")

USER_DATA_PATH = Path("./user_data")
USER_CONFIG_PATH = USER_DATA_PATH.joinpath("config.json")


@dataclass_pre_init
class UiConfig:
    window_title: str
    language: str
    width: int
    height: int
    tabs_index: int

@dataclass_pre_init
class FolderConfig:
    folder_path: str
    options: str
    subfolder: bool

@dataclass_pre_init
class ParameterFileConfig:
    folder_path: str
    options: str

@dataclass_pre_init
class PromptOptions:
    dynamic_glossary: bool

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
class Config:
    ui: UiConfig
    epub: FolderConfig
    glossary: FolderConfig
    vllm_parameter_file: ParameterFileConfig
    prompt_parameter_file: ParameterFileConfig
    prompt_options: PromptOptions
    translation_tag: TranslationTag
    glossary_tag: GlossaryTag

    def __post_init__(self):
        self.load_config()

    def load_config(self):
        if USER_CONFIG_PATH.is_file():
            with USER_CONFIG_PATH.open("r", encoding="utf-8") as file:
                self._initial_config: dict[str, dict[str, str]] = json.load(file)
        else:
            with DEFAULT_CONFIG_PATH.open("rb") as file:
                self._initial_config: dict[str, dict[str, str]] = tomllib.load(file)

        set_dataclass_value(self, self._initial_config)

    def save_user_config(self):
        new_config = asdict(self)

        if new_config == self._initial_config:
            return

        USER_DATA_PATH.mkdir(parents=True, exist_ok=True)

        with USER_CONFIG_PATH.open('w', encoding='utf-8') as file:
            json.dump(new_config, file, indent=4, ensure_ascii=False)


config = Config()