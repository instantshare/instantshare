import pyaudio
import wave

# define the amount of data to be read at once from the wave file
_buffer_size = 1024


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
    data = wf.readframes(_buffer_size)

    # write all data from the wave file into the output stream
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(_buffer_size)

    # clean up
    stream.stop_stream()
    stream.close()
    p.terminate()
