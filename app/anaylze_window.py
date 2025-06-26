from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QVBoxLayout
from PySide6.QtGui import QFont
import numpy as np
import librosa
from app.audio_processor import AudioProcessor


class AnalyzeWindow(QWidget):
    def __init__(self, signal=None,samplerate=None):
        super().__init__()
        self.signal = signal
        self.samplerate = samplerate
        self.audioProcessor = AudioProcessor(signal = signal, sample_rate = samplerate)

        if signal is not None:
            self.times, self.f0, self.voiced_flag, self.voiced_probs = self.audioProcessor.comp_fund_freq()
        else:
            self.times = None
            self.f0 = None
            self.voiced_flag = None
            self.voiced_probs = None

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

        # add time label
        self.timeLabel = QLabel()
        self.timeLabel.setText("Time: 00:00:00")
        self.timeLabel.setFont(QFont("Arial", 14))
        self.timeLabel.setStyleSheet("color: #e6e6f0;")
        self.timeLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        statsLayout.addWidget(self.timeLabel)

        # add average energy label
        self.energyLabel = QLabel()
        self.energyLabel.setText("Average Energy: 0.0 dB")
        self.energyLabel.setFont(QFont("Arial", 14))
        self.energyLabel.setStyleSheet("color: #e6e6f0;")
        self.energyLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        statsLayout.addWidget(self.energyLabel)

        # add zero crossing rate label
        self.zcrLabel = QLabel()
        self.zcrLabel.setText("Zero Crossing Rate: 0.0")
        self.zcrLabel.setFont(QFont("Arial", 14))
        self.zcrLabel.setStyleSheet("color: #e6e6f0;")
        self.zcrLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        statsLayout.addWidget(self.zcrLabel)

        # add silence percentage label
        self.silenceLabel = QLabel()
        self.silenceLabel.setText("Silence Percentage: 0.0%")
        self.silenceLabel.setFont(QFont("Arial", 14))
        self.silenceLabel.setStyleSheet("color: #e6e6f0;")
        self.silenceLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        statsLayout.addWidget(self.silenceLabel)

        # add sample rate label
        self.sampleRateLabel = QLabel()
        self.sampleRateLabel.setText("Sample Rate: 0 Hz")
        self.sampleRateLabel.setFont(QFont("Arial", 14))
        self.sampleRateLabel.setStyleSheet("color: #e6e6f0;")
        self.sampleRateLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        statsLayout.addWidget(self.sampleRateLabel)

        self.updateBasicStats()  # Initialize with dummy values
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

        # add average fundamental frequency label
        self.avgF0Label = QLabel()
        self.avgF0Label.setText("Average Fundamental Frequency: 0.0 Hz")
        self.avgF0Label.setFont(QFont("Arial", 14))
        self.avgF0Label.setStyleSheet("color: #e6e6f0;")
        self.avgF0Label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        pitchLayout.addWidget(self.avgF0Label)

        # add fundamental frequency range label
        self.f0RangeLabel = QLabel()
        self.f0RangeLabel.setText("Fundamental Frequency Range: 0.0 Hz - 0.0 Hz")
        self.f0RangeLabel.setFont(QFont("Arial", 14))
        self.f0RangeLabel.setStyleSheet("color: #e6e6f0;")
        self.f0RangeLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        pitchLayout.addWidget(self.f0RangeLabel)

        # add pitch standard deviation label
        self.pitchStdDevLabel = QLabel()
        self.pitchStdDevLabel.setText("Pitch Standard Deviation: 0.0 Hz")
        self.pitchStdDevLabel.setFont(QFont("Arial", 14))
        self.pitchStdDevLabel.setStyleSheet("color: #e6e6f0;")
        self.pitchStdDevLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        pitchLayout.addWidget(self.pitchStdDevLabel)

        # add voiced/unvoiced ratio label
        self.voicedRatioLabel = QLabel()
        self.voicedRatioLabel.setText("Voiced/Unvoiced Ratio: 0.0")
        self.voicedRatioLabel.setFont(QFont("Arial", 14))
        self.voicedRatioLabel.setStyleSheet("color: #e6e6f0;")
        self.voicedRatioLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        pitchLayout.addWidget(self.voicedRatioLabel)

        # add pitch jitter label
        self.pitchJitterLabel = QLabel()
        self.pitchJitterLabel.setText("Pitch Jitter: 0.0%")
        self.pitchJitterLabel.setFont(QFont("Arial", 14))
        self.pitchJitterLabel.setStyleSheet("color: #e6e6f0;")
        self.pitchJitterLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        pitchLayout.addWidget(self.pitchJitterLabel)

        self.updatePitchStats()  # Initialize with dummy values
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

       # add pitch breaks label
       self.pitchBreaksLabel = QLabel()
       self.pitchBreaksLabel.setText("Pitch Breaks: N/A")
       self.pitchBreaksLabel.setFont(QFont("Arial", 14))
       self.pitchBreaksLabel.setStyleSheet("color: #e6e6f0;")
       self.pitchBreaksLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
       fluencyLayout.addWidget(self.pitchBreaksLabel)

       # add median F0 label
       self.medianF0Label = QLabel()
       self.medianF0Label.setText("Median F0: N/A")
       self.medianF0Label.setFont(QFont("Arial", 14))
       self.medianF0Label.setStyleSheet("color: #e6e6f0;")
       self.medianF0Label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
       fluencyLayout.addWidget(self.medianF0Label)

       # add mean pitch slope label
       self.meanPitchSlopeLabel = QLabel()
       self.meanPitchSlopeLabel.setText("Mean Pitch Slope: N/A")
       self.meanPitchSlopeLabel.setFont(QFont("Arial", 14))
       self.meanPitchSlopeLabel.setStyleSheet("color: #e6e6f0;")
       self.meanPitchSlopeLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
       fluencyLayout.addWidget(self.meanPitchSlopeLabel)

       # add voicing duration label
       self.voicingDurationLabel = QLabel()
       self.voicingDurationLabel.setText("Voicing Duration: N/A")
       self.voicingDurationLabel.setFont(QFont("Arial", 14))
       self.voicingDurationLabel.setStyleSheet("color: #e6e6f0;")
       self.voicingDurationLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
       fluencyLayout.addWidget(self.voicingDurationLabel)

       # add curve smoothness label
       self.curveSmoothnessLabel = QLabel()
       self.curveSmoothnessLabel.setText("Curve Smoothness: N/A")
       self.curveSmoothnessLabel.setFont(QFont("Arial", 14))
       self.curveSmoothnessLabel.setStyleSheet("color: #e6e6f0;")
       self.curveSmoothnessLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
       fluencyLayout.addWidget(self.curveSmoothnessLabel)

       self.updateFluencyStats()
       return self.fluencyContainer

    def updateBasicStats(self):
        if self.signal is not None and self.samplerate:
            self.setTimeLabel()
            self.setEnergyLabel()
            self.setZCRLabel()
            self.setSilenceLabel()
            self.setSampleRateLabel()
    
    def updatePitchStats(self):
        if self.signal is not None and self.samplerate:
            self.setAverageF0Label()
            self.setF0RangeLabel()
            self.setPitchStdDevLabel()
            self.setVoicedRatioLabel()
            self.setPitchJitterLabel()

    def updateFluencyStats(self):
        if self.signal is not None and self.samplerate:
            self.pitchBreaks()
            self.medianF0()
            self.meanPitchSlope()
            self.voicingDuration()
            self.curveSmoothness()
    
    def pitchBreaks(self):
        pass

    def medianF0(self):
        pass

    def meanPitchSlope(self):
        pass

    def voicingDuration(self):
        pass

    def curveSmoothness(self):
        pass

    def setTimeLabel(self):
        if self.signal is not None and self.samplerate:
            hours,minutes,seconds = self.audioProcessor.getTime()
            self.timeLabel.setText(f"Time: {hours:02}:{minutes:02}:{seconds:02}")
    
    def setEnergyLabel(self):
        if self.signal is not None and self.samplerate:
            energy = np.mean(self.signal ** 2)
            energy_db = 10 * np.log10(energy + 1e-10)  # Avoid log(0)
            self.energyLabel.setText(f"Average Energy: {energy_db:.2f} dB")

    def setZCRLabel(self):
        if self.signal is not None and self.samplerate:
            zcr = librosa.feature.zero_crossing_rate(y = self.signal, frame_length=2048, hop_length=256)
            avg_zcr = np.mean(zcr)
            self.zcrLabel.setText(f"Zero Crossing Rate: {avg_zcr:.4f}")
    
    def setSilenceLabel(self):
        if self.signal is not None and self.samplerate:
            silence_percentage = self.audioProcessor.compute_silence()
            self.silenceLabel.setText(f"Silence Percentage: {silence_percentage:.2f}%")
    
    def setSampleRateLabel(self):
        self.sampleRateLabel.setText(f"Sample Rate: {self.samplerate} Hz")

    def setAverageF0Label(self):
        avg_f0 = self.audioProcessor.avg_fundamental_freq(self.f0)
        self.avgF0Label.setText(f"Average Fundamental Frequency: {avg_f0:.2f} Hz")

    def setF0RangeLabel(self):
        f0_min, f0_max = self.audioProcessor.f0_range(self.f0)
        self.f0RangeLabel.setText(f"Fundamental Frequency Range: {f0_min:.2f} Hz - {f0_max:.2f} Hz")

    def setPitchStdDevLabel(self):
        if self.f0 is not None:
            pitch_std_dev = np.nanstd(self.f0)
            self.pitchStdDevLabel.setText(f"Pitch Standard Deviation: {pitch_std_dev:.2f} Hz")
        else:
            self.pitchStdDevLabel.setText("Pitch Standard Deviation: N/A")

    def setVoicedRatioLabel(self):
        voiced_ratio = self.audioProcessor.voiced_ratio(self.voiced_flag)
        self.voicedRatioLabel.setText(f"Voiced/Unvoiced Ratio: {voiced_ratio:.2f}")

    def setPitchJitterLabel(self):
        jitter = self.audioProcessor.pitch_jitter(self.f0)
        self.pitchJitterLabel.setText(f"Pitch Jitter: {jitter:.2f}%") if jitter is not None else self.pitchJitterLabel.setText("Pitch Jitter: N/A")
