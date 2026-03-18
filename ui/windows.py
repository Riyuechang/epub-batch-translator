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
        self.setFocus()

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        self.line_edit_epub_path = QLineEdit()
        self.main_layout.addWidget(self.line_edit_epub_path)

        self.select_epub_layout = QHBoxLayout()
        self.main_layout.addLayout(self.select_epub_layout)

        self.combo_box_epub = QComboBox()
        self.combo_box_epub.addItem(language.front_page.select_all_epub_flies)
        self.select_epub_layout.addWidget(self.combo_box_epub, 1)

        self.button_open_folder = QPushButton()
        self.button_open_folder.setText(language.front_page.open_epub_folder)
        self.select_epub_layout.addWidget(self.button_open_folder)

        self.frame_line = QFrame()
        self.frame_line.setFrameShape(QFrame.Shape.HLine)
        self.frame_line.setFrameShadow(QFrame.Shadow.Sunken)
        self.main_layout.addWidget(self.frame_line)

        self.multiple_layout = QHBoxLayout()
        self.multiple_layout.setSpacing(10)
        self.main_layout.addLayout(self.multiple_layout)

        self.button_start = QPushButton()
        self.button_start.setText(language.front_page.start_processing)
        self.multiple_layout.addWidget(self.button_start, 1)

        self.multiple_layout.addSpacing(20)

        self.label_language = QLabel()
        self.label_language.setText(language.front_page.language)
        self.multiple_layout.addWidget(self.label_language)

        language_files = [dir.strip(".toml") for dir in os.listdir("./ui/language") if dir.endswith(".toml")]

        self.combo_box_language = QComboBox()
        self.combo_box_language.addItems(language_files)
        self.combo_box_language.setCurrentText(config.ui.language)
        self.multiple_layout.addWidget(self.combo_box_language)

        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs, 1)

        self.tab_llm_api = QWidget()
        self.tab_vllm = QWidget()

        self.tabs.addTab(self.tab_llm_api, language.llm_api.tab_name)
        self.tabs.addTab(self.tab_vllm, language.vllm.tab_name)

        self.text_edit_log = QPlainTextEdit()
        self.text_edit_log.setReadOnly(True)
        self.main_layout.addWidget(self.text_edit_log, 1)

        self.progress_bar_stage_progress = QProgressBar()
        self.progress_bar_stage_progress.setRange(0, 100)
        self.main_layout.addWidget(self.progress_bar_stage_progress)

        self.label_stage = QLabel()
        self.label_stage.setText(language.front_page.stage_none)
        self.label_stage.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.label_stage)

        self.main_container = QWidget()
        self.main_container.setLayout(self.main_layout)
        self.setCentralWidget(self.main_container)