import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

class SpectrogramPlot:
    def __init__(self, signal, samplerate, axis_type = "log", title="Spectrogram", xlabel="Time", ylabel="Frequency"):
        self.signal = signal
        self.samplerate = samplerate
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.axis_type = axis_type
        self.data = None

    def compute_spectrogram(self, n_fft=2048, hop_length=512):
        # Compute the Short-Time Fourier Transform (STFT)
        stft = librosa.stft(self.signal, n_fft=n_fft, hop_length=hop_length)

        # create a spectrogram
        self.data = np.abs(stft)

        # Convert to decibels
        self.data = librosa.amplitude_to_db(self.data, ref=np.max)

    def plot(self, cmap='viridis'):
        plt.figure(figsize=(10, 6))
        librosa.display.specshow(self.data, sr=self.samplerate, x_axis='time', y_axis= self.axis_type, cmap=cmap)
        plt.colorbar(format='%+2.0f dB')
        plt.title(self.title)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.tight_layout()
        plt.show()