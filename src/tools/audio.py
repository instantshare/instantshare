import pyaudio
import wave
import threading
import time

from opuslib import Encoder
from opuslib import constants as opusconst

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


class OpusRecorder:
    """
    Class for recording to an opus file. Preferably used in a 'with' statement,
    other than that: make sure to call close() afterwards!

    Credit to:
    3demax   - https://gist.github.com/3demax/4653037
    mabdrabo - https://gist.github.com/mabdrabo/8678538
    """

    def __init__(self):
        # sound settings for recording and encoding
        self.audio_format = pyaudio.paInt16
        self.rate = 8000
        self.chunk = 50
        self.channels = 2
        self.frame_size = 160
        self.seconds_in_frame = 0.02

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
        Encode the audio data using opus codec and save to file.
        :param path: path of the file
        """
        enc = Encoder(self.rate, self.channels, opusconst.APPLICATION_TYPES_MAP['voip'])
        # TODO: how to encode properly? 3demax's solution seems to raise a TypeError.
        opusdata = enc.encode(b''.join(self.audio_data), self.frame_size)

        # write encoded data to file
        # TODO: opusdata is only a few bytes?
        with open(path, "wb") as file:
            file.write(opusdata)

    def close(self):
        """
        Close audio stream.
        """
        self.input_stream.close()


# for testing
if __name__ == "__main__":
    with OpusRecorder() as rec:
        rec.start_record()
        time.sleep(3)
        rec.stop_record()
        rec.save("test.opus")
