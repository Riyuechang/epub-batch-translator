from config import USER_CONFIG_PATH


def remove_user_config():
    USER_CONFIG_PATH.unlink(missing_ok=True)