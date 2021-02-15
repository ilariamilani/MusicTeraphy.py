from AudioActivity import AudioActivity
import time
from subprocess import run


#da mettere in funtions_main
def reproduce_song(level, Nsong):
    if (level == 0):
        run("lxterminal -e omxplayer --vol 600 sounds/AttentiallaMusica.mp3 &", shell=True)
    if (level == 1):
        if (Nsong == 0):
            run("lxterminal -e omxplayer --vol 600 sounds/AttentiallaMusica.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/44Gatti.mp3 &", shell=True)
    elif (level == 2):
        if (Nsong == 0):
            run("lxterminal -e omxplayer --vol 600 sounds/AttentiallaMusica.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
        elif(Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/PulcinoBallerino.mp3 &", shell=True)
    elif (level == 3):
        if (Nsong == 0):
            run("lxterminal -e omxplayer --vol 600 sounds/AttentiallaMusica.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
        elif (Nsong == 0):
            run("lxterminal -e omxplayer --vol 600 sounds/TartarugaSprint.mp3 &", shell=True)


#da mettere in main:
    songtime = 8
    ActivityLevel = 0
    while ActivityLevel < 4:
        song = 0
        reproduce_song(ActivityLevel, song)
        ActivityLevel += 1
        NSongIdentified = 0
        while song < N:
            song += 1
            reproduce_song(ActivityLevel, song)
            activity = AudioActivity()
            activity.start(id=3) #fix thisssssssssssssss

            while activity.t.elapsed_time() < songtime + 2 or activity.silence < 40: #definesongtime #wait in case the child is still playing
                time.sleep(1.0)
                if activity.sequence_identified > 0:
                    print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
                    NSongIdentified += 1
                    activity.sequence_identified = 0
                    break
                else:
                    print("Niente")
            while activity.silence < 15:  #wait in case the child is still playing
                continue
            if ActivityLevel != 1: #(o anche per 1?)
                song += 1
                reproduce_song(ActivityLevel, song)
                while activity.t.elapsed_time() < songtime + 2 or activity.silence < 40:  # definesongtime #wait in case the child is still playing
                    time.sleep(1.0)
                    if activity.sequence_identified > 0:
                        print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
                        NSongIdentified += 1
                        activity.sequence_identified = 0
                        break
                    else:
                        print("Niente")
                while activity.silence < 15:  # wait in case the child is still playing
                    continue
            activity.stop()
            activity.t.stop()  # timer stop
            print("next round")

        if NSongIdentified > 2:
            print("yeeeeeeeeeeeeeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy ready fot the next level")
            #reproduce wow, bravo!. alla fine dei livelli oppure dopo ogni paio di canzone??
        else:
            print("well well riproviamooo")
            #reproduce dai riproviamo!
            ActivityLevel -= 1 #if the child was not able to pass to the next level, the same will be reproposed
        song += 1
        reproduce_song(ActivityLevel, song)
