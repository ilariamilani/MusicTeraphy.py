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
#print(os.path.abspath(__file__))
#print(os.path.dirname(os.path.abspath(__file__)))
#os.chdir(os.path.dirname(os.path.abspath(__file__)))  # change working directory
#PlayAudio().play("sounds/AttentiallaMusica1.wav")

if __name__ == '__main__':

    answerTime = 8.0
    NSongIdentified = 0
    TIME_OUT_song = 15.0  # maximum time given to reproduce a song

    #prove

    # for letter in 'Python':  # First Example
    #     if letter == 'h':
    #         var = 10  # Second Example
    #         while var > 0:
    #             print(var)
    #             var = var - 1
    #             if var == 5:
    #                 break
    #             print("1")
    #         print("2")
    #     print("3")
    #     print (letter)
    # print("4")

    # a=3
    # b=5
    # c=4
    # d=3
    # e=6
    # f=7
    # for letter in 'Python':
    #     if a == 3:
    #         if b == 5:
    #             if c== 4:
    #                 if d==3:
    #                     if e==6:
    #                         if f==7:
    #                             print(f)
    #                             break
    #
    #                         print(e)
    #                     print(d)
    #                 print(c)
    #             print(b)
    #         print(a)
    #     print(letter)






    PlayAudio().play("sounds/queen.wav")
    activity = AudioActivity()
    activity.sequence_identified = 0
    activity.start(id=4)
    while ((activity.elapsed_time < answerTime or activity.silence < 30) and activity.elapsed_time < TIME_OUT_song):  # definesongtime #wait in case the child is still playing
        time.sleep(1.0)
        if activity.sequence_identified > 0:
            print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo 1")
            NSongIdentified += 1
            activity.sequence_identified = 0
            break
    while activity.silence < 15 and activity.elapsed_time < TIME_OUT_song:  # wait in case the child is still playing
        continue
    activity.stop()

    print("next")

    PlayAudio().play("sounds/queen.wav")
    activity = AudioActivity()
    NSongIdentified = 0
    activity.start(id=11)
    while ((activity.elapsed_time < answerTime or activity.silence < 30) and activity.elapsed_time < TIME_OUT_song):  # definesongtime #wait in case the child is still playing
        time.sleep(1.0)
        if activity.sequence_identified > 0:
            print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo 2")
            NSongIdentified += 1
            activity.sequence_identified = 0
            break
    while activity.silence < 15 and activity.elapsed_time < TIME_OUT_song:  # wait in case the child is still playing
        continue
    activity.stop()

    print("next")

    PlayAudio().play("sounds/BrillaBrillaStellina.wav")
    activity = AudioActivity()
    NSongIdentified = 0
    activity.start(id=4)
    while ((activity.elapsed_time < answerTime or activity.silence < 30) and activity.elapsed_time < TIME_OUT_song):
        time.sleep(1.0)
        if activity.sequence_identified > 0:
            print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            NSongIdentified += 1
            activity.sequence_identified = 0
            break
    while activity.silence < 15 and activity.elapsed_time < TIME_OUT_song: #da mettere in and nel while se funz come or silence < 45
        continue
    activity.stop()

    print("next")

    PlayAudio().play("bravo.wav")
    activity = AudioActivity()
    NSongIdentified = 0
    activity.start(id=11)
    while ((activity.elapsed_time < answerTime or activity.silence < 30) and activity.elapsed_time < TIME_OUT_song):
        time.sleep(1.0)
        if activity.sequence_identified > 0:
            print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            NSongIdentified += 1
            activity.sequence_identified = 0
            break
    while activity.silence < 15 and activity.elapsed_time < TIME_OUT_song:  # da mettere in and nel while se funz come or silence < 45
        continue
    activity.stop()
    PlayAudio().play("sounds/GiroGiroTondo1.wav")




    print("next")





    PlayAudio().play("bravo.wav")
    activity = AudioActivity()
    NSongIdentified = 0
    activity.start(id=3)
    song_time = 4  # durata song
    while activity.elapsed_time < song_time + 2 or activity.silence < 40:
        time.sleep(1.0)
        if activity.sequence_identified > 0:
            print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            NSongIdentified += 1
            activity.sequence_identified = 0
            break
    while activity.silence < 15:  # da mettere in and nel while se funz come or silence < 45
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


