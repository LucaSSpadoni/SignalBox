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
        self.stack = self.createStack()
        self.setCentralWidget(self.buildUI())

        # show window
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
    
    def buildPitchShifterPage(self):
        page = QWidget()
        layout = QVBoxLayout()

        # label logic
        label = QLabel("Pitch Shifter", self)
        label.setFont(QFont("Arial", 30))
        label.setStyleSheet("color: purple; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Add pitch shifter controls here
        page.setLayout(layout)
        return page
    
    def buildEqualizerPage(self):
        page = QWidget()
        layout = QVBoxLayout()

        #label logic
        label = QLabel("Equalizer", self)
        label.setFont(QFont("Arial", 30))
        label.setStyleSheet("color: purple; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Add equalizer controls here
        page.setLayout(layout)
        return page
    
    def buildSpectrogramPage(self):
        page = QWidget()
        layout = QVBoxLayout()

        # label logic
        label = QLabel("Spectrogram Visualizer", self)
        label.setFont(QFont("Arial", 30))
        label.setStyleSheet("color: purple; font-weight: bold;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Add spectrogram controls here
        page.setLayout(layout)
        return page
    
    def createStack(self):
        stack = QStackedWidget()
        stack.addWidget(self.buildSpectrogramPage())
        stack.addWidget(self.buildEqualizerPage())
        stack.addWidget(self.buildPitchShifterPage())
        return stack

    def createNavBar(self):
        # create nav bar and add buttons
        navBar = QWidget()
        navLayout = QHBoxLayout()
        navLayout.setContentsMargins(10, 10, 10, 10)
        navBar.setStyleSheet("background-color: black;")

        navLayout.addWidget(self.titleLabel("SignalBox"), alignment=Qt.AlignLeft)

        for i, page in enumerate(["Spectrogram Visualizer", "Equalizer", "Pitch Shifter"]):
            button = QPushButton(page)
            button.setStyleSheet("color: purple; font-weight: bold;")
            button.clicked.connect(lambda _, x=i: self.stack.setCurrentIndex(x))
            navLayout.addWidget(button)

        navBar.setLayout(navLayout)
        return navBar

    def buildUI(self):
        # create container for nav bar and stack
        container = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.createNavBar())
        layout.addWidget(self.stack)
        container.setLayout(layout)
        return container
        