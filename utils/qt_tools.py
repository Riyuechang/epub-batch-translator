from collections.abc import Callable

from ui.content import language


def set_language(
    widgets_set_language_func: list[Callable[[], None]],
    ui_language: str = ""
):
    if ui_language:
        language.load_language(ui_language)

    for set_language_func in widgets_set_language_func:
        set_language_func()