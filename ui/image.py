from pathlib import Path

from utils.common_tools import get_path_dict
from utils.dataclass_tools import dataclass_pre_init, set_dataclass_value


ICON_PATH = Path("./ui/icon")


@dataclass_pre_init
class Icon:
    folder_open: str
    copy: str
    save: str
    delete: str
    refresh: str

    def __post_init__(self):
        self.load_image()

    def load_image(self):
        icon_files = get_path_dict(ICON_PATH)

        set_dataclass_value(self, icon_files)


icon = Icon()