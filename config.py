import tomllib


class UiConfig:
    def __init__(
        self,
        width: int,
        height: int,
        language: str
    ):
        self.width = width
        self.height = height
        self.language = language

class Config:
    def __init__(self, config_path: str):
        with open(config_path, "rb") as file:
            config_data: dict[str, dict[str, str]] = tomllib.load(file)
        
        self.load_config(**config_data)

    def load_config(
        self,
        ui: dict[str, str]
    ):
        self.ui = UiConfig(**ui)


config = Config("config.toml")