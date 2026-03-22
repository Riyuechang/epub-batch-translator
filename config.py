import json
import tomllib
from pathlib import Path
from dataclasses import dataclass, field, asdict


PRESET_CONFIG_PATH = Path("./config.toml")

USER_DATA_PATH = Path("./user_data")
USER_CONFIG_PATH = USER_DATA_PATH.joinpath("config.json")


@dataclass
class UiConfig:
    width: int
    height: int
    language: str

@dataclass
class Config:
    ui: UiConfig = field(init=False)

    def load_config(self):
        if USER_CONFIG_PATH.is_file():
            with USER_CONFIG_PATH.open("r", encoding="utf-8") as file:
                config_data: dict[str, dict[str, str]] = json.load(file)
        else:
            with PRESET_CONFIG_PATH.open("rb") as file:
                config_data: dict[str, dict[str, str]] = tomllib.load(file)

        self.set_config(**config_data)

    def set_config(
        self,
        ui: dict[str, str]
    ):
        self.ui = UiConfig(**ui)

    def save_user_config(self):
        new_config = asdict(self)

        USER_DATA_PATH.mkdir(parents=True, exist_ok=True)

        with USER_CONFIG_PATH.open('w', encoding='utf-8') as file:
            json.dump(new_config, file, indent=4, ensure_ascii=False)


config = Config()
config.load_config()