import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np 
from app.audio_processor import AudioProcessor
import pytest

##### Test Audio #####
def generate_test_signal(frequency=440, duration=1.0, sample_rate=44100):
    """Generate a test signal (sine wave) for testing purposes."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    signal = 0.5 * np.sin(2 * np.pi * frequency * t)  # Amplitude of 0.5
    return signal, sample_rate

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
    signal, sample_rate = generate_test_signal()
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
    signal, sample_rate = generate_test_signal()
    ap = AudioProcessor(signal=signal, sample_rate=sample_rate)
    silence_percentage = ap.compute_silence()
    assert isinstance(silence_percentage, float), "Silence percentage should be a float"
    assert 0 <= silence_percentage <= 100, "Silence percentage should be between 0 and 100"

def test_avg_f0():
    f0 = np.array([100, 200, 300, 400, 500, np.nan])
    ap = AudioProcessor(signal=None, sample_rate=16000)
    avg_f0 = ap.avg_fundamental_freq(f0)
    assert isinstance(avg_f0, float), "Average fundamental frequency should return a float"
    assert not np.isnan(avg_f0), "Average fundamental frequency should not be NaN"
    assert np.nanmin(f0) <= avg_f0 <= np.nanmax(f0), "Average fundamental frequency should be within the range of f0 values"

def test_f0_range():
    f0 = np.array([100, 200, 300, 400, 500, np.nan])
    ap = AudioProcessor(signal=None, sample_rate=16000)
    f0_min, f0_max = ap.f0_range(f0)
    assert isinstance(f0_min, float), "F0 range should return a float"
    assert isinstance(f0_max, float), "F0 range should return a float"
    assert f0_min >= 0, "F0 range should be non-negative"
    assert f0_max >= f0_min, "F0 max should be greater than or equal to F0 min"
    assert np.isclose(f0_min, np.nanmin(f0)), "F0 min should match the minimum of f0 array"
    assert np.isclose(f0_max, np.nanmax(f0)), "F0 max should match the maximum of f0 array"

def test_f0_std():
    signal, sample_rate = generate_test_signal()
    ap = AudioProcessor(signal=signal, sample_rate=sample_rate)
    times, f0, voiced_flag, voiced_probs = ap.comp_fund_freq()
    f0_std = ap.f0_std_dev(f0)
    assert isinstance(f0_std, float), "F0 standard deviation should return a float"
    assert f0_std >= 0, "F0 standard deviation should be non-negative"
    assert not np.isnan(f0_std), "F0 standard deviation should not be NaN"
    assert np.isclose(f0_std, np.nanstd(f0)), "F0 standard deviation should match the standard deviation of f0 array"

def test_voiced_ratio():
    signal, sample_rate = generate_test_signal()
    ap = AudioProcessor(signal=signal, sample_rate=sample_rate)
    times, f0, voiced_flag, voiced_probs = ap.comp_fund_freq()
    voiced_ratio = ap.voiced_ratio(voiced_flag)
    assert isinstance(voiced_ratio, float), "Voiced ratio should return a float"
    assert 0 <= voiced_ratio <= 1, "Voiced ratio should be between 0 and 1"
    assert not np.isnan(voiced_ratio), "Voiced ratio should not be NaN"
    assert np.isclose(voiced_ratio, np.mean(voiced_flag)), "Voiced ratio should match the mean of voiced_flag array"

def test_pitch_breaks():
    signal, sample_rate = generate_test_signal()
    ap = AudioProcessor(signal=signal, sample_rate=sample_rate)
    times, f0, voiced_flag, voiced_probs = ap.comp_fund_freq()
    breaks = ap.pitch_breaks(f0)
    assert isinstance(breaks, int), "Pitch breaks should return an integer"
    assert breaks >= 0, "Pitch breaks should be non-negative"
    assert breaks <= (len(f0) - 1), "Pitch breaks should not exceed the length of f0 array minus one"

def test_median_f0():
    signal, sample_rate = generate_test_signal()
    ap = AudioProcessor(signal=signal, sample_rate=sample_rate)
    times, f0, voiced_flag, voiced_probs = ap.comp_fund_freq()
    median_f0 = ap.median_F0(f0)
    assert isinstance(median_f0, float), "Median F0 should return a float"
    assert not np.isnan(median_f0), "Median F0 should not be NaN"
    assert median_f0 >= 0, "Median F0 should be non-negative"
    assert np.isclose(median_f0, np.nanmedian(f0)), "Median F0 should match the median of f0 array"

def test_mean_pitch_slope():
    signal, sample_rate = generate_test_signal()
    ap = AudioProcessor(signal=signal, sample_rate=sample_rate)
    times, f0, voiced_flag, voiced_probs = ap.comp_fund_freq()
    slope = ap.mean_pitch_slope(f0)
    assert isinstance(slope, float), "Mean pitch slope should return a float"
    assert not np.isnan(slope), "Mean pitch slope should not be NaN"
    assert slope >= 0, "Mean pitch slope should be non-negative due to calculating absolute values"
    assert np.isclose(slope, np.mean(np.abs(np.diff(f0))), rtol=1e-5), "Mean pitch slope should match the mean of absolute differences in f0 array"

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
