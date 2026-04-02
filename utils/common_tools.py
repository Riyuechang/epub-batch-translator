from pathlib import Path
from collections.abc import Callable

from config import config, USER_CONFIG_PATH, EpubConfig, GlossaryConfig


def remove_user_config():
    USER_CONFIG_PATH.unlink(missing_ok=True)

def set_dynamic_glossary_state(state: bool):
    config.prompt_options.dynamic_glossary = state

def set_file_options(
    text: str, 
    current_index_func: Callable[[], int],
    set_config: EpubConfig | GlossaryConfig
):
    if text == "":
        return

    if current_index_func() == 0:
        set_config.options = ""
        return

    set_config.options = text

def get_list_index(data_list: list, value):
    for index, data in enumerate(data_list):
        if data == value:
            return index

    return -1

def get_path_dict(path: str | Path):
    if isinstance(path, str):
        path = Path(path)

    return {
        path_obj.stem: str(path_obj) if path_obj.is_file() else get_path_dict(path_obj)
        for path_obj in path.iterdir()
    }