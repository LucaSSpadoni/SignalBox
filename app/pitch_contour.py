from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QFileDialog, QPushButton, QComboBox, QSlider, QMessageBox
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QDateTime, QTimer, QElapsedTimer
from app.audio_processor import AudioProcessor
from app.contour_plot import ContourPlot
from app.audio_recorder import AudioRecorder
from app.anaylze_window import AnalyzeWindow
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pyaudio # type: ignore

import vlc # type: ignore

class PitchContourPage(QWidget):
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

        # play audio
        self.player = vlc.MediaPlayer()

        # create mic timer
        self.audioTimer = QTimer()
        self.elapsedTimer = QElapsedTimer()
        self.audioTimer.timeout.connect(self.updateElapsedTime)
        self.audioTimer.setInterval(1000) # 1 second interval

        # create recording state
        self.audioRecorder = AudioRecorder()
        self.frames = None

        # build out the UI
        self.buildUI()

    def createContourWidget(self):
        # Left side
        self.contourWidget = QWidget()
        contourLayout = QVBoxLayout()

        contourLayout.setContentsMargins(0, 0, 0, 0)
        contourLayout.setSpacing(0)
        self.contourWidget.setStyleSheet("background-color: #12121c;")

        # Add canvas to the layout
        contourLayout.addWidget(self.canvas)

        # set layout
        contourLayout.setAlignment(Qt.AlignLeft)
        self.contourWidget.setLayout(contourLayout)
        self.contourWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # return contourWidget
        return self.contourWidget

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
        openButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

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

        # mic label
        self.micLabel = QLabel("Time elapsed: 00:00")
        self.micLabel.setStyleSheet("font-size: 10px; color: #e6e6f0; font-weight: bold;")
        self.micLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.micLabel.setAlignment(Qt.AlignHCenter)
        micLayout.addWidget(self.micLabel)

        # start/stop container 
        start_stopContainer = QWidget()
        start_stopContainerLayout = QVBoxLayout()
        start_stopContainerLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        start_stopContainer.setLayout(start_stopContainerLayout)
        micLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # start button
        startButton = QPushButton("Start Recording")
        startButton.setStyleSheet("font-size: 10px; color: #e6e6f0; font-weight: bold;")
        startButton.clicked.connect(self.onStartRecording)
        startButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # stop button
        stopButton = QPushButton("Stop Recording")
        stopButton.setStyleSheet("font-size: 10px; color: #e6e6f0; font-weight: bold;")
        stopButton.clicked.connect(self.onStopRecording)
        stopButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # add reset button
        resetButton = QPushButton("Reset Recording")
        resetButton.setStyleSheet("font-size: 10px; color: #e6e6f0; font-weight: bold;")
        resetButton.clicked.connect(self.onResetRecording)
        resetButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        # add buttons to container
        start_stopContainerLayout.setSpacing(15)
        start_stopContainerLayout.addWidget(startButton)
        start_stopContainerLayout.addWidget(stopButton)
        start_stopContainerLayout.addWidget(resetButton)
        micLayout.addWidget(start_stopContainer)
        self.micContainer.setLayout(micLayout)
        self.micContainer.hide()
        self.rightLayout.addWidget(self.micContainer)

        # set layout
        rightPanel.setStyleSheet("background-color: #242436;")
        rightPanel.setLayout(self.rightLayout)
        rightPanel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # Add play audio button
        playButton = QPushButton("Play Audio")
        playButton.setStyleSheet("font-size: 10px; color: #e6e6f0; font-weight: bold;")
        playButton.clicked.connect(self.onPlayButtonClicked)
        self.rightLayout.addWidget(playButton)

        # Add Visualize button
        visualizeButton = QPushButton("Visualize Contour")
        visualizeButton.setStyleSheet("font-size: 10px; color: #e6e6f0; font-weight: bold;")
        visualizeButton.clicked.connect(self.onVisualizeButtonClicked)
        self.rightLayout.addWidget(visualizeButton)

        # add analysis button
        analysisButton = QPushButton("Analyze")
        analysisButton.setStyleSheet("font-size: 10px; color: #e6e6f0; font-weight: bold;")
        analysisButton.clicked.connect(self.onAnalyzeClicked)
        self.rightLayout.addWidget(analysisButton)

        # Add Save image button
        saveButton = QPushButton("Save Image")
        saveButton.setStyleSheet("font-size: 10px; color: #e6e6f0; font-weight: bold;")
        saveButton.clicked.connect(self.onSaveButtonClicked)
        self.rightLayout.addWidget(saveButton)

        # Add save audio button
        self.saveAudioButton = QPushButton("Save Audio")
        self.saveAudioButton.setStyleSheet("font-size: 10px; color: #e6e6f0; font-weight: bold;")
        self.saveAudioButton.clicked.connect(self.onSaveAudioButtonClicked)
        self.rightLayout.addWidget(self.saveAudioButton)
        self.saveAudioButton.hide()

        # return rightPanel
        return rightPanel

    def buildUI(self):
        # combine widgets into page layout
        self.layout.addWidget(self.createContourWidget(),3)
        self.layout.addWidget(self.createRightWidget(),1)

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
            self.saveAudioButton.hide()
        else:
            self.audioFileContainer.hide()
            self.micContainer.show()
            self.saveAudioButton.show()

    def onVisualizeButtonClicked(self):
        try:
            self.plotContour()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to visualize contour: {e}")
            self.canvas.hide()
        
    def onSaveButtonClicked(self):
        if not hasattr(self, 'contourCanvas') or self.contourCanvas is None:
            QMessageBox.warning(self, "Error", "No contour to save.")
            return
        
        options = QFileDialog.Options()
        default_name = f"contour_plot_{QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')}.png"
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Contour Plot", default_name, "PNG Files (*.png);;JPEG Files (*.jpg);;SVG Files (*.svg);;PDF Files (*.pdf);;All Files (*)", options=options)
        if fileName:
            try:
                self.contourCanvas.figure.savefig(fileName, format='png', dpi=300, bbox_inches='tight')
                QMessageBox.information(self, "Success", f"Contour plot saved as {fileName}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save contour plot: {e}")

    def onPlayButtonClicked(self):
        input_source = self.inputToggle.currentText()

        if input_source == "Audio File":
            if not self.audioPath:
                QMessageBox.warning(self, "Error", "No audio file selected.")
                return
            
            # play audio
            self.player.set_media(vlc.Media(self.audioPath))
            self.player.audio_set_volume(50)
            self.player.play()

        elif input_source == "Microphone":
            if not self.frames:
                QMessageBox.warning(self, "Error", "No audio recorded from microphone.")
                return
            
            # use pyaudio to play recorded audio
            p = pyaudio.PyAudio()

            try:
                stream = p.open(format=pyaudio.paInt16,
                                channels=self.audioRecorder.channels,
                                rate=self.audioRecorder.sampleRate,
                                output=True)

                # Convert frames to bytes and play
                audio_data = b''.join(self.frames)
                stream.write(audio_data)
                stream.stop_stream()
                stream.close()
            finally:
                p.terminate()

    def onSaveAudioButtonClicked(self):
        if not self.frames:
            QMessageBox.warning(self, "Error", "No audio recorded from microphone.")
            return
        
        options = QFileDialog.Options()
        default_name = f"recording_{QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')}.wav"
        fileName, _ = QFileDialog.getSaveFileName(self, "Save Audio", default_name, "WAV Files (*.wav);;All Files (*)", options=options)
        if fileName:
            try:
                self.audioRecorder.save_recording(fileName)
                QMessageBox.information(self, "Success", f"Audio saved as {fileName}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save audio: {e}")

    def onStartRecording(self):
        self.elapsedTimer.start()
        self.audioTimer.start()
        self.audioRecorder.start_recording()

    def updateElapsedTime(self):
        elapsed_ms = self.elapsedTimer.elapsed()
        minutes = (elapsed_ms // 60000)
        seconds = (elapsed_ms // 1000) % 60
        self.micLabel.setText(f"Time elapsed: {minutes:02}:{seconds:02}")   

    def onStopRecording(self):
        self.audioTimer.stop()
        self.audioRecorder.stop_recording()
        self.frames = self.audioRecorder.frames
        if self.frames:
            QMessageBox.information(self, "Recording", "Audio recording stopped successfully.")
        else:
            QMessageBox.warning(self, "Recording", "No audio recorded.")
            self.frames = None
            self.audioRecorder.reset()

    def onResetRecording(self):
        self.elapsedTimer.invalidate()
        self.micLabel.setText("Time elapsed: 00:00")
        self.audioTimer.stop()
        self.audioRecorder.reset()
        self.frames = None

    def plotContour(self):

        input_source = self.inputToggle.currentText()
        
        # if the user wants to visualize the file input
        if input_source == "Audio File":
            if not self.audioPath:
                QMessageBox.warning(self, "Error", "No audio file selected.")
                return
            
            # load audio file
            processor = AudioProcessor(self.audioPath)
            signal, sr = processor.load_audio()
            times, f0, voiced_flag, voiced_probs = processor.comp_fund_freq()
            
        
        # if the user wants to visualize the mic input
        elif input_source == "Microphone":
            if not self.frames:
                QMessageBox.warning(self, "Error", "No audio recorded from microphone.")
                return
            
            processor = AudioProcessor()
            signal = processor.frames_to_array(self.frames)
            processor.signal = signal
            processor.sample_rate = self.audioRecorder.sampleRate # Assuming a default sample rate for mic input
            times, f0, voiced_flag, voiced_probs = processor.comp_fund_freq()

        plotter = ContourPlot(times, f0, voiced_flag, voiced_probs)
        canvas = plotter.plot_pitch()

        layout = self.contourWidget.layout()
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        layout.addWidget(canvas)
        self.contourCanvas = canvas

    def onAnalyzeClicked(self):
        self.analysis_window = AnalyzeWindow()
        self.analysis_window.show()
        