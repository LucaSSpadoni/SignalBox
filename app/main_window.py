from PySide6.QtWidgets import (QMainWindow, QLabel, QWidget, QApplication, QVBoxLayout, QPushButton
                                , QStackedWidget, QHBoxLayout)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QSizePolicy
from app.spectrogram_page import SpectrogramPage
from app.equalizer_page import EqualizerPage
from app.pitch_shifter_page import PitchShifterPage
from app.real_time_visualizer_page import RealTimePage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # set main window properties
        self.setWindowTitle("Main Window")
        self.setGeometry(200, 200, 800, 500)
        self.center()
        self.setStyleSheet("background-color: #1b1b2f;")
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
        titleLabel.setStyleSheet("color: #8e44ad; font-weight: bold;")
        return titleLabel
    
    def createStack(self):
        stack = QStackedWidget()
        stack.addWidget(SpectrogramPage())
        stack.addWidget(RealTimePage())
        stack.addWidget(EqualizerPage())
        stack.addWidget(PitchShifterPage())
        return stack

    def createNavBar(self):
        # create nav bar and add buttons
        navBar = QWidget()
        navLayout = QHBoxLayout()

        navBar.setStyleSheet("background-color:	#242436;")
        navBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        navLayout.addWidget(self.titleLabel("SignalBox"), alignment=Qt.AlignLeft)

        for i, page in enumerate(["Static Visualizer", "Real-time Visualizer", "Equalizer", "Pitch Shifter"]):
            button = QPushButton(page)
            button.setStyleSheet("color: #e6e6f0; font-weight: bold;")
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            button.clicked.connect(lambda _, x=i: self.stack.setCurrentIndex(x))
            navLayout.addWidget(button)

        navBar.setLayout(navLayout)
        return navBar

    def buildUI(self):
        # create container for nav bar and stack
        container = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        navBar = self.createNavBar()
        self.stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout.addWidget(navBar)
        layout.addWidget(self.stack)

        container.setLayout(layout)
        return container
        