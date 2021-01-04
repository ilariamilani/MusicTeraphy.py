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
import json
import math
import os
import wave

import pyaudio

from timer import Timer

from audiohandler import AudioHandler
from playaudio import PlayAudio



AUDIO_FOLDER_PATH = "audio_files/"
FILENAMES = "sampson"

listening = False
reproducing = False


def listen(time):
    listening = True
    # varibili per aprire il microfono
    CHUNK = 1024 * 4
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100

    # Stop for a time as long as the short melody played before (time). I'm giving the time to the patient to reproduce the melody
    t = Timer()
    t.start()
    while t.elapsed_time() < time:
        continue
    t.stop()

    # After waiting I'll check if he's still trying to reproduce the melody or if he's communicating
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=False, frames_per_buffer=CHUNK)
    silence = 0
    while True:
        data = stream.read(CHUNK) #al suo posto posso chiamo metodo audiohandler x capire se ilbimbo parla
        rms = audioop.rms(data, 2)  # quadratic mean of the data
        decibel = 20 * math.log10(rms)  # transforms into db
        if decibel < 65:  # silence
            silence += 1
        else:  # the patient is still speaking/reproducing the melody
            silence = 0
        if silence > 5:  # the patient finished speaking/reproducing the melody
            print("NOT_SPEAKING")
            listening = False # the robot finishes to listen to the patient and can take action
            return
        else:
            print("SPEAKING")





def main():
    print(PlayAudio())
    print(os.path.abspath(__file__))
    print(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # serve per cambiare working directory
    PlayAudio().play_audio("sampson0")



    data = json.load(open("script.json"))
    counter = 0
    while True:
        if not listening: # when the robot is not listening to the patient will reproduce the file
            file_to_play = data["battute"][counter]["filename"]
            PlayAudio().play_audio(file_to_play)
            counter = counter + 1
        if not reproducing: # the robot listens to the patient
            listen(data["battute"][counter]["durata"])


    audio = AudioHandler()
    audio.start()  # open the the stream
    audio.mainloop()  # main operations with librosa

    audio.stop()

if __name__ == "__main__":
    main()


