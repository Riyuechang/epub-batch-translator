import sys
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from collections.abc import Callable
from typing import Literal

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import QProcess, Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog, 
    QFrame, 
    QLabel,
    QMessageBox, 
    QPushButton,
    QCheckBox,
    QComboBox,
    QLineEdit,
    QSizePolicy,
    QSystemTrayIcon
)

from config import config, FolderConfig, ParameterFileConfig
from ui.image import icon
from ui.content import language, WarningMessage
from utils.common_tools import remove_user_config, set_file_options, get_list_index


class Folder:
    @staticmethod
    def open(
        set_text_func: Callable[[], None], 
        set_config: FolderConfig, 
        combo_box: QComboBox, 
        pattern: Literal["epub", "json"]
    ):
        folder_path = QFileDialog.getExistingDirectory(directory=set_config.folder_path)

        if folder_path:
            set_text_func(folder_path)
            set_config.folder_path = folder_path
            Folder.read_files(folder_path, set_config, combo_box, pattern)

    @staticmethod
    def read_files(
        path: str, 
        set_config: FolderConfig, 
        combo_box: QComboBox, 
        pattern: Literal["epub", "json"]
    ):
        folder_path = Path(path)

        if set_config.subfolder:
            files = [str(file.relative_to(folder_path)) for file in folder_path.rglob(f"*.{pattern}") if file.is_file()]
        else:
            files = [file.name for file in folder_path.glob(f"*.{pattern}") if file.is_file()]

        files.sort()

        combo_box_first_item_text = combo_box.itemText(0)
        combo_box_index = get_list_index(files, set_config.options)

        combo_box.clear()
        combo_box.addItems([combo_box_first_item_text] + files)
        combo_box.setCurrentIndex(combo_box_index + 1)

    @staticmethod
    def set_subfolder(
        state: bool, 
        set_config: FolderConfig, 
        combo_box: QComboBox, 
        pattern: Literal['epub', 'json']
    ):
        set_config.subfolder = state
        Folder.read_files(set_config.folder_path, set_config, combo_box, pattern)

class ParameterFile:
    @dataclass
    class PromptParameter:
        translation_prompt: str
        glossary_prompt: str

    @dataclass
    class PromptParameterSetFunc:
        translation_prompt: Callable[[str | None], None]
        glossary_prompt: Callable[[str | None], None]

    @staticmethod
    def load_combo_box(
        set_config: ParameterFileConfig, 
        combo_box: QComboBox
    ):
        files = [file.stem for file in Path(set_config.folder_path).glob(f"*.json") if file.is_file()]
        files.sort()

        combo_box_index = get_list_index(files, set_config.options)

        combo_box.clear()
        combo_box.addItems(files)
        combo_box.setCurrentIndex(0 if combo_box_index == -1 else combo_box_index)

    @staticmethod
    def save(
        set_config: ParameterFileConfig,
        combo_box: QComboBox,
        dataclass_obj: object
    ):
        file_name = combo_box.currentText()
        
        if file_name == "":
            return
        
        set_config.options = file_name

        folder_path = Path(set_config.folder_path)
        folder_path.mkdir(parents=True, exist_ok=True)

        parameter_file = folder_path.joinpath(f"{file_name}.json")

        if parameter_file.is_file():
            result = Message.warning_message(language.save_message.warning, lambda: None)

            if not result:
                return

        with parameter_file.open('w', encoding='utf-8') as file:
            json.dump(asdict(dataclass_obj), file, indent=4, ensure_ascii=False)

        ParameterFile.load_combo_box(set_config, combo_box)
        system_tray_icon = QSystemTrayIcon(QApplication.instance())
        system_tray_icon.setIcon(QIcon(icon.app))
        system_tray_icon.show()
        system_tray_icon.showMessage(
            config.ui.window_title,
            language.save_message.system.message,
            QSystemTrayIcon.MessageIcon.Warning,
            1000
        )

    @staticmethod
    def delete(
        set_config: ParameterFileConfig,
        combo_box: QComboBox
    ):
        file_name = combo_box.currentText()

        if file_name == "":
            return

        result = Message.warning_message(language.delete_warning_message, lambda: None)

        if not result:
            return

        Path(set_config.folder_path, f"{file_name}.json").unlink()
        ParameterFile.load_combo_box(set_config, combo_box)

    @staticmethod
    def load_parameter(
        file_name: str, 
        set_config: ParameterFileConfig,
        parameter_set_func_dataclass: object
    ):
        file_path = Path(set_config.folder_path, f"{file_name}.json")

        if not file_path.is_file():
            return

        set_config.options = file_name

        with file_path.open("r", encoding="utf-8") as file:
            parameter_data: dict[str, str] = json.load(file)

        parameter_set_func_dict = asdict(parameter_set_func_dataclass)

        for key, value in parameter_data.items():
            parameter_set_func_dict[key](value)

