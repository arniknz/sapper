from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sapper")
        b = QPushButton("Click!")

        self.setCentralWidget(b)

app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec()