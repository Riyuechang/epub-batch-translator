import os
from collections.abc import Callable

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
    QProgressBar
)

from config import config
from ui.image import icon
from ui.content import language
from utils.qt_tools import (
    Folder,
    ParameterFile,
    SetWidget,
    SetConnect,
    Message, 
    set_language, 
    reset_ui
)
from utils.common_tools import set_dynamic_glossary_state

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
        self.widgets_set_language_func: list[Callable[[], None]] = []

        self.setFocus()
        self.set_menu()
        self.set_main_layout()
        self.set_connect()

        Folder.read_files(config.epub.folder_path, config.epub, self.epub_combo_box, "epub")
        Folder.read_files(config.glossary.folder_path, config.glossary, self.glossary_combo_box, "json")
        ParameterFile.load_combo_box(config.prompt_parameter, self.prompt_parameter_file_widget.file_combo_box)

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

        self.set_epub_widget_layout()

        self.epub_widget_layout_frame = SetWidget.frame()
        self.main_layout.addWidget(self.epub_widget_layout_frame)

        self.set_glossary_widget_layout()

        self.glossary_widget_layout_frame = SetWidget.frame()
        self.main_layout.addWidget(self.glossary_widget_layout_frame)

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

        self.processing_layout_frame = SetWidget.frame()
        self.main_layout.addWidget(self.processing_layout_frame)

        self.set_processing_layout()

    def set_epub_widget_layout(self):
        self.epub_folder_widget = SetWidget.select_path_widget(config.epub.folder_path, config.epub.subfolder)
        self.main_layout.addLayout(self.epub_folder_widget.layout)
        self.widgets_set_language_func.append(
            lambda: self.epub_folder_widget.path_label.setText(language.epub_widget.folder_path)
        )
        self.widgets_set_language_func.append(
            lambda: self.epub_folder_widget.subfolder_check_box.setText(language.folder_options.subfolder)
        )

        self.epub_combo_box = SetWidget.files_combo_box(config.epub)
        self.main_layout.addWidget(self.epub_combo_box)
        self.widgets_set_language_func.append(
            lambda: self.epub_combo_box.setItemText(0, language.epub_widget.select_all_epub_files)
        )

    def set_glossary_widget_layout(self):
        self.glossary_folder_widget = SetWidget.select_path_widget(config.glossary.folder_path, config.glossary.subfolder)
        self.main_layout.addLayout(self.glossary_folder_widget.layout)
        self.widgets_set_language_func.append(
            lambda: self.glossary_folder_widget.path_label.setText(language.glossary_widget.folder_path)
        )
        self.widgets_set_language_func.append(
            lambda: self.glossary_folder_widget.subfolder_check_box.setText(language.folder_options.subfolder)
        )

        self.glossary_combo_box = SetWidget.files_combo_box(config.glossary)
        self.main_layout.addWidget(self.glossary_combo_box)
        self.widgets_set_language_func.append(
            lambda: self.glossary_combo_box.setItemText(0, language.glossary_widget.auto_glossary)
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

        self.set_prompt_options_layout()

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

        self.content_tag_line_edit = SetWidget.copy_line_edit(config.translation_tag.content)
        self.translation_prompt_label_layout.addWidget(self.content_tag_line_edit.line_edit)

        self.glossary_tag_label = QLabel()
        self.translation_prompt_label_layout.addWidget(self.glossary_tag_label)
        self.widgets_set_language_func.append(
            lambda: self.glossary_tag_label.setText(language.prompts_area.translation_tag.glossary)
        )

        self.glossary_tag_line_edit = SetWidget.copy_line_edit(config.translation_tag.glossary)
        self.translation_prompt_label_layout.addWidget(self.glossary_tag_line_edit.line_edit)

        self.history_tag_label = QLabel()
        self.translation_prompt_label_layout.addWidget(self.history_tag_label)
        self.widgets_set_language_func.append(
            lambda: self.history_tag_label.setText(language.prompts_area.translation_tag.history)
        )

        self.history_tag_line_edit = SetWidget.copy_line_edit(config.translation_tag.history)
        self.translation_prompt_label_layout.addWidget(self.history_tag_line_edit.line_edit)

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

        self.source_text_tag_line_edit = SetWidget.copy_line_edit(config.glossary_tag.source_text)
        self.glossary_prompt_label_layout.addWidget(self.source_text_tag_line_edit.line_edit)

        self.translation_tag_label = QLabel()
        self.glossary_prompt_label_layout.addWidget(self.translation_tag_label)
        self.widgets_set_language_func.append(
            lambda: self.translation_tag_label.setText(language.prompts_area.glossary_tag.translation)
        )

        self.translation_tag_line_edit = SetWidget.copy_line_edit(config.glossary_tag.translation)
        self.glossary_prompt_label_layout.addWidget(self.translation_tag_line_edit.line_edit)

        self.annotation_tag_label = QLabel()
        self.glossary_prompt_label_layout.addWidget(self.annotation_tag_label)
        self.widgets_set_language_func.append(
            lambda: self.annotation_tag_label.setText(language.prompts_area.glossary_tag.annotation)
        )

        self.annotation_tag_line_edit = SetWidget.copy_line_edit(config.glossary_tag.annotation)
        self.glossary_prompt_label_layout.addWidget(self.annotation_tag_line_edit.line_edit)

    def set_prompt_options_layout(self):
        self.prompt_parameter_file_widget = SetWidget.set_parameter_file_widget(
            config.prompt_parameter,
            lambda: ParameterFile.PromptParameter(
                translation_prompt=self.translation_prompt_text_edit.toPlainText(),
                glossary_prompt=self.glossary_prompt_line_edit.text()
            ),
            ParameterFile.PromptParameterSetFunc(
                translation_prompt=self.translation_prompt_text_edit.setPlainText,
                glossary_prompt=self.glossary_prompt_line_edit.setText
            )
        )
        self.prompt_layout.addLayout(self.prompt_parameter_file_widget.layout)
        self.widgets_set_language_func.append(
            lambda: self.prompt_parameter_file_widget.file_label.setText(language.prompt_parameter.parameter_file)
        )
        self.widgets_set_language_func.append(
            lambda: self.prompt_parameter_file_widget.file_combo_box.lineEdit().setPlaceholderText(language.prompt_parameter.parameter_file_example)
        )

        self.prompt_parameter_file_widget.layout.addStretch(1)

        self.dynamic_glossary_check_box = QCheckBox()
        self.dynamic_glossary_check_box.setChecked(config.prompt_options.dynamic_glossary)
        self.prompt_parameter_file_widget.layout.addWidget(self.dynamic_glossary_check_box)
        self.widgets_set_language_func.append(
            lambda: self.dynamic_glossary_check_box.setText(language.prompt_options.dynamic_glossary)
        )

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
        self.reset_ui_action.triggered.connect(
            lambda: Message.warning_message(language.reset_ui_message, reset_ui)
        )
        self.language_group.triggered.connect(
            lambda ui_language: set_language(
                self.widgets_set_language_func,
                ui_language.text()
            )
        )
        self.about_action.triggered.connect(Message.about_message)
        SetConnect.select_path(self.epub_folder_widget, config.epub, self.epub_combo_box, "epub")
        SetConnect.select_path(self.glossary_folder_widget, config.glossary, self.glossary_combo_box, "json")
        self.dynamic_glossary_check_box.clicked.connect(set_dynamic_glossary_state)