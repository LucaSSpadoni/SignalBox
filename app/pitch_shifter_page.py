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
    
    def createSpectrographWidget(self):
         # Left side
        spectrographWidget = QWidget()
        spectrographLayout = QHBoxLayout()

        # label logic
        spectrographLabel = QLabel("Spectrograph Widget")
        spectrographLabel.setFont(QFont("Arial", 20))
        spectrographLabel.setStyleSheet("color: #b0bec5; font-weight: bold;")
        spectrographLayout.addWidget(spectrographLabel)

        # set layout
        spectrographWidget.setStyleSheet("background-color: #000033;")
        spectrographLayout.setAlignment(Qt.AlignLeft)
        spectrographWidget.setLayout(spectrographLayout)
        spectrographWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return spectrographWidget
    
    def createRightWidget(self):
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
        return rightPanel

    def buildUI(self):
        
        # combine widgets into page layout
        self.layout.addWidget(self.createSpectrographWidget(),3)
        self.layout.addWidget(self.createRightWidget(),1)