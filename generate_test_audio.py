import numpy as np
import soundfile as sf
from pydub import AudioSegment

# Generate 1 second of 440Hz sine wave
sr = 22050
t = np.linspace(0, 1, int(sr), endpoint=False)
wave = (0.5 * np.sin(2 * np.pi * 440 * t)).astype(np.float32)

# Save as WAV
sf.write("assets/sample.wav", wave, sr)

# Convert WAV to MP3 and FLAC
segment = AudioSegment.from_file("assets/sample.wav", format="wav")
segment.export("assets/sample.mp3", format="mp3")
segment.export("assets/sample.flac", format="flac")

print("✅ WAV, MP3, and FLAC files created in assets/")

# Generate 1 second of white noise
white_noise = (0.5 * np.random.uniform(-1, 1, int(sr))).astype(np.float32)

# Save white noise as WAV
sf.write("assets/white_noise.wav", white_noise, sr)

print("✅ White noise file created in assets/")