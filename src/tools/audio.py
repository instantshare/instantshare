import pyaudio
import wave
import threading


# define the amount of data to be read at once from the wave file
_wave_buffer_size = 1024


def play_wave_file(path):
    # open the wave file
    wf = wave.open(path, 'rb')

    # instantiate the PyAudio object
    p = pyaudio.PyAudio()

    # open an output stream with PyAudio
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data from the wave file
    data = wf.readframes(_wave_buffer_size)

    # write all data from the wave file into the output stream
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(_wave_buffer_size)

    # clean up
    stream.stop_stream()
    stream.close()
    p.terminate()


class WaveRecorder:
    """
    Class for recording a wave audio file. Preferably used in a 'with' statement,
    other than that: make sure to call close() afterwards!

    Credit to:
    mabdrabo - https://gist.github.com/mabdrabo/8678538
    """

    def __init__(self, ):
        # sound settings for recording and encoding
        self.audio_format = pyaudio.paInt16
        self.rate = 16000
        self.chunk = 1024
        self.channels = 2

        # open pyaudio input stream to record. Uses default sound device.
        self.audio = pyaudio.PyAudio()
        self.input_stream = self.audio.open(
            format=self.audio_format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            output=False,
            frames_per_buffer=self.chunk
        )

        # buffer for recorded data
        self.audio_data = []

        # initialization for asynchronous workflow
        self.recording = False
        self.record_worker = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def start_record(self):
        """
        Start recording asynchronously. To stop the recording, call stop_record().
        """
        # work for the recording thread
        def record():
            while self.recording:
                # read chunks from input stream and save to buffer
                data = self.input_stream.read(self.chunk)
                self.audio_data.append(data)

        # start the recorder
        self.recording = True
        self.record_worker = threading.Thread(target=record)
        self.record_worker.start()

    def stop_record(self):
        """
        Stop recording. Does nothing if not recording.
        """
        self.recording = False
        self.record_worker.join()

    def reset(self):
        """
        Discard recorded data.
        """
        self.audio_data = []

    def save(self, path):
        """
        Encode the audio data using wave codec and save to file.
        :param path: path of the file
        """
        file = wave.open(path, "wb")
        file.setnchannels(self.channels)
        file.setsampwidth(self.audio.get_sample_size(self.audio_format))
        file.setframerate(self.rate)
        file.writeframes(b''.join(self.audio_data))
        file.close()

    def close(self):
        """
        Close audio stream.
        """
        self.input_stream.close()


# for testing
if __name__ == "__main__":
    with WaveRecorder() as rec:
        rec.start_record()
        input()
        rec.stop_record()
        rec.save("test.wav")
