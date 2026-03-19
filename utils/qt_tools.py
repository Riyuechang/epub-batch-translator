from collections.abc import Callable

from ui.content import language


def set_language(widgets_set_language_func: list[Callable[[], None]]):
    for set_language_func in widgets_set_language_func:
        set_language_func()

def reset_language(
    widgets_set_language_func: list[Callable[[], None]],
    ui_language: str
):
    language.load_language(ui_language)
    set_language(widgets_set_language_func)