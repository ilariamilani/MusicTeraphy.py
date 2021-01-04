import pyaudio
import wave
import sys

class PlayAudio(object):


    def __init__(self):
        self.FORMAT = pyaudio.paFloat32
        self.AUDIO_FOLDER_PATH = "audio_files/"
        self.CHUNK = 1024
        #self.reproducing = False


    def play_audio(self, filename):
        file = self.AUDIO_FOLDER_PATH + filename + ".wav"  # it builds the string to communicate the file path
        wf = wave.open(file, 'rb')  # opens the audio file
        p = pyaudio.PyAudio()  # initializes pyAudio

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        reproducing = True
        data = wf.readframes(self.CHUNK)
        while data != '':
            stream.write(data)
            data = wf.readframes(self.CHUNK)
        stream.close()
        wf.close()
        p.terminate()
        reproducing = False
        return

