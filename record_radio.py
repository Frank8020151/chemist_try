import wave
import threading

import pyaudio


class RecordRadio:
    def __init__(self, outPutFile, format=pyaudio.paInt16, channels=1,chunk=1024 , rate=44100):
        self.format = format
        self.channels = channels
        self.chunk = chunk
        self.rate = rate
        self.outPutFile = outPutFile
        self.p = None
        self.stream = None
        self.wavFile = None
        self.start: bool = False

    def start_record(self):
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            frames_per_buffer=self.chunk,
            input=True,
        )
        self.wavFile = wave.open(self.outPutFile, "wb")
        self.wavFile.setnchannels(self.channels)
        self.wavFile.setsampwidth(self.p.get_sample_size(self.format))
        self.wavFile.setframerate(self.rate)
        self.start = True
        thd = threading.Thread(target=self.record)
        thd.start()

    def record(self):
        while self.start:
            self.wavFile.writeframes(self.stream.read(self.chunk))

    def stop_record(self):
        self.start = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.wavFile.close()
