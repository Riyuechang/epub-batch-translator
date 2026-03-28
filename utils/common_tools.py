from pathlib import Path

from config import USER_CONFIG_PATH


def truncate_middle(
    text:str, 
    max_length: int, 
    ellipsis: str = "..."
):
    if len(text) <= max_length:
        return text

    remaining_len = max_length - len(ellipsis)

    front_len = remaining_len // 2
    back_len = remaining_len - front_len

    return text[:front_len] + ellipsis + text[-back_len:]

def path_truncate_middle(
    path:str, 
    parent_path_max_length: int = 24, 
    file_max_length: int = 40
):
    max_length = parent_path_max_length + file_max_length

    if len(path) <= max_length:
        return path

    file_path = Path(path)

    new_parent_path = truncate_middle(str(file_path.parent), parent_path_max_length)

    if len(new_parent_path) + len(file_path.name) <= max_length:
        return str(Path(new_parent_path, file_path.name))
    
    new_file = truncate_middle(file_path.name, file_max_length)

    return str(Path(new_parent_path, new_file))

def remove_user_config():
    USER_CONFIG_PATH.unlink(missing_ok=True)