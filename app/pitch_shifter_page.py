from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QFileDialog, QPushButton, QComboBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

class PitchShifterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #000033;")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.inputToggle = QComboBox()
        self.fileLabel = QLabel("File: None")
        self.buildUI()
    
    def createSpectrographWidget(self):
         # Left side
        spectrographWidget = QWidget()
        spectrographLayout = QHBoxLayout()

        # label logic
        spectrographLabel = QLabel("Spectrograph Widget")
        spectrographLabel.setFont(QFont("Arial", 20))
        spectrographLabel.setStyleSheet("color: #e6e6f0; font-weight: bold;")
        spectrographLayout.addWidget(spectrographLabel)

        # set layout
        spectrographWidget.setStyleSheet("background-color: #12121c;")
        spectrographLayout.setAlignment(Qt.AlignLeft)
        spectrographWidget.setLayout(spectrographLayout)
        spectrographWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return spectrographWidget
    
    def createRightWidget(self):
        # Right side
        rightPanel = QWidget()
        self.rightLayout = QVBoxLayout()
        self.rightLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Section Title
        rightLabel = QLabel("Control Panel")
        rightLabel.setFont(QFont("Arial", 20))
        rightLabel.setStyleSheet("color: #e6e6f0; font-weight: bold;")
        rightLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.rightLayout.addWidget(rightLabel)

        # Input source toggle
        self.inputToggle.addItems(["Audio File", "Microphone"])
        self.inputToggle.setStyleSheet("font-size: 10px; color: #e6e6f0; font-weight: bold;")
        self.inputToggle.currentIndexChanged.connect(self.onInputSourceChanged)
        self.rightLayout.addWidget(self.inputToggle)
        
    # AUDIO FILE CONTAINER
        self.audioFileContainer = QWidget()
        audioFileLayout = QVBoxLayout()
        audioFileLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Add button to open file dialog
        openButton = QPushButton("Open Audio File")
        openButton.setStyleSheet("font-size: 10px; color: #e6e6f0; font-weight: bold;")
        openButton.clicked.connect(self.openFileDialog)

        # Add file label
        self.fileLabel.setStyleSheet("font-size: 10px; color: #e6e6f0; font-weight: bold;")
        self.fileLabel.setAlignment(Qt.AlignHCenter)
        audioFileLayout.addWidget(openButton)
        audioFileLayout.addWidget(self.fileLabel)
        self.audioFileContainer.setLayout(audioFileLayout)
        self.rightLayout.addWidget(self.audioFileContainer)        

        # MIC CONTAINER
        self.micContainer = QWidget()
        micLayout = QVBoxLayout()
        micLabel = QLabel("Microphone Input")
        micLabel.setStyleSheet("font-size: 10px; color: #e6e6f0; font-weight: bold;")
        micLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        micLayout.addWidget(micLabel)
        self.micContainer.setLayout(micLayout)
        self.micContainer.hide()
        self.rightLayout.addWidget(self.micContainer)

        # set layout
        rightPanel.setStyleSheet("background-color: #242436;")
        rightPanel.setLayout(self.rightLayout)
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
    
    def onInputSourceChanged(self, index):
        if self.inputToggle.currentText() == "Audio File":
            self.audioFileContainer.show()
            self.micContainer.hide()
        else:
            self.audioFileContainer.hide()
            self.micContainer.show()