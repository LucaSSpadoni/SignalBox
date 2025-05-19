from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QFileDialog, QPushButton, QComboBox, QSlider
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from app.audio_processor import AudioProcessor
from app.spectrogram_plot import SpectrogramPlot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import librosa.display

class SpectrogramPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #000033;")
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # control panel
        self.inputToggle = QComboBox()
        self.windowSize = QComboBox()
        self.hopLength = QSlider(Qt.Horizontal)
        self.hopLengthValue = QLabel("Hop Length: 1")
        self.colorMap = QComboBox()
        self.fileLabel = QLabel("File: None")

        # audio processor
        self.audioPath = None

        # plotting
        self.canvas = FigureCanvas(Figure(figsize=(5, 4)))
        self.canvas.setStyleSheet("background-color: transparent;")
        self.canvas.setContentsMargins(0, 0, 0, 0)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.hide()

        self.buildUI()

    def createSpectrogramWidget(self):
        # Left side
        self.spectrogramWidget = QWidget()
        spectrogramLayout = QVBoxLayout()

        spectrogramLayout.setContentsMargins(0, 0, 0, 0)
        spectrogramLayout.setSpacing(0)
        self.spectrogramWidget.setStyleSheet("background-color: #000033;")

        # Add canvas to the layout
        spectrogramLayout.addWidget(self.canvas)

        # set layout
        self.spectrogramWidget.setStyleSheet("background-color: #000033;")
        spectrogramLayout.setAlignment(Qt.AlignLeft)
        self.spectrogramWidget.setLayout(spectrogramLayout)
        self.spectrogramWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # return spectrogramWidget
        return self.spectrogramWidget

    def createRightWidget(self):
        # Right side
        rightPanel = QWidget()
        self.rightLayout = QVBoxLayout()
        self.rightLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Section Title
        rightLabel = QLabel("Control Panel")
        rightLabel.setFont(QFont("Arial", 20))
        rightLabel.setStyleSheet("color: #b0bec5; font-weight: bold;")
        rightLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.rightLayout.addWidget(rightLabel)

        # Input source toggle
        self.inputToggle.addItems(["Audio File", "Microphone"])
        self.inputToggle.setStyleSheet("font-size: 10px; color: #b0bec5; font-weight: bold;")
        self.inputToggle.currentIndexChanged.connect(self.onInputSourceChanged)
        self.rightLayout.addWidget(self.inputToggle)
        
    # AUDIO FILE CONTAINER
        self.audioFileContainer = QWidget()
        audioFileLayout = QVBoxLayout()
        audioFileLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Add button to open file dialog
        openButton = QPushButton("Open Audio File")
        openButton.setStyleSheet("font-size: 10px; color: #b0bec5; font-weight: bold;")
        openButton.clicked.connect(self.openFileDialog)

        # Add file label
        self.fileLabel.setStyleSheet("font-size: 10px; color: #b0bec5; font-weight: bold;")
        self.fileLabel.setAlignment(Qt.AlignHCenter)
        audioFileLayout.addWidget(openButton)
        audioFileLayout.addWidget(self.fileLabel)
        self.audioFileContainer.setLayout(audioFileLayout)
        self.rightLayout.addWidget(self.audioFileContainer)        

        # MIC CONTAINER
        self.micContainer = QWidget()
        micLayout = QVBoxLayout()
        micLabel = QLabel("Microphone Input")
        micLabel.setStyleSheet("font-size: 10px; color: #b0bec5; font-weight: bold;")
        micLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        micLayout.addWidget(micLabel)
        self.micContainer.setLayout(micLayout)
        self.micContainer.hide()
        self.rightLayout.addWidget(self.micContainer)

        # set layout
        rightPanel.setStyleSheet("background-color: #000033;")
        rightPanel.setLayout(self.rightLayout)
        rightPanel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Window size label
        windowSizeLabel = QLabel("Window Size")
        windowSizeLabel.setStyleSheet("font-size: 10px; color: #b0bec5; font-weight: bold;")
        windowSizeLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.rightLayout.addWidget(windowSizeLabel)

        # Add window size dropdown
        self.windowSize.addItems(["256", "512", "1024", "2048"])
        self.windowSize.setStyleSheet("font-size: 10px; color: #b0bec5; font-weight: bold;")
        self.windowSize.currentIndexChanged.connect(self.onWindowSizeChanged)
        self.rightLayout.addWidget(self.windowSize)

        # Hop length label
        self.hopLengthValue.setStyleSheet("font-size: 10px; color: #b0bec5; font-weight: bold;")
        self.hopLengthValue.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.rightLayout.addWidget(self.hopLengthValue)

        # Add hop length slider
        self.hopLength.setMinimum(1)
        self.hopLength.setMaximum(512)
        self.hopLength.setValue(1)
        self.hopLength.setStyleSheet("font-size: 10px; color: #b0bec5; font-weight: bold;")
        self.hopLength.valueChanged.connect(self.onHopLengthChanged)
        self.rightLayout.addWidget(self.hopLength)

        # Color map label
        colorMapLabel = QLabel("Color Map")
        colorMapLabel.setStyleSheet("font-size: 10px; color: #b0bec5; font-weight: bold;")
        colorMapLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.rightLayout.addWidget(colorMapLabel)

        # Add color map dropdown
        colorMapList = ["viridis", "plasma", "inferno", "magma", "cividis", "turbo"]
        self.colorMap.addItems(colorMapList)
        self.colorMap.setStyleSheet("font-size: 10px; color: #b0bec5; font-weight: bold;")
        self.colorMap.currentIndexChanged.connect(self.onColorMapChanged)
        self.rightLayout.addWidget(self.colorMap)

        # Add Visualize button
        visualizeButton = QPushButton("Visualize Spectrogram")
        visualizeButton.setStyleSheet("font-size: 10px; color: #b0bec5; font-weight: bold;")
        visualizeButton.clicked.connect(self.plotSpectrogram)
        self.rightLayout.addWidget(visualizeButton)

        #return rightPanel
        return rightPanel

    def buildUI(self):
        # combine widgets into page layout
        self.layout.addWidget(self.createSpectrogramWidget(),3)
        self.layout.addWidget(self.createRightWidget(),1)

        # Set initial visibility
        self.onWindowSizeChanged(0)

    def openFileDialog(self):
        # Open file dialog to select audio file
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Audio File", "", "Audio Files (*.wav *.mp3);;All Files (*)", options=options)
        if fileName:
            print(f"Selected file: {fileName}")
            self.audioPath = fileName

            # Update label with selected file name
            fn = fileName.split("/")
            self.fileLabel.setText(f"File: {fn[-1]}")

    def onInputSourceChanged(self, index):
        if self.inputToggle.currentText() == "Audio File":
            self.audioFileContainer.show()
            self.micContainer.hide()
        else:
            self.audioFileContainer.hide()
            self.micContainer.show()

    def micRecorder(self):
        # Placeholder for microphone input logic
        pass

    def onWindowSizeChanged(self, index):
        n_fft = int(self.windowSize.currentText())
        self.hopLength.setMinimum(n_fft // 8)
        self.hopLength.setMaximum(n_fft // 2)

    def onHopLengthChanged(self, value):
        self.hopLengthValue.setText(f"Hop Length: {value}")
    
    def onColorMapChanged(self, index):
        # Placeholder for color map logic
        pass

    def plotSpectrogram(self):

        if not self.audioPath:
            raise ValueError("No audio file selected.")
        
        # load audio file
        processor = AudioProcessor(self.audioPath)
        signal, sr = processor.load_audio()

        # create normalized audio
        signal = processor.normalize_audio()

        # get parameters
        n_fft = int(self.windowSize.currentText())
        hop_length = self.hopLength.value()
        color_map = self.colorMap.currentText()

        # create spectrogram plot
        plotter = SpectrogramPlot(signal, sr, axis_type="log", title="Spectrogram", xlabel="Time", ylabel="Frequency")
        plotter.compute_spectrogram(n_fft=n_fft, hop_length=hop_length)
        
        # clear previous plot
        #self.canvas.figure.clf()
        fig = Figure(figsize=(5,4),dpi=100,facecolor='#000033')
        canvas = FigureCanvas(fig)
        canvas.setStyleSheet("background-color: transparent;")
        canvas.setContentsMargins(0, 0, 0, 0)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        ax = fig.add_subplot(111)

        ax.set_facecolor('#000033')
        for spine in ax.spines.values():
            spine.set_visible(False)

        img = librosa.display.specshow(plotter.data, sr=sr, x_axis='time', y_axis='log', ax=ax, cmap=color_map,hop_length=hop_length)
        colorbar = fig.colorbar(img, ax=ax, format='%+2.0f dB')
        colorbar.set_label('Amplitude (dB)', color='#b0bec5')
        colorbar.ax.yaxis.set_tick_params(color='#b0bec5')
        colorbar.outline.set_edgecolor('#b0bec5')
        plt.setp(colorbar.ax.get_yticklabels(), color='#b0bec5')

        # Style the plot
        ax.tick_params(colors='#b0bec5')  # axis ticks
        ax.spines['bottom'].set_color('#b0bec5')
        ax.spines['left'].set_color('#b0bec5')
        ax.xaxis.label.set_color('#b0bec5')
        ax.yaxis.label.set_color('#b0bec5')
        for spine in ax.spines.values():
            spine.set_edgecolor('#b0bec5')

        # Clear previous plot if any
        layout = self.spectrogramWidget.layout()
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        layout.addWidget(canvas)
        self.spectrogramCanvas = canvas

    def onVisualizeButtonClicked(self):
        try:
            self.plotSpectrogram()
        except Exception as e:
            print(f"Error visualizing spectrogram: {e}")

    def onSaveButtonClicked(self):
        # Placeholder for save button logic
        pass









        



        