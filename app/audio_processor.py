import librosa
import numpy as np

class AudioProcessor:
    def __init__(self, audio_file = None, signal=None, sample_rate=None):
        self.audio_file = audio_file
        self.target_sample_rate = 44100
        self.signal = signal
        self.sample_rate = sample_rate
        self.normalized_audio = None

    def load_audio(self):

        # check if audio file is provided
        if not self.audio_file:
            raise ValueError("No audio file provided.")
        
        # Load the audio file
        self.signal, self.sample_rate = librosa.load(self.audio_file, sr=self.target_sample_rate)

        return self.signal, self.sample_rate

    def normalize_audio(self):
        # Check if the audio signal is loaded
        if self.signal is None:
            raise ValueError("Audio signal not loaded. Please load an audio file first.")
        
        # Normalize the audio signal
        self.normalized_audio = librosa.util.normalize(self.signal,norm=np.inf)
        return self.normalized_audio

    def frames_to_array(self,frames):
        data = b''.join(frames)
        audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0  # Convert to float32 and normalize
        self.signal = audio_data
        self.sample_rate = 44100
        return audio_data
    
    def comp_fund_freq(self):
        # Check if the audio signal is loaded
        if self.signal is None:
            raise ValueError("Audio signal not loaded. Please load an audio file first.")
        
        # Compute the fundamental frequency
        f0, voiced_flag, voiced_probs = librosa.pyin(self.signal,sr=self.sample_rate, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C10'), frame_length=2048, hop_length=256)
        times = librosa.times_like(f0, sr=self.sample_rate)
        return times, f0, voiced_flag, voiced_probs
    
    def compute_silence(self):
        # Check if the audio signal is loaded
        if self.signal is None:
            raise ValueError("Audio signal not loaded. Please load an audio file first.")
        
        # Compute silence regions
        frame_length = 2048
        hop_length = 256

        energy = np.array([
            np.sum(np.abs(self.signal[i:i + frame_length] ** 2))
            for i in range(0, len(self.signal) - frame_length, hop_length)
        ])

        threshold_value = 1e-2 #np.percentile(energy, 3)
        silence = np.mean(energy < threshold_value) * 100
        return silence