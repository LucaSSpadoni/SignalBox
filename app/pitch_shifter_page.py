from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QFileDialog, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class PitchShifterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #000033;")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.fileLabel = QLabel("File: None")
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
        container = QVBoxLayout()
        container.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Section Title
        rightLabel = QLabel("Control Panel")
        rightLabel.setFont(QFont("Arial", 20))
        rightLabel.setStyleSheet("color: #b0bec5; font-weight: bold;")
        rightLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        
        # Add button to open file dialog
        openButton = QPushButton("Open Audio File")
        openButton.setStyleSheet("font-size: 10px; color: #b0bec5; font-weight: bold;")
        openButton.clicked.connect(self.openFileDialog)

        # Add file label
        self.fileLabel.setStyleSheet("font-size: 10px; color: #b0bec5; font-weight: bold;")
        self.fileLabel.setAlignment(Qt.AlignHCenter)
        
        # add widgets to container
        container.addWidget(rightLabel)
        container.addWidget(openButton)
        container.addWidget(self.fileLabel)

        # set layout
        rightPanel.setStyleSheet("background-color: #000033;")
        rightPanel.setLayout(container)
        rightPanel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        #return rightPanel
        return rightPanel

    def buildUI(self):
        
        # combine widgets into page layout
        self.layout.addWidget(self.createSpectrographWidget(),3)
        self.layout.addWidget(self.createRightWidget(),1)
    
    def openFileDialog(self):
        # Open file dialog to select audio file
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.wav *.mp3);;All Files (*)", options=options)
        if fileName:
            print(f"Selected file: {fileName}")

            # Update label with selected file name
            fn = fileName.split("/")
            self.fileLabel.setText(f"File: {fn[-1]}")
            # Here you can add code to process the selected file