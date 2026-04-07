import sys

from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication

from ui.windows import MainWindow


app = QApplication(sys.argv)

font_id = QFontDatabase.addApplicationFont("./ui/font/MapleMonoNormalNL-CN-Regular.ttf")
font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
font = QFont(font_family, 12)

app.setFont(font)

window = MainWindow()
window.show()

sys.exit(app.exec())