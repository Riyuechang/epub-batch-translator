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
    width: int
    height: int
    language: str

@dataclass_pre_init
class Config:
    epub_folder_path: str
    ui: UiConfig

    def __post_init__(self):
        self.load_config()

    def load_config(self):
        if USER_CONFIG_PATH.is_file():
            with USER_CONFIG_PATH.open("r", encoding="utf-8") as file:
                config_data: dict[str, dict[str, str]] = json.load(file)
        else:
            with DEFAULT_CONFIG_PATH.open("rb") as file:
                config_data: dict[str, dict[str, str]] = tomllib.load(file)

        set_dataclass_value(self, config_data)

    def save_user_config(self):
        new_config = asdict(self)

        USER_DATA_PATH.mkdir(parents=True, exist_ok=True)

        with USER_CONFIG_PATH.open('w', encoding='utf-8') as file:
            json.dump(new_config, file, indent=4, ensure_ascii=False)


config = Config()