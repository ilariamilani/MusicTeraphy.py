from AudioActivity import AudioActivity
import time
import os
import random
from subprocess import run
from audioplayer import PlayAudio


#print(os.path.abspath(__file__))
#print(os.path.dirname(os.path.abspath(__file__)))
#os.chdir(os.path.dirname(os.path.abspath(__file__)))  # change working directory

bravo = ["audioYolk/bravissimo.wav", "audioYolk/wowchebravo.wav", "audioYolk/evviva.wav"]
riprova = ["audioYolk/riproviamo.wav", "audioYolk/dairiprova.wav", "audioYolk/daidinuovo.wav", "audioYolk/provaancora.wav"]
suona = ["audioYolk/battiatempo.wav", "audioYolk/suonaaritmo.wav", "audioYolk/daivaiatempo.wav"]
canta = ["audioYolk/cantaconme.wav", "audioYolk/cantiamo.wav"]
pain = ["audioYolk/ahiachemale.wav", "audioYolk/ahiabasta.wav", "audioYolk/mifaimale.wav"]
angry = ["audioYolk/basta.wav", "audioYolk/nomaestra.wav", "audioYolk/bastacattivo.wav", "audioYolk/noooo.wav"]
sad = ["audioYolk/oooouuuuu.wav", "audioYolk/uuuuuhhhhhh.wav", "audioYolk/nodai.wav"]
happy = ["audioYolk/ohchebello.wav", "audioYolk/wowsonofelice.wav", "audioYolk/evviva.wav"]
found = ["audioYolk/eccoti.wav", "audioYolk/eccotigiochiamo.wav", "audioYolk/ohwowseiqui.wav", "audioYolk/seiqui.wav", "audioYolk/tihotrovatogiocaconme.wav"]
notfound = ["audioYolk/ahnonseitudovesei.wav", "audioYolk/ahnonseitudoveseifattisentire.wav", "audioYolk/ohnomaeunoggettodovesei.wav", "audioYolk/ahnonontitrovo.wav"]
dovesei = ["audioYolk/doveseifunny.wav", "audioYolk/dovesei.wav", "audioYolk/doveseigiochiamo.wav", "audioYolk/fattisentirefunny.wav", "audioYolk/fattisentire.wav", "audioYolk/doveseigiochiamofunny.wav", "audioYolk/ehiciseifunny.wav", "audioYolk/ehicisei.wav", "audioYolk/ehiciseifunny2.wav"]
giochiamo = ["audioYolk/giocaconme.wav", "audioYolk/giochiamo.wav", "audioYolk/vuoigiocareconme.wav", "audioYolk/giochiamoinsieme.wav"]
myturn = ["audioYolk/oraascolta.wav", "audioYolk/oratoccaame.wav", "audioYolk/toccaame.wav"]
yourturn = ["audioYolk/oratoccaate.wav", "audioYolk/adessosuonatu.wav", "audioYolk/oraprovatu.wav", "audioYolk/toccaate.wav", "audioYolk/provatu.wav"]
nongioca = ["audioYolk/nonvuoigiocareconme.wav", "audioYolk/nontipiacequestogioco.wav", "audioYolk/nonsuoniconme.wav"]
nextlevel = ["audioYolk/prontoperilprossimolivello.wav", "audioYolk/orasaraunpopiudifficile.wav"]


#da mettere in funtions_main
def reproduce_song(level, Nsong):
    if (level == 0): #interaction with the user
        if (Nsong == 0):
            audio = random.choice(suona)
            PlayAudio().play(audio)
        elif (Nsong == 1):
            audio = random.choice(bravo)
            PlayAudio().play(audio)
        elif (Nsong == 2):
            audio = random.choice(happy)
            PlayAudio().play(audio)
        elif (Nsong == 3):
            audio = random.choice(riprova)
            PlayAudio().play(audio)
        elif (Nsong == 4):
            audio = random.choice(yourturn)
            PlayAudio().play(audio)
        elif (Nsong == 5):
            audio = random.choice(myturn)
            PlayAudio().play(audio)
        elif (Nsong == 6):
            audio = random.choice(canta)
            PlayAudio().play(audio)
        elif (Nsong == 7):
            audio = random.choice(sad)
            PlayAudio().play(audio)
        elif (Nsong == 8):
            audio = random.choice(nongioca)
            PlayAudio().play(audio)
        elif (Nsong == 9):
            audio = random.choice(nextlevel)
            PlayAudio().play(audio)
        elif (Nsong == 10):
            audio = random.choice(giochiamo)
            PlayAudio().play(audio)
    if (level == 1):
        if (Nsong == 0):
            PlayAudio().play("sounds/AttentiallaMusica1.wav")
        elif (Nsong == 1):
            PlayAudio().play("sounds/dindondan.wav")
        elif (Nsong == 2):
            PlayAudio().play("sounds/dindondan.wav")
        elif (Nsong == 3):
            PlayAudio().play("sounds/ticheta.wav")
        elif (Nsong == 4):
            PlayAudio().play("sounds/ticheta.wav")
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
            PlayAudio().play("sounds/TwinkleTwinkleLittleStar.wav")
        elif (Nsong == 2):
            PlayAudio().play("sounds/TwinkleTwinkleLittleStar.wav")
        elif (Nsong == 3):
            PlayAudio().play("sounds/queen.wav")
        elif (Nsong == 4):
            PlayAudio().play("sounds/queen.wav")
        elif (Nsong == 5):
            PlayAudio().play("sounds/BrillaBrillaStellina.wav")
        elif (Nsong == 6):
            PlayAudio().play("sounds/BrillaBrillaStellina.wav")
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
            PlayAudio().play("sounds/fraMartino.wav")
        elif (Nsong == 4):
            PlayAudio().play("sounds/SuonaLeCampane.wav")
        elif (Nsong == 5):
            PlayAudio().play("sounds/vecchiaFattoria1.wav")
        elif (Nsong == 6):
            PlayAudio().play("sounds/vecchiaFattoria2.wav")
        elif (Nsong == 7):
            PlayAudio().play("sounds/founding.wav")
            #PlayAudio().play("sounds/TartarugaSprint.waw")




