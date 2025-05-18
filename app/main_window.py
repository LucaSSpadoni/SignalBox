from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QApplication, QVBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(200, 200, 800, 500)
        self.center()
        self.titleLabel("SignalBox")
        self.show()

    def center(self):
        frame = self.frameGeometry()
        centerPoint = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(centerPoint)
        self.move(frame.topLeft())

    def titleLabel(self, text):
        # Creare central widget
        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)

        # Create title label
        titleLabel = QLabel(text, self)
        titleLabel.setFont(QFont("Arial", 30))
        titleLabel.setStyleSheet("color: purple; font-weight: bold;")
        titleLabel.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 40, 0, 0)  # left, top, right, bottom

        # Add layout and set central widget
        layout.addWidget(titleLabel)
        layout.addStretch(300)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        