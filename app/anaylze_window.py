from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QVBoxLayout
from PySide6.QtGui import QFont


class AnalyzeWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Analyze Window")
        self.setGeometry(200, 200, 900, 600)
        self.setStyleSheet("background-color: #1b1b2f;")

        # Create layout and widgets
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.basicStatsUI()
        self.pitchUI()
        self.fluencyUI()
        self.buildUI()

    def buildUI(self):
        self.layout.addWidget(self.statsContainer, 1)
        self.layout.addWidget(self.pitchContainer, 1)
        self.layout.addWidget(self.fluencyContainer, 1)

    def basicStatsUI(self):
        # set layout
        self.statsContainer = QWidget(self)
        self.statsContainer.setStyleSheet("background-color: #242436;")
        statsLayout = QVBoxLayout(self.statsContainer)
        self.statsContainer.setLayout(statsLayout)

        # Add title label
        titleLabel = QLabel("Basic Statistics", self.statsContainer)
        titleLabel.setFont(QFont("Arial", 20))
        titleLabel.setStyleSheet("color: #e6e6f0; font-weight: bold;")
        titleLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        statsLayout.addWidget(titleLabel)

        return self.statsContainer
    
    def pitchUI(self):
        # set layout
        self.pitchContainer = QWidget(self)
        self.pitchContainer.setStyleSheet("background-color: #242436;")
        pitchLayout = QVBoxLayout(self.pitchContainer)
        self.pitchContainer.setLayout(pitchLayout)

        # Add title label
        titleLabel = QLabel("Pitch Analysis", self.pitchContainer)
        titleLabel.setFont(QFont("Arial", 20))
        titleLabel.setStyleSheet("color: #e6e6f0; font-weight: bold;")
        titleLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        pitchLayout.addWidget(titleLabel)

        return self.pitchContainer
    
    def fluencyUI(self):
       # set layout
       self.fluencyContainer = QWidget(self)
       self.fluencyContainer.setStyleSheet("background-color: #242436;")
       fluencyLayout = QVBoxLayout(self.fluencyContainer)
       self.fluencyContainer.setLayout(fluencyLayout)

       # Add title label
       titleLabel = QLabel("Fluency Analysis", self.fluencyContainer)
       titleLabel.setFont(QFont("Arial", 20))
       titleLabel.setStyleSheet("color: #e6e6f0; font-weight: bold;")
       titleLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
       fluencyLayout.addWidget(titleLabel)

       return self.fluencyContainer