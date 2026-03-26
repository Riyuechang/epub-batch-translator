import sys
from collections.abc import Callable

from PyQt6.QtCore import QProcess, Qt
from PyQt6.QtWidgets import QApplication, QFrame, QMessageBox

from config import config
from ui.content import language
from utils.common_tools import remove_user_config


def set_language(
    widgets_set_language_func: list[Callable[[], None]],
    ui_language: str = ""
):
    if ui_language:
        language.load_language(ui_language)
        config.ui.language = ui_language
        config.save_user_config()

    for set_language_func in widgets_set_language_func:
        set_language_func()

def set_frame():
    frame = QFrame()
    frame.setFrameShape(QFrame.Shape.HLine)
    frame.setFrameShadow(QFrame.Shadow.Sunken)

    return frame

def restart_app():
    QApplication.quit()
    QProcess.startDetached(sys.executable, sys.argv)

def reset_ui_message():
    message_box = QMessageBox()

    message_box.setIcon(QMessageBox.Icon.Warning)
    message_box.setWindowTitle(language.reset_ui_message.title)
    message_box.setText(language.reset_ui_message.message)

    action_button = message_box.addButton(language.reset_ui_message.confirm, QMessageBox.ButtonRole.ActionRole)
    reject_button = message_box.addButton(language.reset_ui_message.cancel, QMessageBox.ButtonRole.RejectRole)

    message_box.setDefaultButton(reject_button)
    message_box.exec()

    clicked_button = message_box.clickedButton()

    if clicked_button == action_button:
        remove_user_config()
        restart_app()

def about_message():
    message_box = QMessageBox()

    message_box.setWindowTitle(language.about_message.title)
    message_box.setText(language.about_message.message)
    message_box.setTextFormat(Qt.TextFormat.RichText)
    message_box.addButton(language.about_message.confirm, QMessageBox.ButtonRole.AcceptRole)
    message_box.exec()