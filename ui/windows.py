import os

from PyQt6 import QtCore
from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (
    QMainWindow, 
    QApplication, 
    QVBoxLayout, 
    QHBoxLayout, 
    QFrame,
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
from utils import qt_tools


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("epub-batch-translator")
        self.resize(config.ui.width, config.ui.height)
        self.center()
        self.set_ui()

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

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.epub_path_line_edit = QLineEdit()
        self.epub_path_line_edit.setText(config.epub_folder_path)
        self.main_layout.addWidget(self.epub_path_line_edit)

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

        self.multiple_layout.addSpacing(20)

        self.language_label = QLabel()
        self.multiple_layout.addWidget(self.language_label)
        self.widgets_set_language_func.append(
            lambda: self.language_label.setText(language.main_page.language)
        )

        language_files = [dir.strip(".toml") for dir in os.listdir("./ui/language") if dir.endswith(".toml")]

        self.language_combo_box = QComboBox()
        self.language_combo_box.addItems(language_files)
        self.language_combo_box.setCurrentText(config.ui.language)
        self.language_combo_box.currentTextChanged.connect(
            lambda ui_language: qt_tools.set_language(
                self.widgets_set_language_func,
                ui_language
            )
        )
        self.multiple_layout.addWidget(self.language_combo_box)

        self.line_frame = QFrame()
        self.line_frame.setFrameShape(QFrame.Shape.HLine)
        self.line_frame.setFrameShadow(QFrame.Shadow.Sunken)
        self.main_layout.addWidget(self.line_frame)

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

        self.line2_frame = QFrame()
        self.line2_frame.setFrameShape(QFrame.Shape.HLine)
        self.line2_frame.setFrameShadow(QFrame.Shadow.Sunken)
        self.main_layout.addWidget(self.line2_frame)

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

        self.auto_processing_button = QPushButton()
        self.main_layout.addWidget(self.auto_processing_button)
        self.widgets_set_language_func.append(
            lambda: self.auto_processing_button.setText(language.processing_stage.auto_processing)
        )

        self.main_container = QWidget()
        self.main_container.setLayout(self.main_layout)
        self.setCentralWidget(self.main_container)

        qt_tools.set_language(self.widgets_set_language_func)