import librosa
import numpy as np
import soundfile as sf

class AudioProcessor:
    def __init__(self, audio_file):
        self.audio_file = audio_file
        self.target_sample_rate = 44100
        self.signal = None
        self.sample_rate = None
        self.normalized_audio = None

    def load_audio(self):

        # check if audio file is provided
        if not self.audio_file:
            raise ValueError("No audio file provided.")
        
        # Load the audio file
        self.signal, self.sample_rate = librosa.load(self.audio_file, sr=self.target_sample_rate, mono=True)

        return self.signal, self.sample_rate

    def normalize_audio(self):
        # Check if the audio signal is loaded
        if self.signal is None:
            raise ValueError("Audio signal not loaded. Please load an audio file first.")
        
        # Normalize the audio signal
        self.normalized_audio = librosa.util.normalize(self.signal,norm=np.inf)
        return self.normalized_audio

    def save_audio(self, output_file):
        # Check if the normalized audio signal is available
        # Save the normalized audio signal to a file
        pass