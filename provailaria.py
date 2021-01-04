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
        data = stream.read(CHUNK) #al suo posto posso chiamo metodo audiohandler x capire se ilbimbo parla
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





def main():
    print(os.path.abspath(__file__))
    print(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # serve per cambiare working directory
    PlayAudio().play("sampson0")



    data = json.load(open("script.json"))
    counter = 0
    while True:
        if not is_listening:
            file_to_play = data["battute"][counter]["filename"]
            play_audio(file_to_play)
            counter = counter + 1
        if not active_kid:
            listen(data["battute"][counter]["durata"])


    audio = AudioHandler()
    audio.start()  # open the the stream
    audio.mainloop()  # main operations with librosa

    audio.stop()

if __name__ == "__main__":
    main()

#crea oggetto speaker x suonare
