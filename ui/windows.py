import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor, QActionGroup, QAction
from PyQt6.QtWidgets import (
    QMainWindow, 
    QApplication, 
    QVBoxLayout, 
    QHBoxLayout, 
    QGridLayout,
    QWidget, 
    QTabWidget, 
    QLabel, 
    QPushButton,
    QComboBox,
    QCheckBox,
    QLineEdit,
    QPlainTextEdit,
    QProgressBar,
    QSizePolicy
)

from config import config
from ui.content import language
from utils.qt_tools import (
    Epub,
    set_language, 
    set_frame, 
    set_copy_line_edit,
    reset_ui_message, 
    about_message
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("epub-batch-translator")
        self.resize(config.ui.width, config.ui.height)
        self.center()
        self.set_ui()

    def closeEvent(self, event):
        config.ui.width = self.width()
        config.ui.height = self.height()

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
        self.set_connect()

        set_language(self.widgets_set_language_func)
        Epub.read(config.epub.epub_folder_path, self.epub_combo_box)
    
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
        self.epub_path_line_edit.setText(config.epub.epub_folder_path)
        self.main_layout.addWidget(self.epub_path_line_edit)

        self.set_epub_widget_layout()

        self.line_frame = set_frame()
        self.main_layout.addWidget(self.line_frame)

        self.set_translator_layout()

        self.log_text_edit = QPlainTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.main_layout.addWidget(self.log_text_edit, 1)

        self.stage_progress_bar = QProgressBar()
        self.stage_progress_bar.setRange(0, 100)
        self.main_layout.addWidget(self.stage_progress_bar)

        self.stage_label = QLabel()
        self.stage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.stage_label)
        self.widgets_set_language_func.append(
            lambda: self.stage_label.setText(language.processing_stage.no_task)
        )

        self.line2_frame = set_frame()
        self.main_layout.addWidget(self.line2_frame)

        self.set_processing_layout()

    def set_epub_widget_layout(self):
        self.epub_widget_layout = QHBoxLayout()
        self.main_layout.addLayout(self.epub_widget_layout)

        self.open_folder_button = QPushButton()
        self.epub_widget_layout.addWidget(self.open_folder_button)
        self.widgets_set_language_func.append(
            lambda: self.open_folder_button.setText(language.epub_widget.open_epub_folder)
        )

        self.epub_combo_box = QComboBox()
        self.epub_combo_box.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        self.epub_combo_box.setEditable(True)
        self.epub_combo_box.view().setTextElideMode(Qt.TextElideMode.ElideMiddle)

        self.epub_combo_box_line_edit = self.epub_combo_box.lineEdit()
        self.epub_combo_box_line_edit.setReadOnly(True)
        self.epub_combo_box_line_edit.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.epub_combo_box.addItem("none")
        self.epub_widget_layout.addWidget(self.epub_combo_box, 1)
        self.widgets_set_language_func.append(
            lambda: self.epub_combo_box.setItemText(0, language.epub_widget.select_all_epub_flies)
        )

        self.subfolder_check_box = QCheckBox()
        self.subfolder_check_box.setChecked(config.epub.subfolder)
        self.epub_widget_layout.addWidget(self.subfolder_check_box)
        self.widgets_set_language_func.append(
            lambda: self.subfolder_check_box.setText(language.epub_widget.subfolder)
        )

    def set_translator_layout(self):
        self.translator_layout = QHBoxLayout()
        self.main_layout.addLayout(self.translator_layout, 3)

        self.set_prompt_layout()
        self.set_tabs()

    def set_prompt_layout(self):
        self.prompt_layout = QVBoxLayout()
        self.translator_layout.addLayout(self.prompt_layout, 1)

        self.set_translation_prompt_label_layout()

        self.translation_prompt_text_edit = QPlainTextEdit()
        self.prompt_layout.addWidget(self.translation_prompt_text_edit)
        self.widgets_set_language_func.append(
            lambda: self.translation_prompt_text_edit.setPlaceholderText(language.prompts_area.translation_prompt_example)
        )

        self.set_glossary_prompt_label_layout()

        self.glossary_prompt_line_edit = QLineEdit()
        self.prompt_layout.addWidget(self.glossary_prompt_line_edit)
        self.widgets_set_language_func.append(
            lambda: self.glossary_prompt_line_edit.setPlaceholderText(language.prompts_area.glossary_prompt_example)
        )

    def set_translation_prompt_label_layout(self):
        self.translation_prompt_label_layout = QHBoxLayout()
        self.prompt_layout.addLayout(self.translation_prompt_label_layout)

        self.translation_prompt_label = QLabel()
        self.translation_prompt_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.translation_prompt_label_layout.addWidget(self.translation_prompt_label)
        self.widgets_set_language_func.append(
            lambda: self.translation_prompt_label.setText(language.prompts_area.translation_prompt)
        )

        self.translation_prompt_label_layout.addSpacing(20)
        self.translation_prompt_label_layout.addStretch(1)

        self.content_tag_label = QLabel()
        self.translation_prompt_label_layout.addWidget(self.content_tag_label)
        self.widgets_set_language_func.append(
            lambda: self.content_tag_label.setText(language.prompts_area.translation_tag.content)
        )

        self.content_tag_line_edit, self.content_tag_copy_action = set_copy_line_edit(self, config.translation_tag.content)
        self.translation_prompt_label_layout.addWidget(self.content_tag_line_edit)

        self.glossary_tag_label = QLabel()
        self.translation_prompt_label_layout.addWidget(self.glossary_tag_label)
        self.widgets_set_language_func.append(
            lambda: self.glossary_tag_label.setText(language.prompts_area.translation_tag.glossary)
        )

        self.glossary_tag_line_edit, self.glossary_tag_copy_action = set_copy_line_edit(self, config.translation_tag.glossary)
        self.translation_prompt_label_layout.addWidget(self.glossary_tag_line_edit)

        self.history_tag_label = QLabel()
        self.translation_prompt_label_layout.addWidget(self.history_tag_label)
        self.widgets_set_language_func.append(
            lambda: self.history_tag_label.setText(language.prompts_area.translation_tag.history)
        )

        self.history_tag_line_edit, self.history_tag_copy_action = set_copy_line_edit(self, config.translation_tag.history)
        self.translation_prompt_label_layout.addWidget(self.history_tag_line_edit)

    def set_glossary_prompt_label_layout(self):
        self.glossary_prompt_label_layout = QHBoxLayout()
        self.prompt_layout.addLayout(self.glossary_prompt_label_layout)

        self.glossary_prompt_label = QLabel()
        self.glossary_prompt_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.glossary_prompt_label_layout.addWidget(self.glossary_prompt_label)
        self.widgets_set_language_func.append(
            lambda: self.glossary_prompt_label.setText(language.prompts_area.glossary_prompt)
        )

        self.glossary_prompt_label_layout.addSpacing(20)
        self.glossary_prompt_label_layout.addStretch(1)

        self.source_text_tag_label = QLabel()
        self.glossary_prompt_label_layout.addWidget(self.source_text_tag_label)
        self.widgets_set_language_func.append(
            lambda: self.source_text_tag_label.setText(language.prompts_area.glossary_tag.source_text)
        )

        self.source_text_tag_line_edit, self.source_text_tag_copy_action = set_copy_line_edit(self, config.glossary_tag.source_text)
        self.glossary_prompt_label_layout.addWidget(self.source_text_tag_line_edit)

        self.translation_tag_label = QLabel()
        self.glossary_prompt_label_layout.addWidget(self.translation_tag_label)
        self.widgets_set_language_func.append(
            lambda: self.translation_tag_label.setText(language.prompts_area.glossary_tag.translation)
        )

        self.translation_tag_line_edit, self.translation_tag_copy_action = set_copy_line_edit(self, config.glossary_tag.translation)
        self.glossary_prompt_label_layout.addWidget(self.translation_tag_line_edit)

        self.annotation_tag_label = QLabel()
        self.glossary_prompt_label_layout.addWidget(self.annotation_tag_label)
        self.widgets_set_language_func.append(
            lambda: self.annotation_tag_label.setText(language.prompts_area.glossary_tag.annotation)
        )

        self.annotation_tag_line_edit, self.annotation_tag_copy_action = set_copy_line_edit(self, config.glossary_tag.annotation)
        self.glossary_prompt_label_layout.addWidget(self.annotation_tag_line_edit)

    def set_tabs(self):
        self.tabs = QTabWidget()
        self.translator_layout.addWidget(self.tabs)

        self.llm_api_tab = QWidget()
        self.vllm_tab = QWidget()

        self.tabs.addTab(self.llm_api_tab, "none")
        self.tabs.addTab(self.vllm_tab, "none")

        self.widgets_set_language_func.append(
            lambda: self.tabs.setTabText(0, language.llm_api_tab.tab_name)
        )
        self.widgets_set_language_func.append(
            lambda: self.tabs.setTabText(1, language.vllm_tab.tab_name)
        )

    def set_processing_layout(self):
        self.processing_layout = QGridLayout()
        self.main_layout.addLayout(self.processing_layout)

        self.extract_content_button = QPushButton()
        self.processing_layout.addWidget(self.extract_content_button, 0, 0)
        self.widgets_set_language_func.append(
            lambda: self.extract_content_button.setText(language.processing_stage.extract_content)
        )

        self.calculate_similarity_button = QPushButton()
        self.processing_layout.addWidget(self.calculate_similarity_button, 0, 1)
        self.widgets_set_language_func.append(
            lambda: self.calculate_similarity_button.setText(language.processing_stage.calculate_similarity)
        )

        self.content_chunking_button = QPushButton()
        self.processing_layout.addWidget(self.content_chunking_button, 0, 2)
        self.widgets_set_language_func.append(
            lambda: self.content_chunking_button.setText(language.processing_stage.content_chunking)
        )

        self.translate_button = QPushButton()
        self.processing_layout.addWidget(self.translate_button, 0, 3)
        self.widgets_set_language_func.append(
            lambda: self.translate_button.setText(language.processing_stage.translate)
        )

        self.alignment_check_button = QPushButton()
        self.processing_layout.addWidget(self.alignment_check_button, 0, 4)
        self.widgets_set_language_func.append(
            lambda: self.alignment_check_button.setText(language.processing_stage.alignment_check)
        )

        self.replace_translation_button = QPushButton()
        self.processing_layout.addWidget(self.replace_translation_button, 0, 5)
        self.widgets_set_language_func.append(
            lambda: self.replace_translation_button.setText(language.processing_stage.replace_translation)
        )

        self.auto_processing_button = QPushButton()
        self.processing_layout.addWidget(self.auto_processing_button, 1, 0, 1, 4)
        self.widgets_set_language_func.append(
            lambda: self.auto_processing_button.setText(language.processing_stage.auto_processing)
        )

        self.select_translator_label = QLabel()
        self.select_translator_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.processing_layout.addWidget(self.select_translator_label, 1, 4, 1, 1)
        self.widgets_set_language_func.append(
            lambda: self.select_translator_label.setText(language.processing_stage.select_translator)
        )

        self.select_translator_combo_box = QComboBox()
        self.select_translator_combo_box.addItem("none")
        self.select_translator_combo_box.addItem("none")
        self.processing_layout.addWidget(self.select_translator_combo_box, 1, 5, 1, 1)
        self.widgets_set_language_func.append(
            lambda: self.select_translator_combo_box.setItemText(0, language.llm_api_tab.tab_name)
        )
        self.widgets_set_language_func.append(
            lambda: self.select_translator_combo_box.setItemText(1, language.vllm_tab.tab_name)
        )

    def set_connect(self):
        self.reset_ui_action.triggered.connect(reset_ui_message)
        self.language_group.triggered.connect(
            lambda ui_language: set_language(
                self.widgets_set_language_func,
                ui_language.text()
            )
        )
        self.about_action.triggered.connect(about_message)
        self.epub_path_line_edit.textChanged.connect(
            lambda text: Epub.read(text, self.epub_combo_box)
        )
        self.open_folder_button.clicked.connect(
            lambda: Epub.open_folder(self.epub_path_line_edit.setText)
        )
        self.subfolder_check_box.clicked.connect(
            lambda state: Epub.set_subfolder(state, self.epub_combo_box)
        )