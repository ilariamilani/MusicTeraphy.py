from AudioActivity import AudioActivity
import time
from timer import Timer
from playaudio import PlayAudio
import audioop
import json

AUDIO_FOLDER_PATH = "audio_files/"
FILENAMES = "sampson"

if __name__ == '__main__':

    activity = AudioActivity()
    NSongIdentified = 0


    #PlayAudio().play_audio("sampson0")
    activity.start(id=0)
    song_time = 4 # durata song
    while activity.t.elapsed_time() < song_time + 2 or activity.silence < 40:
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
    activity.t.stop() #timer stop


    print("2nd turn")

    #activity.actual_sequence = None
    activity.choice_sequence(id=0)
    activity.t.start()
    #activity.start(id=0)
    #PlayAudio().play_audio("sampson0")
    song_time = 10  # durata song
    while activity.t.elapsed_time() < song_time + 2:
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
    activity.t.stop()  # timer stop

    print("3rd turn")

    #activity.initialize_sequences()
    activity.choice_sequence(id=0)
    activity.t.start()
    #activity.start(id=0)
    # PlayAudio().play_audio("sampson0")
    song_time = 10  # durata song
    while activity.t.elapsed_time() < song_time + 2:
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
    activity.t.stop()


    print("4th turn")

    activity.choice_sequence(id=0)
    activity.t.start()
    #activity.start(id=2)
    #PlayAudio().play_audio("sampson0")
    song_time = 10  # durata song
    while activity.t.elapsed_time() < song_time + 2:
        time.sleep(1.0)
        if activity.sequence_identified > 0:
            print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            NSongIdentified += 1
            activity.sequence_identified = 0
            break
        else:
            print("Niente")
    activity.stop()
    activity.t.stop()



    if NSongIdentified > 1 :
        print("yeeeeeeeeeeeeeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy ready fot the next level")
    else :
        print("well well riproviamooo")

    NSongIdentified = 0


    activity.stop()
