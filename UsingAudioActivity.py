from AudioActivity import AudioActivity
import time
from timer import Timer
from audioplayer import PlayAudio
import audioop
import json
import wave
import numpy as np
import os

#AUDIO_FOLDER_PATH = "sounds/"
print(os.path.abspath(__file__))
print(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))  # change working directory
#PlayAudio().play("sounds/AttentiallaMusica1.wav")

if __name__ == '__main__':

    activity = AudioActivity()
    NSongIdentified = 0

    i=3

    PlayAudio().play("bravo.wav")
    activity.start(id=i)
    song_time = 4 # durata song
    while activity.elapsed_time < song_time + 2 or activity.silence < 40:
        time.sleep(1.0)
        if activity.sequence_identified > 0:
            print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            NSongIdentified += 1
            activity.sequence_identified = 0
            #activity.p = None
            #activity.stream = None
            break
        else:
            print("Niente")
    while activity.silence < 15: #da mettere in and nel while se funz come or silence < 45
        continue

    PlayAudio().play("bravo.wav")

    while activity.elapsed_time < song_time + 2 or activity.silence < 40:
        time.sleep(1.0)
        if activity.sequence_identified > 0:
            print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            NSongIdentified += 1
            activity.sequence_identified = 0
            #activity.p = None
            #activity.stream = None
            break
        else:
            print("Niente")
    while activity.silence < 15: #da mettere in and nel while se funz come or silence < 45
        continue
    #activity.stop()


    print(".")
    print("2nd turn")
    print(".")
    #PlayAudio().play("bravo.wav")
    #activity.actual_sequence = None
    activity.choice_sequence(2)
    #activity.start(id=0)
    song_time = 10  # durata song
    while activity.elapsed_time < song_time + 2:
        time.sleep(1.0)
        if activity.sequence_identified > 0:
            print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            NSongIdentified += 1
            activity.sequence_identified = 0
            #activity.p = None
            #activity.stream = None
            break
        else:
            print("Niente")
    while activity.silence < 10:  # da mettere o no?
        continue
    print("stop: next")
    #activity.stop()

    print("3rd turn")
    #PlayAudio().play("bravo.wav")
    #activity.initialize_sequences()
    activity.choice_sequence(id=0)
    #activity.start(id=0)
    song_time = 10  # durata song
    while activity.elapsed_time < song_time + 2:
        time.sleep(1.0)
        if activity.sequence_identified > 0:
            print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            NSongIdentified += 1
            activity.sequence_identified = 0
            # activity.p = None
            # activity.stream = None
            break
        else:
            print("Niente")

    #activity.stop()


    print("4th turn")
    #PlayAudio().play("bravo.wav")
    activity.choice_sequence(0)
    #activity.start(id=2)
    song_time = 10  # durata song
    while activity.elapsed_time < song_time + 2:
        time.sleep(1.0)
        if activity.sequence_identified > 0:
            print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            NSongIdentified += 1
            activity.sequence_identified = 0
            break
        else:
            print("Niente")



    if NSongIdentified > 1 :
        print("yeeeeeeeeeeeeeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy ready fot the next level")
    else :
        print("well well riproviamooo")

    NSongIdentified = 0


    activity.stop()


    #PlayAudio().play("bravo.wav")
    activity = AudioActivity()

    activity.start(id=0)
    song_time = 4  # durata song
    while activity.elapsed_time < song_time + 2 or activity.silence < 40:
        time.sleep(1.0)
        if activity.sequence_identified > 0:
            print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            NSongIdentified += 1
            activity.sequence_identified = 0
            # activity.p = None
            # activity.stream = None
            break
        else:
            print("Niente")
    while activity.silence < 15:  # da mettere in and nel while se funz come or silence < 45
        continue
    # activity.stop()
    activity.stop()



    #PlayAudio().play("bravo.wav")
    activity2 = AudioActivity()
    NSongIdentified = 0

    activity2.start(id=0)
    song_time = 4  # durata song
    while activity2.elapsed_time < song_time + 2 or activity2.silence < 40:
        time.sleep(1.0)
        if activity2.sequence_identified > 0:
            print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            NSongIdentified += 1
            activity2.sequence_identified = 0
            # activity.p = None
            # activity.stream = None
            break
        else:
            print("Niente")
    while activity2.silence < 15:  # da mettere in and nel while se funz come or silence < 45
        continue
    # activity.stop()
    activity2.stop()


