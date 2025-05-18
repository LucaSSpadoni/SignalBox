from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class PitchShifterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #000033;")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.buildUI()

    def buildUI(self):
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
        self.layout.addWidget(spectrogramWidget,3)
        self.layout.addWidget(rightPanel,1)