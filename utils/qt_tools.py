import sys
from pathlib import Path
from dataclasses import dataclass
from collections.abc import Callable
from typing import Literal

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QProcess, Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QHBoxLayout,
    QFileDialog, 
    QFrame, 
    QLabel,
    QMessageBox, 
    QPushButton,
    QCheckBox,
    QComboBox,
    QLineEdit,
    QSizePolicy
)

from config import config, EpubConfig, GlossaryConfig
from ui.image import icon
from ui.content import language
from utils.common_tools import remove_user_config, set_file_options

class Folder:


    @staticmethod
    def open(
        set_config: EpubConfig | GlossaryConfig, 
        set_text_func: Callable[[], None]
    ):
        folder_path = QFileDialog.getExistingDirectory(directory=set_config.folder_path)

        if folder_path:
            set_text_func(folder_path)

    @staticmethod
    def read_files(
        set_config: EpubConfig | GlossaryConfig, 
        text: str, 
        combo_box: QComboBox, 
        pattern: Literal["epub", "json"]
    ):
        set_config.folder_path = text
        folder_path = Path(text)

        if set_config.subfolder:
            epub_files = [str(file.relative_to(folder_path)) for file in folder_path.rglob(f"*.{pattern}") if file.is_file()]
        else:
            epub_files = [file.name for file in folder_path.glob(f"*.{pattern}") if file.is_file()]

        epub_files.sort()

        combo_box_first_item_text = combo_box.itemText(0)
        combo_box_index = epub_files.index(set_config.options) if set_config.options in epub_files else -1

        combo_box.clear()
        combo_box.addItems([combo_box_first_item_text] + epub_files)
        combo_box.setCurrentIndex(combo_box_index + 1)

    @staticmethod
    def set_subfolder(
        set_config: EpubConfig | GlossaryConfig, 
        state: bool, 
        combo_box: QComboBox, 
        pattern: Literal['epub', 'json']
    ):
        set_config.subfolder = state
        Folder.read_files(set_config, set_config.folder_path, combo_box, pattern)

class SetWidget:


    @dataclass
    class SelectPathWidget:
        layout: QHBoxLayout
        path_label: QLabel
        path_line_edit: QLineEdit
        open_folder_button: QPushButton
        subfolder_check_box: QCheckBox

    @dataclass
    class CopyLineEdit:
        line_edit: QLineEdit
        action: QAction


    @staticmethod
    def files_combo_box(set_config: EpubConfig | GlossaryConfig):
        combo_box = QComboBox()
        combo_box.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        combo_box.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        combo_box.setEditable(True)
        combo_box.view().setTextElideMode(Qt.TextElideMode.ElideMiddle)
        combo_box.lineEdit().setReadOnly(True)
        combo_box.addItem("none")

        combo_box.currentTextChanged.connect(
            lambda text: set_file_options(set_config, text)
        )

        return combo_box

    @staticmethod
    def select_path_widget(
        default_path: str,
        default_subfolder: str
    ):
        layout = QHBoxLayout()

        path_label = QLabel()
        layout.addWidget(path_label)

        path_line_edit = QLineEdit()
        path_line_edit.setText(default_path)
        layout.addWidget(path_line_edit)

        open_folder_button = QPushButton()
        open_folder_button.setIcon(QIcon(icon.folder_open))
        layout.addWidget(open_folder_button)

        subfolder_check_box = QCheckBox()
        subfolder_check_box.setChecked(default_subfolder)
        layout.addWidget(subfolder_check_box)

        return SetWidget.SelectPathWidget(
            layout=layout,
            path_label=path_label,
            path_line_edit=path_line_edit,
            open_folder_button=open_folder_button,
            subfolder_check_box=subfolder_check_box
        )

    @staticmethod
    def frame():
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.HLine)
        frame.setFrameShadow(QFrame.Shadow.Sunken)

        return frame

    @staticmethod
    def copy_line_edit(text: str):
        line_edit = QLineEdit()

        line_edit.setText(text)
        line_edit.setReadOnly(True)
        line_edit.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        action = QAction(QIcon(icon.copy), "")
        action.triggered.connect(
            lambda: copy_to_clipboard(line_edit.text())
        )
        line_edit.addAction(action, QLineEdit.ActionPosition.TrailingPosition)

        line_edit_width = line_edit.fontMetrics().horizontalAdvance(line_edit.text())
        line_edit.setFixedWidth(line_edit_width + 35)

        return SetWidget.CopyLineEdit(
            line_edit=line_edit, 
            action=action
        )

    @staticmethod
    def push_button_icon(icon_path: str):
        button = QPushButton()
        button.setIcon(QIcon(icon_path))

        return button

class SetConnect:


    @staticmethod
    def select_path(
        set_config: EpubConfig | GlossaryConfig,
        widget: SetWidget.SelectPathWidget, 
        combo_box: QComboBox,
        pattern: Literal['epub', 'json']
    ):
        widget.path_line_edit.textChanged.connect(
            lambda text: Folder.read_files(set_config, text, combo_box, pattern)
        )
        widget.open_folder_button.clicked.connect(
            lambda: Folder.open(set_config, widget.path_line_edit.setText)
        )
        widget.subfolder_check_box.clicked.connect(
            lambda state: Folder.set_subfolder(set_config, state, combo_box, pattern)
        )


def set_language(
    widgets_set_language_func: list[Callable[[], None]],
    ui_language: str = ""
):
    if ui_language:
        language.load_language(ui_language)
        config.ui.language = ui_language

    for set_language_func in widgets_set_language_func:
        set_language_func()

def copy_to_clipboard(text: str):
    clipboard = QApplication.clipboard()
    clipboard.setText(text)

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