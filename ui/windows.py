import os

from PyQt6 import QtCore
from PyQt6.QtGui import QCursor, QActionGroup, QAction
from PyQt6.QtWidgets import (
    QMainWindow, 
    QApplication, 
    QVBoxLayout, 
    QHBoxLayout, 
    QWidget, 
    QTabWidget, 
    QLabel, 
    QPushButton,
    QComboBox,
    QLineEdit,
    QPlainTextEdit,
    QProgressBar
)

from config import config
from ui.content import language
from utils.qt_tools import set_language, set_frame, reset_ui_message, about_message


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("epub-batch-translator")
        self.resize(config.ui.width, config.ui.height)
        self.center()
        self.set_ui()

    def resizeEvent(self, event):
        window_width = self.width()
        window_height = self.height()

        if window_width != config.ui.width or window_height != config.ui.height:
            config.ui.width = window_width
            config.ui.height = window_height
            config.save_user_config()

    def center(self):
        screen = QApplication.screenAt(QCursor.pos())

        if screen is None:
            screen = QApplication.primaryScreen()

        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()

        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

    def set_ui(self):
        self.widgets_set_language_func = []

        self.setFocus()
        self.set_menu()
        self.set_main_layout()

        set_language(self.widgets_set_language_func)
    
    def set_menu(self):
        self.menu_bar = self.menuBar()

        self.set_settings_menu()
        self.set_language_menu()
        self.set_about_menu()

    def set_settings_menu(self):
        self.settings_menu = self.menu_bar.addMenu("none")
        self.widgets_set_language_func.append(
            lambda: self.settings_menu.setTitle(language.menu_bar.settings_menu.menu_name)
        )

        self.reset_ui_action = QAction()
        self.reset_ui_action.triggered.connect(reset_ui_message)
        self.settings_menu.addAction(self.reset_ui_action)
        self.widgets_set_language_func.append(
            lambda: self.reset_ui_action.setText(language.menu_bar.settings_menu.reset_ui)
        )

    def set_language_menu(self):
        self.language_menu = self.menu_bar.addMenu("none")
        self.widgets_set_language_func.append(
            lambda: self.language_menu.setTitle(language.menu_bar.language)
        )

        self.language_group = QActionGroup(self)
        self.language_group.triggered.connect(
            lambda ui_language: set_language(
                self.widgets_set_language_func,
                ui_language.text()
            )
        )

        self.language_actions: dict[str, QAction] = {dir.strip(".toml"): "" for dir in os.listdir("./ui/language") if dir.endswith(".toml")}
        for language_name in self.language_actions:
            action = QAction(language_name)
            action.setCheckable(True)
            self.language_group.addAction(action)
            self.language_menu.addAction(action)
            self.language_actions[language_name] = action

        self.language_actions[config.ui.language].setChecked(True)

    def set_about_menu(self):
        self.about_action = self.menu_bar.addAction("none")
        self.about_action.triggered.connect(about_message)
        self.widgets_set_language_func.append(
            lambda: self.about_action.setText(language.menu_bar.about)
        )

    def set_main_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.main_container = QWidget()
        self.main_container.setLayout(self.main_layout)
        self.setCentralWidget(self.main_container)

        self.epub_path_line_edit = QLineEdit()
        self.epub_path_line_edit.setText(config.epub_folder_path)
        self.main_layout.addWidget(self.epub_path_line_edit)

        self.set_multiple_layout()

        self.line_frame = set_frame()
        self.main_layout.addWidget(self.line_frame)

        self.set_tabs()

        self.log_text_edit = QPlainTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.main_layout.addWidget(self.log_text_edit, 1)

        self.stage_progress_bar = QProgressBar()
        self.stage_progress_bar.setRange(0, 100)
        self.main_layout.addWidget(self.stage_progress_bar)

        self.stage_label = QLabel()
        self.stage_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.stage_label)
        self.widgets_set_language_func.append(
            lambda: self.stage_label.setText(language.processing_stage.no_task)
        )

        self.line2_frame = set_frame()
        self.main_layout.addWidget(self.line2_frame)

        self.set_processing_layout()

        self.auto_processing_button = QPushButton()
        self.main_layout.addWidget(self.auto_processing_button)
        self.widgets_set_language_func.append(
            lambda: self.auto_processing_button.setText(language.processing_stage.auto_processing)
        )

    def set_multiple_layout(self):
        self.multiple_layout = QHBoxLayout()
        self.main_layout.addLayout(self.multiple_layout)

        self.open_folder_button = QPushButton()
        self.multiple_layout.addWidget(self.open_folder_button)
        self.widgets_set_language_func.append(
            lambda: self.open_folder_button.setText(language.main_page.open_epub_folder)
        )

        self.epub_combo_box = QComboBox()
        self.epub_combo_box.addItem("none")
        self.multiple_layout.addWidget(self.epub_combo_box, 1)
        self.widgets_set_language_func.append(
            lambda: self.epub_combo_box.setItemText(0, language.main_page.select_all_epub_flies)
        )

    def set_tabs(self):
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs, 3)

        self.prompt_tab = QWidget()
        self.llm_api_tab = QWidget()
        self.vllm_tab = QWidget()

        self.tabs.addTab(self.prompt_tab, "none")
        self.tabs.addTab(self.llm_api_tab, "none")
        self.tabs.addTab(self.vllm_tab, "none")

        self.widgets_set_language_func.append(
            lambda: self.tabs.setTabText(0, language.prompt_tab.tab_name)
        )
        self.widgets_set_language_func.append(
            lambda: self.tabs.setTabText(1, language.llm_api_tab.tab_name)
        )
        self.widgets_set_language_func.append(
            lambda: self.tabs.setTabText(2, language.vllm_tab.tab_name)
        )

    def set_processing_layout(self):
        self.processing_layout = QHBoxLayout()
        self.main_layout.addLayout(self.processing_layout)

        self.extract_content_button = QPushButton()
        self.processing_layout.addWidget(self.extract_content_button)
        self.widgets_set_language_func.append(
            lambda: self.extract_content_button.setText(language.processing_stage.extract_content)
        )

        self.calculate_similarity_button = QPushButton()
        self.processing_layout.addWidget(self.calculate_similarity_button)
        self.widgets_set_language_func.append(
            lambda: self.calculate_similarity_button.setText(language.processing_stage.calculate_similarity)
        )

        self.content_chunking_button = QPushButton()
        self.processing_layout.addWidget(self.content_chunking_button)
        self.widgets_set_language_func.append(
            lambda: self.content_chunking_button.setText(language.processing_stage.content_chunking)
        )

        self.translate_button = QPushButton()
        self.processing_layout.addWidget(self.translate_button)
        self.widgets_set_language_func.append(
            lambda: self.translate_button.setText(language.processing_stage.translate)
        )

        self.alignment_check_button = QPushButton()
        self.processing_layout.addWidget(self.alignment_check_button)
        self.widgets_set_language_func.append(
            lambda: self.alignment_check_button.setText(language.processing_stage.alignment_check)
        )

        self.replace_translation_button = QPushButton()
        self.processing_layout.addWidget(self.replace_translation_button)
        self.widgets_set_language_func.append(
            lambda: self.replace_translation_button.setText(language.processing_stage.replace_translation)
        )