class SetWidget:
    @dataclass
    class SelectPathWidget:
        layout: QHBoxLayout
        file_combo_box: QComboBox
        path_label: QLabel
        path_line_edit: QLineEdit
        refresh_button: QPushButton
        open_folder_button: QPushButton
        subfolder_check_box: QCheckBox

    @dataclass
    class CopyLineEdit:
        line_edit: QLineEdit
        action: QAction

    @dataclass
    class ParameterFileWidget:
        layout: QHBoxLayout | QVBoxLayout
        file_label: QLabel
        file_combo_box: QComboBox
        refresh_button: QPushButton
        save_button: QPushButton
        delete_button: QPushButton


    @staticmethod
    def select_path_widget(
        set_config: FolderConfig,
        pattern: Literal['epub', 'json']
    ):
        layout = QHBoxLayout()

        path_label = QLabel()
        layout.addWidget(path_label)

        path_line_edit = QLineEdit()
        path_line_edit.setText(set_config.folder_path)
        layout.addWidget(path_line_edit)

        refresh_button = QPushButton()
        refresh_button.setIcon(QIcon(icon.refresh))
        layout.addWidget(refresh_button)

        open_folder_button = QPushButton()
        open_folder_button.setIcon(QIcon(icon.folder_open))
        layout.addWidget(open_folder_button)

        subfolder_check_box = QCheckBox()
        subfolder_check_box.setChecked(set_config.subfolder)
        layout.addWidget(subfolder_check_box)

        file_combo_box = QComboBox()
        file_combo_box.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        file_combo_box.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        file_combo_box.setEditable(True)
        file_combo_box.view().setTextElideMode(Qt.TextElideMode.ElideMiddle)
        file_combo_box.lineEdit().setReadOnly(True)
        file_combo_box.addItem("none")

        file_combo_box.currentTextChanged.connect(
            lambda text: set_file_options(text, file_combo_box.currentIndex, set_config)
        )
        path_line_edit.returnPressed.connect(
            lambda: Folder.read_files(path_line_edit.text(), set_config, file_combo_box, pattern)
        )
        refresh_button.clicked.connect(
            lambda: Folder.read_files(path_line_edit.text(), set_config, file_combo_box, pattern)
        )
        open_folder_button.clicked.connect(
            lambda: Folder.open(path_line_edit.setText, set_config, file_combo_box, pattern)
        )
        subfolder_check_box.clicked.connect(
            lambda state: Folder.set_subfolder(state, set_config, file_combo_box, pattern)
        )

        return SetWidget.SelectPathWidget(
            layout=layout,
            file_combo_box=file_combo_box,
            path_label=path_label,
            path_line_edit=path_line_edit,
            refresh_button=refresh_button,
            open_folder_button=open_folder_button,
            subfolder_check_box=subfolder_check_box
        )

    @staticmethod
    def set_parameter_file_widget(
        set_config: ParameterFileConfig,
        parameter_get_dataclass_func: Callable[[], object],
        parameter_set_func_dataclass: object,
        two_layers: bool = False
    ):
        layout = QHBoxLayout()

        file_label = QLabel()
        layout.addWidget(file_label)

        if two_layers:
            layout.addStretch(1)

        file_combo_box = QComboBox()
        file_combo_box.setEditable(True)
        file_combo_box.view().setTextElideMode(Qt.TextElideMode.ElideMiddle)
        file_combo_box.lineEdit().returnPressed.disconnect()
        file_combo_box.currentTextChanged.connect(
            lambda text: ParameterFile.load_parameter(text, set_config, parameter_set_func_dataclass)
        )

        if two_layers:
            second_layout = QVBoxLayout()
            second_layout.addLayout(layout)
            second_layout.addWidget(file_combo_box)
        else:
            layout.addWidget(file_combo_box, 1)

        refresh_button = SetWidget.push_button_icon(icon.refresh)
        refresh_button.clicked.connect(
            lambda: ParameterFile.load_combo_box(set_config, file_combo_box)
        )
        layout.addWidget(refresh_button)

        save_button = SetWidget.push_button_icon(icon.save)
        save_button.clicked.connect(
            lambda: ParameterFile.save(set_config, file_combo_box, parameter_get_dataclass_func())
        )
        layout.addWidget(save_button)

        delete_button = SetWidget.push_button_icon(icon.delete)
        delete_button.clicked.connect(
            lambda: ParameterFile.delete(set_config, file_combo_box)
        )
        layout.addWidget(delete_button)

        return SetWidget.ParameterFileWidget(
            layout=second_layout if two_layers else layout,
            file_label=file_label,
            file_combo_box=file_combo_box,
            refresh_button=refresh_button,
            save_button=save_button,
            delete_button=delete_button
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

class Message:
    @staticmethod
    def warning_message(
        language: WarningMessage,
        trigger_func: Callable[[], None]
    ):
        message_box = QMessageBox()

        message_box.setIcon(QMessageBox.Icon.Warning)
        message_box.setWindowTitle(language.title)
        message_box.setText(language.message)

        action_button = message_box.addButton(language.confirm, QMessageBox.ButtonRole.ActionRole)
        reject_button = message_box.addButton(language.cancel, QMessageBox.ButtonRole.RejectRole)

        message_box.setDefaultButton(reject_button)
        message_box.exec()

        clicked_button = message_box.clickedButton()

        if clicked_button == action_button:
            trigger_func()
            return True
        
        return False

    @staticmethod
    def about_message():
        message_box = QMessageBox()

        message_box.setWindowTitle(language.about_message.title)
        message_box.setText(language.about_message.message)
        message_box.setTextFormat(Qt.TextFormat.RichText)
        message_box.addButton(language.about_message.confirm, QMessageBox.ButtonRole.AcceptRole)
        message_box.exec()


def set_language(
    widgets_set_language_func: list[Callable[[], None]],
    ui_language: str = ""
):
    if ui_language:
        language.load_language(ui_language)
        config.ui.language = ui_language

    for set_language_func in widgets_set_language_func:
        set_language_func()

def reset_ui():
    QApplication.quit()
    remove_user_config()
    QProcess.startDetached(sys.executable, sys.argv)

def copy_to_clipboard(text: str):
    clipboard = QApplication.clipboard()
    clipboard.setText(text)