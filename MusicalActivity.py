from AudioActivity import AudioActivity
import time
import os
from subprocess import run
from audioplayer import PlayAudio


#print(os.path.abspath(__file__))
#print(os.path.dirname(os.path.abspath(__file__)))
#os.chdir(os.path.dirname(os.path.abspath(__file__)))  # change working directory

#da mettere in funtions_main
def reproduce_song(level, Nsong):
    if (level == 0): #interaction with the user
        if (Nsong == 0):
            PlayAudio().play("sounds/SuonaConMe.wav")
        elif (Nsong == 1):
            PlayAudio().play("sounds/wow.wav")
            PlayAudio().play("sounds/CheBravo.wav")
        elif (Nsong == 2):
            PlayAudio().play("sounds/wow.wav")
            PlayAudio().play("sounds/Evviva.wav")
        elif (Nsong == 3):
            PlayAudio().play("sounds/Riproviamo.wav")
        elif (Nsong == 4):
            PlayAudio().play("sounds/ToccaATe.wav")
        elif (Nsong == 5):
            PlayAudio().play("sounds/OraToccaAMe.wav")
        elif (Nsong == 6):
            PlayAudio().play("sounds/CantaConMe.wav")
    if (level == 1):
        if (Nsong == 0):
            PlayAudio().play("sounds/AttentiallaMusica1.wav")
        elif (Nsong == 1):
            PlayAudio().play("sounds/tatittitata.wav")
        elif (Nsong == 2):
            PlayAudio().play("sounds/tatittitata.wav")
        elif (Nsong == 3):
            PlayAudio().play("sounds/tichetà.wav")
        elif (Nsong == 4):
            PlayAudio().play("sounds/tichetà.wav")
        elif (Nsong == 5):
            PlayAudio().play("sounds/opopop.wav")
        elif (Nsong == 6):
            PlayAudio().play("sounds/opopop.wav")
        elif (Nsong == 7):
            PlayAudio().play("sounds/founding.wav")
            #PlayAudio().play("sounds/44Gatti.wav.waw")
    elif (level == 2):
        if (Nsong == 0):
            PlayAudio().play("sounds/AttentiallaMusica2.wav")
        elif (Nsong == 1):
            PlayAudio().play("sounds/Snappy_R2D2.wav")
        elif (Nsong == 2):
            PlayAudio().play("sounds/Snappy_R2D2.wav")
        elif (Nsong == 3):
            PlayAudio().play("sounds/queen.wav")
        elif (Nsong == 4):
            PlayAudio().play("sounds/queen.wav")
        elif (Nsong == 5):
            PlayAudio().play("sounds/queen.wav")
        elif (Nsong == 6):
            PlayAudio().play("sounds/queen.wav")
        elif(Nsong == 7):
            PlayAudio().play("sounds/founding.wav")
            #PlayAudio().play("sounds/PulcinoBallerino.waw")
    elif (level == 3):
        if (Nsong == 0):
            PlayAudio().play("sounds/AttentiallaMusica3.wav")
        elif (Nsong == 1):
            PlayAudio().play("sounds/GiroGiroTondo1.wav")
        elif (Nsong == 2):
            PlayAudio().play("sounds/GiroGiroTondo2.wav")
        elif (Nsong == 3):
            PlayAudio().play("sounds/Snappy_R2D2.wav")
        elif (Nsong == 4):
            PlayAudio().play("sounds/Snappy_R2D2.wav")
        elif (Nsong == 5):
            PlayAudio().play("sounds/Snappy_R2D2.wav")
        elif (Nsong == 6):
            PlayAudio().play("sounds/Snappy_R2D2.wav")
        elif (Nsong == 7):
            PlayAudio().play("sounds/founding.wav")
            #PlayAudio().play("sounds/TartarugaSprint.waw")
    #elif (level == 4):




#da mettere in main program:

#defines
NSongsinLevel = 7 # number of songs in a level
MA_interactionLevel = 0 #contains the audios for interaction in MA

if __name__ == '__main__':

    Nid = 0
    answerTime = 8.0
    ActivityLevel = 1
    while ActivityLevel < 4:
        song = 0
        #reproduce_song(ActivityLevel, song) #Attenti alla musica!
        NSongIdentified = 0
        while song < NSongsinLevel:
            song += 1
            if song == NSongsinLevel:
                print("end of level")
                break
            if (((song % 2) != 0) and (song != NSongsinLevel)): #every time a new song is played (odd number)(every song is reproduced twice)
                reproduce_song(MA_interactionLevel, 0) #suona con me!
            if song == NSongsinLevel:
                reproduce_song(MA_interactionLevel, 6)  # canta con me!
            if song == 2:
                reproduce_song(MA_interactionLevel, 5)  # ora tocca a me!
            reproduce_song(ActivityLevel, song)
            if song == 1:
                reproduce_song(MA_interactionLevel, 4) #tocca a te!

            # BEAT RECOGNITION
            activity = AudioActivity()
            activity.start(id=Nid)
            print("id=")
            print(Nid)
            if (song % 2) != 0:  # every time a new song is played (odd number)(every song is reproduced twice)
                Nid += 1
            while activity.elapsed_time < answerTime or activity.silence < 40: #definesongtime #wait in case the child is still playing
                time.sleep(1.0)
                if activity.sequence_identified > 0:
                    print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
                    NSongIdentified += 1
                    activity.sequence_identified = 0
                    time.sleep(1.5)
                    break
                #else:
                    #print("Niente")
            while activity.silence < 15:  #wait in case the child is still playing
                continue
            activity.stop()
            if ( ((song % 2) == 0) and (NSongIdentified > 0)): #at least 1 song over 2 has been correctly reproduced
                reproduce_song(MA_interactionLevel, 2) #wow evviva!
            print(".")
            print("next song in the same level")
            print(".")
        # LEVEL CONCLUDED: checking for results. if 50% of the activity is correct: next level. else: repeat the level
        if (song == NSongsinLevel): #end of the level
            if NSongIdentified >= ((NSongsinLevel - 1) // 2): #50% correct
                print(".")
                print("yeeeeeeeeeeeeeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy ready fot the next level")
                print(".")
                reproduce_song(MA_interactionLevel, 1)  # wow, bravo! reproduced when the level has been passed
                reproduce_song(ActivityLevel, song)
                ActivityLevel += 1
            else:
                print(".")
                print("well well riproviamooo")
                print(".")
                reproduce_song(MA_interactionLevel, 3)  # riproviamo
                # if the child was not able to pass to the next level, the same will be reproposed
                Nid -= ((NSongsinLevel - 1) // 2)
        song += 1
        reproduce_song(ActivityLevel, song) #Z???????????????????????????????????????????????????????????????????????????????


##aggiungi anche luci e movimenti alle espressioni
