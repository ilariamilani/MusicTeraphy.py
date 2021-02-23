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
        elif (Nsong == 1):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
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
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
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
            run("lxterminal -e omxplayer --vol 600 sounds/GiroGiroTondo1.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/GiroGiroTondo2.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
        elif (Nsong):
            run("lxterminal -e omxplayer --vol 600 sounds/.mp3 &", shell=True)
        elif (Nsong == 0):
            run("lxterminal -e omxplayer --vol 600 sounds/TartarugaSprint.mp3 &", shell=True)
    elif (level == 4): #interaction with the user
        if (Nsong == 0):
            run("lxterminal -e omxplayer --vol 600 sounds/SuonaConMe.mp3 &", shell=True)
        elif (Nsong == 1):
            run("lxterminal -e omxplayer --vol 600 sounds/wow.mp3 &", shell=True)
            run("lxterminal -e omxplayer --vol 600 sounds/CheBravo.mp3 &", shell=True)
        elif (Nsong == 2):
            run("lxterminal -e omxplayer --vol 600 sounds/wow.mp3 &", shell=True)
            run("lxterminal -e omxplayer --vol 600 sounds/Evviva.mp3 &", shell=True)
        elif (Nsong == 3):
            run("lxterminal -e omxplayer --vol 600 sounds/Riproviamo.mp3 &", shell=True)
        elif (Nsong == 4):
            run("lxterminal -e omxplayer --vol 600 sounds/ToccaATe.mp3 &", shell=True)
        elif (Nsong == 5):
            run("lxterminal -e omxplayer --vol 600 sounds/OraToccaAMe.mp3 &", shell=True)



#da mettere in main:
    #defines
    NSongsinLevel = 2 # number of songs in a level
    MA_interactionLevel = 4 #contains the audios for interaction in MA

    #main
    Nid = 0
    songtime = 8
    ActivityLevel = 0
    while ActivityLevel < 4:
        song = 0
        reproduce_song(ActivityLevel, song)
        ActivityLevel += 1
        NSongIdentified = 0
        while song < NSongsinLevel:
            reproduce_song(MA_interactionLevel, 0) #suona con me!
            song += 1
            reproduce_song(ActivityLevel, song)
            if((ActivityLevel == 1) and (song == 1)):
                reproduce_song(MA_interactionLevel, 4) #tocca a te!
            activity = AudioActivity()
            activity.start(id=Nid)
            Nid += 1

            while activity.elapsed_time() < songtime + 2 or activity.silence < 40: #definesongtime #wait in case the child is still playing
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
            if ActivityLevel != 1: #if not certain song that won't repeat the rythm??????????????????????????????????????????????????????????????????????????????????????????????
                if ((ActivityLevel == 1) and (song == 1)):
                    reproduce_song(MA_interactionLevel, 5)  #ora tocca a me!
                song += 1
                reproduce_song(ActivityLevel, song)
                if ((ActivityLevel == 1) and (song == 2)):
                    reproduce_song(MA_interactionLevel, 4)  # tocca a te!
                activity.sequence_identified = 0
                while activity.elapsed_time() < songtime + 2 or activity.silence < 40:  # definesongtime #wait in case the child is still playing
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
            #activity.t.stop()  # timer stop
            if ((ActivityLevel == 1) and (song == 2) and (NSongIdentified > 2)):
                reproduce_song(MA_interactionLevel, 2) #wow evviva!
            print("next round")

        if (song == NSongsinLevel): #end of the level
            if NSongIdentified > 2:
                print("yeeeeeeeeeeeeeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy ready fot the next level")
                reproduce_song(MA_interactionLevel, 1)  # wow, bravo! alla fine dei livelli oppure dopo ogni paio di canzone??
            else:
                print("well well riproviamooo")
                reproduce_song(MA_interactionLevel, 3)  # riproviamo
                ActivityLevel -= 1  # if the child was not able to pass to the next level, the same will be reproposed
        song += 1
        reproduce_song(ActivityLevel, song)


##aggiungi anche luci e movimenti alle espressioni
