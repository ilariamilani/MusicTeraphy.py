# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# def print_hi(name):
# Use a breakpoint in the code line below to debug your script.
#   print(f'Hi, {name}')
# Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#   print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import audioop
import math

import pyaudio
import wave
import time
import os
import json
from timer import Timer

import numpy as np
import librosa

AUDIO_FOLDER_PATH = "audio_files/"
FILENAMES = "sampson"
active_kid = False
is_listening = False


def listen(time):
    is_listening = True
    # varibili per aprire il microfono
    CHUNK = 1024 * 4
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    # Stop for a time as long as the short melody played before (time). I'm giving the time to the kid to reproduce the melody
    t = Timer()
    t.start()
    while t.elapsed_time() < time:
        continue
    t.stop()

    # After waiting I'll check if he's still trying to reproduce the melody or if he's communicating
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=False, frames_per_buffer=CHUNK)
    silent_kid = 0
    while True:
        data = stream.read(CHUNK)
        rms = audioop.rms(data, 2)  # quadratic mean of the data
        decibel = 20 * math.log10(rms)  # transforms into db
        if decibel < 65:  # silent
            silent_kid += 1
        else:  # the kid is still speaking/reproducing the melody
            silent_kid = 0
        if silent_kid > 5:  # the kid finished speaking/reproducing the melody
            print("NOT_SPEAKING")
            is_listening = False # the robot finishes to listen to the kid and can take action
            return
        else:
            print("SPEAKING")


def play_audio(filename):
    file = AUDIO_FOLDER_PATH + filename + ".wav"  # it builds the string to communicate the file path
    wf = wave.open(file, 'rb')  # opens the audio file
    p = pyaudio.PyAudio()  # initializes pyAudio

    # reproduces the file
    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    # opens the stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    stream.start_stream()
    active_kid = True
    while stream.is_active():
        continue

    print("NOT ACTIVE")
    stream.stop_stream()
    stream.close()
    wf.close()

    p.terminate()
    active_kid = False
    return


class AudioHandler(object):
    def __init__(self):
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 250  # it analyzes around 3 seconds of audio at a time
        self.p = None
        self.stream = None

    def start(self):
        self.p = pyaudio.PyAudio()
        print(self.p.get_default_input_device_info())
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  output=False,
                                  stream_callback=self.callback,
                                  frames_per_buffer=self.CHUNK)

    def stop(self):
        self.stream.close()
        self.p.terminate()

    def callback(self, in_data, frame_count, time_info, flag):
        numpy_array = np.frombuffer(in_data, dtype=np.float32)
        tempo, beat_frames = librosa.beat.beat_track(y=numpy_array, sr=self.RATE)
        onset_env = librosa.onset.onset_strength(y=numpy_array, sr=self.RATE)
        pulse = librosa.beat.plp(onset_envelope=onset_env, sr=self.RATE)
        print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
        print(beat_frames)
        # print("Beat principale : ", np.flatnonzero(librosa.util.localmax(pulse)))
        # beat_times = librosa.frames_to_time(beat_frames, self.RATE)
        # print(beat_times)
        return None, pyaudio.paContinue

    def mainloop(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))  # serve per cambiare working directory
        data = json.load(open("script.json"))
        counter = 0
        while True:
            if not is_listening:
                file_to_play = data["battute"][counter]["filename"]
                play_audio(file_to_play)
                counter = counter + 1
            if not active_kid:
                listen(data["battute"][counter]["durata"])
                while (
                self.stream.is_active()):  # if using button you can set self.stream to 0 (self.stream = 0), otherwise you can use a stop condition
                    continue

def main()
audio = AudioHandler()
audio.start()  # open the the stream
audio.mainloop()  # main operations with librosa
audio.stop()

if __name__ == "__main__":
    main()
