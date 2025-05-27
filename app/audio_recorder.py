import pyaudio
import threading
import wave

class AudioRecorder:
    def __init__(self, chunkSize=1024, channels=1, sampleRate=44100):
        self.chunkSize = chunkSize
        self.channels = channels
        self.sampleRate = sampleRate
        self.is_recording = False
        self.frames = []
        self.audioInterface = pyaudio.PyAudio()
        self.stream = None
        self.thread = None
    
    def start_recording(self):
        # check if user is already recording
        if self.is_recording:
            return
        
        # set recording equal to True
        self.is_recording = True

        # Create a new thread for recording and init stream
        self.stream = self.audioInterface.open(format=pyaudio.paInt16,
                                      channels=self.channels,
                                      rate=self.sampleRate,
                                      input=True,
                                      frames_per_buffer=self.chunkSize)
        
        self.thread = threading.Thread(target=self._record)
        self.thread.start()
    
    def _record(self):
        # try to record audio date to frames, print error if it occurs
        try:
            while self.is_recording:
                data = self.stream.read(self.chunkSize)
                self.frames.append(data)
        except Exception as e:
            print(f"Error during recording: {e}")
            self.is_recording = False

    def stop_recording(self):

        self.is_recording = False

        if self.thread:
            self.thread.join()
            self.thread = None

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

        self.audioInterface.terminate()

    def save_recording(self, output_file):
        # check that there are frames to save
        if not self.frames:
            print("No audio frames to save.")
            return
        
        # save as wave file
        wave_file = wave.open(output_file, 'wb')
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(self.audioInterface.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(self.sampleRate)
        wave_file.writeframes(b''.join(self.frames))
        wave_file.close()

    def reset(self):
        # Reset the recorder state
        self.frames = []
        self.is_recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        if self.thread:
            self.thread.join()
            self.thread = None
        self.audioInterface.terminate()
        self.audioInterface = pyaudio.PyAudio()