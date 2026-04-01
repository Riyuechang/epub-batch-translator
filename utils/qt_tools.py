import sys
from pathlib import Path
from collections.abc import Callable

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QProcess, Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QApplication, 
    QFileDialog, 
    QFrame, 
    QMessageBox, 
    QPushButton,
    QComboBox,
    QLineEdit
)

from config import config
from ui.image import icon
from ui.content import language
from utils.common_tools import remove_user_config


class Epub:


    @staticmethod
    def open_folder(set_text_func: Callable[[], None]):
        folder_path = QFileDialog.getExistingDirectory(directory=config.epub.epub_folder_path)

        if folder_path:
            set_text_func(folder_path)

    @staticmethod
    def read(text: str, combo_box: QComboBox):
        config.epub.epub_folder_path = text
        folder_path = Path(text)

        if config.epub.subfolder:
            epub_files = [str(file.relative_to(folder_path)) for file in folder_path.rglob("*.epub") if file.is_file()]
        else:
            epub_files = [file.name for file in folder_path.glob("*.epub") if file.is_file()]

        epub_files.sort()

        combo_box.clear()
        combo_box.addItems([language.epub_widget.select_all_epub_flies] + epub_files)

    @staticmethod
    def set_subfolder(state: bool, combo_box: QComboBox):
        config.epub.subfolder = state
        Epub.read(config.epub.epub_folder_path, combo_box)


def copy_to_clipboard(text: str):
    clipboard = QApplication.clipboard()
    clipboard.setText(text)

def set_language(
    widgets_set_language_func: list[Callable[[], None]],
    ui_language: str = ""
):
    if ui_language:
        language.load_language(ui_language)
        config.ui.language = ui_language

    for set_language_func in widgets_set_language_func:
        set_language_func()

def set_frame():
    frame = QFrame()
    frame.setFrameShape(QFrame.Shape.HLine)
    frame.setFrameShadow(QFrame.Shadow.Sunken)

    return frame

def set_copy_line_edit(cls: QMainWindow, copy_text: str):
    copy_line_edit = QLineEdit()

    copy_line_edit.setText(copy_text)
    copy_line_edit.setReadOnly(True)
    copy_line_edit.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    copy_action = QAction(QIcon(icon.copy), "")
    copy_action.triggered.connect(
        lambda: copy_to_clipboard(copy_line_edit.text())
    )
    copy_line_edit.addAction(copy_action, QLineEdit.ActionPosition.TrailingPosition)

    copy_line_edit_width = copy_line_edit.fontMetrics().horizontalAdvance(copy_line_edit.text())
    copy_line_edit.setFixedWidth(copy_line_edit_width + 35)

    return copy_line_edit, copy_action

def set_push_button_icon(icon_path: str):
    button = QPushButton()
    button.setIcon(QIcon(icon_path))

    return button

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
        QApplication.quit()
        remove_user_config()
        QProcess.startDetached(sys.executable, sys.argv)

def about_message():
    message_box = QMessageBox()

    message_box.setWindowTitle(language.about_message.title)
    message_box.setText(language.about_message.message)
    message_box.setTextFormat(Qt.TextFormat.RichText)
    message_box.addButton(language.about_message.confirm, QMessageBox.ButtonRole.AcceptRole)
    message_box.exec()