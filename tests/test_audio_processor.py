import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np 
from app.audio_processor import AudioProcessor
import pytest


##### Preprocessor Tests #####
def test_load_audio():
    path = "assets/white_noise.wav"
    ap = AudioProcessor(audio_file=path)
    signal, sample_rate = ap.load_audio()
    assert isinstance(signal, np.ndarray), "Signal should be a numpy array"
    assert isinstance(sample_rate, int), "Sample rate should be an integer"
    assert len(signal) > 0, "Signal should not be empty"

def test_normalize_audio():
    signal = np.array([0.5, -0.5, 0.3, -0.3])
    ap = AudioProcessor(signal=signal, sample_rate=16000)
    normalized_signal = ap.normalize_audio()
    assert np.max(np.abs(normalized_signal)) == pytest.approx(1.0, rel=1e-6), "Normalized audio should be within [-1, 1]"

def test_frames_to_array():
    frames = [np.array([1000, -1000], dtype=np.int16).tobytes()]
    ap = AudioProcessor()
    signal = ap.frames_to_array(frames)
    assert isinstance(signal, np.ndarray), "Converted signal should be a numpy array"
    assert signal.dtype == np.float32, "Signal should be converted to float32"
    assert np.all(np.abs(signal)) <= 1.0, "Signal should be scaled"

def test_comp_fund_freq():
    sample_rate = 16000
    duration = 1  # seconds
    t = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    signal = 0.5 * np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave

    ap = AudioProcessor(signal=signal, sample_rate=sample_rate)
    times, f0, voiced_flag, voiced_probs = ap.comp_fund_freq()

    assert isinstance(times, np.ndarray), "Times should be a numpy array"
    assert isinstance(f0, np.ndarray), "Fundamental frequency (f0) should be a numpy array"
    assert isinstance(voiced_flag, np.ndarray), "Voiced flag should be a numpy array"
    assert isinstance(voiced_probs, np.ndarray), "Voiced probabilities should be a numpy array"

    assert len(times) == len(f0) == len(voiced_flag) == len(voiced_probs), "Times and f0 arrays"
    assert np.all(np.isfinite(f0)), "Fundamental frequency (f0) should not contain NaN values"
    assert np.any(voiced_flag), "Voiced flag should contain at least one voiced frame"

##### Stats Tests #####
def test_compute_silence():
    pass

def test_avg_f0():
    pass

def test_f0_range():
    pass

def test_f0_std():
    pass

def test_voiced_ratio():
    pass

def test_pitch_breaks():
    pass

def test_median_f0():
    pass

def test_mean_pitch_slope():
    pass

def test_pitch_jitter():
    f0 = np.array([100, 105, 110, 115, 120, 125, np.nan])
    ap = AudioProcessor(signal=None, sample_rate=16000)
    jitter = ap.pitch_jitter(f0)
    assert isinstance(jitter, float), "Pitch jitter should return a float"
    assert jitter >= 0, "Pitch jitter should be non-negative"

def test_voicing_duration():
    voiced_flag = np.array([1, 0, 1, 1, 0, 1])
    ap = AudioProcessor(signal=None, sample_rate=16000)
    duration = ap.voicing_duration(voiced_flag)
    assert duration >= 0, "Voicing duration should be non-negative"

def test_get_time():
    sr = 16000
    duration = 125  # seconds
    signal = np.zeros(sr * duration)
    ap = AudioProcessor(signal=signal, sample_rate=sr)
    h, m, s = ap.getTime()
    assert h == 0, "Hours should be 0 for 125 seconds"
    assert m == 2, "Minutes should be 2 for 125 seconds"
    assert s == 5, "Seconds should be 5 for 125 seconds"

def test_curve_smoothness():
   f0 = np.array([100, 210, 140, 105, 300, np.nan, 0, 105])
   ap = AudioProcessor(signal = None, sample_rate=16000)
   r2 = ap.curve_smoothness(f0)
   assert isinstance(r2, float), "Curve smoothness should return a float"
   assert 0 <= r2 <= 1, "Curve smoothness should be between 0 and 1"