#da mettere in main program:

#defines
NSongsinLevel = 7 # number of songs in a level
MA_interactionLevel = 0 #contains the audios for interaction in MA

if __name__ == '__main__':

    TOTSongsIdentified = 0
    try_again = 0
    Nid = 0
    AnswerTime = 9.0  # minimum time given to reproduce a song
    TIME_OUT_SONG = 12.0  # maximum time given to reproduce a song
    answerTime = 0
    TIME_OUT_song = 0
    #correctSong = 0
    ActivityLevel = 1
    identification_time = 0
    while ActivityLevel < 4:
        song = 0
        reproduce_song(ActivityLevel, song) #Attenti alla musica!
        NSongIdentified = 0
        if ActivityLevel == 1:
            answerTime = AnswerTime - 3.0
            TIME_OUT_song = TIME_OUT_SONG - 3.0
        elif ActivityLevel == 2:
            answerTime = AnswerTime
            TIME_OUT_song = TIME_OUT_SONG
        while song < NSongsinLevel:
            song += 1
            if song == NSongsinLevel:
                print("end of level")
                break
            reproduce_song(MA_interactionLevel, 5)  # ora tocca a me!
            reproduce_song(ActivityLevel, song)
            reproduce_song(MA_interactionLevel, 4) #tocca a te!
            #if song == 1: #before every firts song of the level
            if (((song % 2) != 0) and (song != NSongsinLevel)): #every time a new song is played (odd number)(every song is reproduced twice)
                reproduce_song(MA_interactionLevel, 0) #suona con me!
            # BEAT RECOGNITION
            activity = AudioActivity()
            activity.start(id=Nid)
            print("id=")
            print(Nid)
            if (song % 2) != 0:  # every time a new song is played (odd number)(every song is reproduced twice)
                Nid += 1
                #correctSong = 0
            while ((activity.elapsed_time < answerTime or activity.silence < 15) and activity.elapsed_time < TIME_OUT_song): #wait in case the child is still playing (making noises)
                time.sleep(1.0)
                if activity.sequence_identified > 0:
                    print("Bravoooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
                    NSongIdentified += 1
                    time.sleep(1.0)
                    identification_time = time.perf_counter()
                    break
            if activity.sequence_identified > 0:
                while activity.silence < 15 and (identification_time + 1.5 > activity.elapsed_time):  #wait in case the child is still playing
                    continue
            activity.stop()
            # reaction of the robot to the 2 songs just performed
            #correctSong = correctSong + activity.sequence_identified
            if (activity.sequence_identified == 0) and (activity.other_activity > 20 or activity.Nbeat < 3):
                print("the child is not performing the activity")
                reproduce_song(MA_interactionLevel, 7)  # sad :(
                reproduce_song(MA_interactionLevel, 8)  # not playing
                reproduce_song(MA_interactionLevel, 10) #giochiamo!
            elif activity.sequence_identified > 0: # song correctly reproduced
                print("song well reproduced by the child")
                reproduce_song(MA_interactionLevel, 1) #wow bravo!
                child_not_involved = 0
                if ActivityLevel != 3 and (song % 2) != 0:  # not reproducing the same song if the child altready reproduced it well
                    song += 1
                    NSongIdentified += 1
            else:
                #if (song % 2) == 0 and correctSong < 1: #if not even 1 song over 2 has been correctly reproduced
                print("song NOT well reproduced by the child")
                reproduce_song(MA_interactionLevel, 3)  # riproviamo
            print(".")
            print("next song in the same level")
            print(".")
            activity.sequence_identified = 0
        # LEVEL CONCLUDED: checking for results. if 50% of the activity is correct: next level. else: repeat the level
        if (song == NSongsinLevel): #end of the level
            if NSongIdentified >= ((NSongsinLevel - 1) // 2): #50% correct
                print(".")
                print("yeeeeeeeeeeeeeyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy ready fot the next level")
                print(".")
                reproduce_song(MA_interactionLevel, 2)  # wow, evviva!
                reproduce_song(MA_interactionLevel, 6)  # canta con me!
                reproduce_song(ActivityLevel, song) # long song
                try_again = 0
                ActivityLevel += 1
                if ActivityLevel < 4:
                    reproduce_song(MA_interactionLevel, 9)  # level has been passed
            else:
                print(".")
                print("well well riproviamooo")
                print(".")
                reproduce_song(MA_interactionLevel, 3)  # riproviamo
                try_again += 1
                if try_again < 3:
                    # if the child was not able to pass to the next level, the same will be reproposed
                    Nid -= ((NSongsinLevel - 1) // 2)
                else:  # if the level has been proposed too many times, pass to the next level
                    ActivityLevel += 1  # next level
                    if ActivityLevel < 4:
                        reproduce_song(MA_interactionLevel, 9)  # level has been passed
            TOTSongsIdentified = TOTSongsIdentified + NSongIdentified
            print (TOTSongsIdentified)


##aggiungi anche luci e movimenti alle espressioni
