from PySide6.QtWidgets import (QMainWindow, QLabel, QWidget, QApplication, QVBoxLayout, QPushButton
                                , QStackedWidget, QHBoxLayout)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Slot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # set main window properties
        self.setWindowTitle("Main Window")
        self.setGeometry(200, 200, 800, 500)
        self.center()
        self.setStyleSheet("background-color: grey;")
        self.setCentralWidget(self.buildUI())
        self.show()

    def center(self):
        frame = self.frameGeometry()
        centerPoint = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(centerPoint)
        self.move(frame.topLeft())

    def titleLabel(self, text):
        # Create title label
        titleLabel = QLabel(text, self)
        titleLabel.setFont(QFont("Arial", 30))
        titleLabel.setStyleSheet("color: purple; font-weight: bold;")
        return titleLabel
    
    def buildPage(self, titleText):
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)
        return page
    
    def createNavBar(self):
        # create nav bar and add buttons
        navBar = QWidget()
        navLayout = QHBoxLayout()
        navLayout.setContentsMargins(10, 10, 10, 10)
        #navBar.setSpacing(10)
        navBar.setStyleSheet("background-color: black;")

        navLayout.addWidget(self.titleLabel("SignalBox"), alignment=Qt.AlignLeft)

        for i, page in enumerate(["Spectrogram Visualizer", "Equalizer", "Pitch Shifter"]):
            button = QPushButton(page)
            button.setStyleSheet("color: purple; font-weight: bold;")
            button.clicked.connect(lambda _, x=i: self.stack.setCurrentIndex(x))
            navLayout.addWidget(button)

        navBar.setLayout(navLayout)
        return navBar
    
    def createStack(self):
        stack = QStackedWidget()
        stack.addWidget(self.buildPage("Spectrogram Visualizer"))
        stack.addWidget(self.buildPage("Equalizer"))
        stack.addWidget(self.buildPage("Pitch Shifter"))
        return stack

    def buildUI(self):
        # create container for nav bar and stack
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.createNavBar())
        layout.addWidget(self.createStack())
        container.setLayout(layout)
        return container
        