from PySide6.QtWidgets import (QMainWindow, QLabel, QWidget, QApplication, QVBoxLayout, QPushButton
                                , QStackedWidget, QHBoxLayout)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QSizePolicy

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # set main window properties
        self.setWindowTitle("Main Window")
        self.setGeometry(200, 200, 800, 500)
        self.center()
        self.setStyleSheet("background-color: #71797E;")
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
    
    def buildPitchShifterPage(self):
        page = QWidget()
        layout = QHBoxLayout()

        # Left side
        spectrogramWidget = QWidget()
        spectrogramLayout = QHBoxLayout()

        # label logic
        spectrogramLabel = QLabel("Spectrograph Widget")
        spectrogramLabel.setFont(QFont("Arial", 20))
        spectrogramLabel.setStyleSheet("color: #b0bec5; font-weight: bold;")
        spectrogramLayout.addWidget(spectrogramLabel)

        # set layout
        spectrogramWidget.setStyleSheet("background-color: #000033;")
        spectrogramLayout.setAlignment(Qt.AlignLeft)
        spectrogramWidget.setLayout(spectrogramLayout)
        spectrogramWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Right side
        rightPanel = QWidget()
        rightLayout = QVBoxLayout()

        # label logic
        rightLabel = QLabel("Pitch Shifter")
        rightLabel.setFont(QFont("Arial", 20))
        rightLabel.setStyleSheet("color: #b0bec5; font-weight: bold;")
        rightLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        rightLayout.addWidget(rightLabel)
        
        # set layout
        rightPanel.setStyleSheet("background-color: #000033;")
        rightPanel.setLayout(rightLayout)
        rightPanel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        
        # combine widgets into page layout
        layout.addWidget(spectrogramWidget,3)
        layout.addWidget(rightPanel,1)

        # form page
        page.setLayout(layout)
        page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return page
    
    def buildEqualizerPage(self):
        page = QWidget()
        layout = QHBoxLayout()

        # Left side
        spectrogramWidget = QWidget()
        spectrogramLayout = QHBoxLayout()

        # label logic
        spectrogramLabel = QLabel("Spectrograph Widget")
        spectrogramLabel.setFont(QFont("Arial", 20))
        spectrogramLabel.setStyleSheet("color: #b0bec5; font-weight: bold;")
        spectrogramLayout.addWidget(spectrogramLabel)

        # set layout
        spectrogramWidget.setStyleSheet("background-color: #000033;")
        spectrogramLayout.setAlignment(Qt.AlignLeft)
        spectrogramWidget.setLayout(spectrogramLayout)
        spectrogramWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Right side
        rightPanel = QWidget()
        rightLayout = QVBoxLayout()

        # label logic
        rightLabel = QLabel("Equalizer")
        rightLabel.setFont(QFont("Arial", 20))
        rightLabel.setStyleSheet("color: #b0bec5; font-weight: bold;")
        rightLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        rightLayout.addWidget(rightLabel)
        
        # set layout
        rightPanel.setStyleSheet("background-color: #000033;")
        rightPanel.setLayout(rightLayout)
        rightPanel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        
        # combine widgets into page layout
        layout.addWidget(spectrogramWidget,3)
        layout.addWidget(rightPanel,1)

        # form page
        page.setLayout(layout)
        page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return page
    
    def buildSpectrogramPage(self):
        page = QWidget()
        layout = QHBoxLayout()

        # Left side
        spectrogramWidget = QWidget()
        spectrogramLayout = QHBoxLayout()

        # label logic
        spectrogramLabel = QLabel("Spectrogram Widget")
        spectrogramLabel.setFont(QFont("Arial", 20))
        spectrogramLabel.setStyleSheet("color: #b0bec5; font-weight: bold;")
        spectrogramLayout.addWidget(spectrogramLabel)

        # set layout
        spectrogramWidget.setStyleSheet("background-color: #000033;")
        spectrogramLayout.setAlignment(Qt.AlignLeft)
        spectrogramWidget.setLayout(spectrogramLayout)
        spectrogramWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Right side
        rightPanel = QWidget()
        rightLayout = QVBoxLayout()

        # label logic
        rightLabel = QLabel("Right Panel")
        rightLabel.setFont(QFont("Arial", 20))
        rightLabel.setStyleSheet("color: #b0bec5; font-weight: bold;")
        rightLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        rightLayout.addWidget(rightLabel)
        
        # set layout
        rightPanel.setStyleSheet("background-color: #000033;")
        rightPanel.setLayout(rightLayout)
        rightPanel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        
        # combine widgets into page layout
        layout.addWidget(spectrogramWidget,3)
        layout.addWidget(rightPanel,1)

        # form page
        page.setLayout(layout)
        page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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

        navBar.setStyleSheet("background-color: #000033;")
        navBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        navLayout.addWidget(self.titleLabel("SignalBox"), alignment=Qt.AlignLeft)

        for i, page in enumerate(["Spectrogram Visualizer", "Equalizer", "Pitch Shifter"]):
            button = QPushButton(page)
            button.setStyleSheet("color: #b0bec5; font-weight: bold;")
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
        