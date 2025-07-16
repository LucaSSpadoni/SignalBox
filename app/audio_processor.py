import librosa
import numpy as np
from sklearn.metrics import r2_score
from numpy.polynomial import Polynomial

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
    
    def getTime(self):
        # Check if the audio signal is loaded
        if self.signal is None:
            raise ValueError("Audio signal not loaded. Please load an audio file first.")
        
        # Calculate duration in seconds
        duration = len(self.signal) / self.sample_rate
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        return hours, minutes, seconds
    
    def avg_fundamental_freq(self, f0):
        # Check if the f0 array is provided
        if f0 is None or len(f0) == 0:
            raise ValueError("Fundamental frequency array is empty or not provided.")
        

        # avoid NaN values in f0
        valid_f0 = f0[~np.isnan(f0)]
        
        # Calculate the average fundamental frequency
        avg_f0 = np.nanmean(f0)
        return avg_f0
    
    def f0_range(self, f0):
        # Check if the f0 array is provided
        if f0 is None or len(f0) == 0:
            raise ValueError("Fundamental frequency array is empty or not provided.")
        
        # Calculate the range of fundamental frequency
        f0_min = np.nanmin(f0)
        f0_max = np.nanmax(f0)
        return f0_min, f0_max
    
    def f0_std_dev(self, f0):
        # Check if the f0 array is provided
        if f0 is None or len(f0) == 0:
            raise ValueError("Fundamental frequency array is empty or not provided.")
        
        # Calculate the standard deviation of fundamental frequency
        f0_std = np.nanstd(f0)
        return f0_std
    
    def voiced_ratio(self, voiced_flag):
        # Check if the voiced_flag array is provided
        if voiced_flag is None or len(voiced_flag) == 0:
            raise ValueError("Voiced flag array is empty or not provided.")
        
        # Calculate the ratio of voiced frames
        voiced_ratio = np.mean(voiced_flag)
        return voiced_ratio
    
    def pitch_jitter(self, f0):
        # Check if the f0 array is provided
        if f0 is None or len(f0) == 0:
            raise ValueError("Fundamental frequency array is empty or not provided.")
        
        # Calculate the jitter (pitch variation)
        voiced_f0 = f0[~np.isnan(f0)]
        if len(voiced_f0) < 2:
            return 0.0
        
        diffs = np.abs(np.diff(voiced_f0))
        jitter = np.mean(diffs) / np.mean(voiced_f0) * 100
        return jitter
    
    def pitch_breaks(self, f0):
        # Check if the f0 array is provided
        if f0 is None or len(f0) == 0:
            raise ValueError("Fundamental frequency array is empty or not provided.")
        
        voiced_flag = ~np.isnan(f0) & (f0 > 0)
        return int(np.sum(np.abs(np.diff(voiced_flag.astype(int)))))
    
    def median_F0(self, f0):
        # Check if the f0 array is provided
        if f0 is None or len(f0) == 0:
            raise ValueError("Fundamental frequency array is empty or not provided.")
        
        # Calculate the median fundamental frequency
        median_f0 = np.nanmedian(f0)
        return median_f0
    
    def mean_pitch_slope(self, f0):
        # Check if the f0 array is provided
        if f0 is None or len(f0) == 0:
            raise ValueError("Fundamental frequency array is empty or not provided.")
        
        voiced_f0 = f0[~np.isnan(f0) & (f0 > 0)]
        if len(voiced_f0) < 2:
            return 0.0
    
        slope = np.mean(np.abs(np.diff(voiced_f0)))
        return slope
    
    def voicing_duration(self, voiced_flag):
        # Check if the voiced_flag array is provided
        if voiced_flag is None or len(voiced_flag) == 0:
            raise ValueError("Voiced flag array is empty or not provided.")
        
        # Calculate the voicing duration
        num_voiced_frames = np.sum(voiced_flag)
        duration = (num_voiced_frames * 256) / self.sample_rate
        return duration
    
    def curve_smoothness(self, f0):
        # Check if the f0 array is provided
        if f0 is None or len(f0) == 0:
            raise ValueError("Fundamental frequency array is empty or not provided.")
        
        voiced = ~np.isnan(f0) & (f0 > 0)
        voiced_f0 = f0[voiced]
        indices = np.where(voiced)[0]
    
        if len(voiced_f0) < 4:
            return 0.0
    
        poly = Polynomial.fit(indices, voiced_f0, deg=3)
        r2 = r2_score(voiced_f0, poly(indices))
        return float(r2)