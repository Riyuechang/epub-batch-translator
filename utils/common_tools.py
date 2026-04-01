import re
from pathlib import Path

from config import config, USER_CONFIG_PATH, EpubConfig, GlossaryConfig


def remove_user_config():
    USER_CONFIG_PATH.unlink(missing_ok=True)

def set_dynamic_glossary_state(state: bool):
    config.prompt_options.dynamic_glossary = state

def set_file_options(
    set_config: EpubConfig | GlossaryConfig, 
    text: str
):
    if text == "":
        return

    if re.match(r"-- .*? --", text):
        set_config.options = ""
        return

    set_config.options = text

def get_path_dict(path: str | Path):
    if isinstance(path, str):
        path = Path(path)

    return {
        path_obj.stem: str(path_obj) if path_obj.is_file() else get_path_dict(path_obj)
        for path_obj in path.iterdir()
    }