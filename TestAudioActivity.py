from AudioActivity import AudioActivity
import time
from playaudio import PlayAudio
import audioop
import json
import os

AUDIO_FOLDER_PATH = "audio_files/"
FILENAMES = "sampson"



if __name__ == '__main__':


    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # change working directory
    PlayAudio().play_audio("sampson0")


    activity = AudioActivity()

    activity.start(id=0)

    while activity.t.elapsed_time() < 10:
        time.sleep(1.0)
        if activity.sequence_identified > 0:
            print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            activity.sequence_identified = 0
        else:
            print("Niente")
    print("finito")
    activity.t.stop()
    activity.stop()
