import sys
from pathlib import Path
from collections.abc import Callable

from PyQt6.QtCore import QProcess, Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QFileDialog, 
    QFrame, 
    QMessageBox, 
    QComboBox
)

from config import config
from ui.content import language
from utils.common_tools import remove_user_config


def open_folder(set_text_func: Callable[[], None]):
    folder_path = QFileDialog.getExistingDirectory()
    set_text_func(folder_path)

def read_epub(text: str, combo_box: QComboBox):
    config.epub.epub_folder_path = text
    folder_path = Path(text)

    if config.epub.subfolder:
        epub_files = [file.name for file in folder_path.rglob("*.epub") if file.is_file()]
    else:
        epub_files = [file.name for file in folder_path.glob("*.epub") if file.is_file()]

    epub_files.sort()

    combo_box.clear()
    combo_box.addItems([language.epub_widget.select_all_epub_flies] + epub_files)

def set_subfolder(state: bool, combo_box: QComboBox):
    config.epub.subfolder = state
    read_epub(config.epub.epub_folder_path, combo_box)

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