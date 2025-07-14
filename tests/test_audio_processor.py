import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np 
from app.audio_processor import AudioProcessor
import pytest



def test_curve_smoothness():
   f0 = np.array([100, 210, 140, 105, 300, np.nan, 0, 105])
   ap = AudioProcessor(signal = None, sample_rate=16000)
   r2 = ap.curve_smoothness(f0)
   assert isinstance(r2, float), "Curve smoothness should return a float"
   assert 0 <= r2 <= 1, "Curve smoothness should be between 0 and 1"

def test_voicing_duration():
    voiced_flag = np.array([1, 0, 1, 1, 0, 1])
    ap = AudioProcessor(signal=None, sample_rate=16000)
    duration = ap.voicing_duration(voiced_flag)
    assert duration >= 0, "Voicing duration should be non-negative"

def test_normalize_audio():
    signal = np.array([0.5, -0.5, 0.3, -0.3])
    ap = AudioProcessor(signal=signal, sample_rate=16000)
    normalized_signal = ap.normalize_audio()
    assert np.max(np.abs(normalized_signal)) == pytest.approx(1.0, rel=1e-6), "Normalized audio should be within [-1, 1]"

def test_pitch_jitter():
    f0 = np.array([100, 105, 110, 115, 120, 125, np.nan])
    ap = AudioProcessor(signal=None, sample_rate=16000)
    jitter = ap.pitch_jitter(f0)
    assert isinstance(jitter, float), "Pitch jitter should return a float"
    assert jitter >= 0, "Pitch jitter should be non-negative"

def test_get_time():
    sr = 16000
    duration = 125  # seconds
    signal = np.zeros(sr * duration)
    ap = AudioProcessor(signal=signal, sample_rate=sr)
    h, m, s = ap.getTime()
    assert h == 0, "Hours should be 0 for 125 seconds"
    assert m == 2, "Minutes should be 2 for 125 seconds"
    assert s == 5, "Seconds should be 5 for 125 seconds"

