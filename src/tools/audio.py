import pyaudio
import wave

# define the size of data to be read at once from the wave file
CHUNK = 1024

def play_notification():
    # open the wave file
    wf = wave.open("res/notification.wav", 'rb')

    # instantiate the PyAudio object
    p = pyaudio.PyAudio()

    # open an output stream with PyAudio
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # read data from the wave file
    data = wf.readframes(CHUNK)

    # write all data from the wave file into the output stream
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(CHUNK)

    # clean up
    stream.stop_stream()
    stream.close()
    p.terminate()