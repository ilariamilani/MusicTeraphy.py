#!/usr/bin/env python3

import argparse
import sys
import os
import time
import subprocess
from datetime import datetime
from AudioActivity import AudioActivity
from pynput import keyboard
import functions_main
import connections_arduinos as arduino #new_user_fun
import logging

logging.basicConfig(format="[ %(levelname)s ] %(message)s",
                    level=logging.INFO,
                    stream=sys.stdout)
log = logging.getLogger()


def build_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m_od", "--model_od", type=str, default= "models/ssdlite_mobilenet_v2/FP16/ssdlite_mobilenet_v2.xml",
                        help="path to model of object detector to be infered in NCS2, in xml format")

    parser.add_argument("-m_hpe", "--model_hpe", default="models/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite", type=str,
                            help="path to model of human pose estimator to be infered in Google Coral TPU, TFlite model. Assigned one by default")

    parser.add_argument("-i", "--input", type=str, nargs='+', default='0', help="path to video or image/images")
    parser.add_argument("-d", "--device", type=str, default='MYRIAD', required=False,
                        help="Specify the target to infer on CPU, GPU, or MYRIAD")
    parser.add_argument("--person_label", type=int, required=False, default=1, help="Label of class person for detector")
    parser.add_argument("--modality", type=str, default="Multi", help="Define the modality of representation of the output. Set single to visualize the skeleton of the main actor")
    parser.add_argument("--no_show", help='Optional. Do not display output.', action='store_true')
    return parser


def on_press(key):
    global child_action
    global MusicalActivity
    global receiveAction
    global good_interaction
    try:
        print("{0} Pressed".format(key.char))        
        if key.char == ("a"):
            child_action = "touch"
            MusicalActivity = False
            receiveAction = True
            good_interaction = False
        elif key.char == ("s"):
            child_action = "push"
            MusicalActivity = False
            receiveAction = True
            good_interaction = False
        elif key.char == ("d"):
            child_action = "hit"
            MusicalActivity = False
            receiveAction = True
            good_interaction = False
        elif key.char == ("f"):
            child_action = "hug"
            MusicalActivity = False
            receiveAction = True
            good_interaction = True
        elif key.char == ("g"):
            child_action = "strongHug"
            MusicalActivity = False
            receiveAction = True
            good_interaction = False
        elif key.char == ("h"):
            child_action = "none"
            MusicalActivity = False
            receiveAction = True
            good_interaction = False
        elif key.char == ("j"):
            child_action = "activity"
            MusicalActivity = False
            receiveAction = True
            good_interaction = False
        elif key.char == ("k"):
            child_action = "notfound" # if the robot identifies the child in an object
            MusicalActivity = False
            receiveAction = True
            good_interaction = False
        else:
            child_action = child_action
    except AttributeError:
        child_action = child_action
        print("Special Key {0} pressed".format(key))

def on_release(key):
    global child_action
    global MusicalActivity
    if key == keyboard.Key.esc:
        child_action = "QUIT"
        MusicalActivity = False
    print("Child action: " + child_action)

child_action = " "
MusicalActivity = False
receiveAction = False
good_interaction = False
breakFromKey = False
listener = keyboard.Listener(on_press = on_press, on_release = on_release)
listener.start()

class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    excited (at least, I think that is why it lets exceptions through).
    '''

    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)

with suppress_stdout_stderr():

    def run_demo(args):

        time.sleep(2)
        arduino.new_user_function()

        functions_main.send_uno_lights(arduino.ser1,"none")
        functions_main.send_uno_lights(arduino.ser1, "move")

        #Human Interaction variables
        TIME_OUT = 40 # How much time do i have if i'm searching a human during the interaction loop?
        TIME_OUT_HUM = 30 # How much time can I stay without human?
        tracking_a_user = False #is the obstacle i read from sonar an human?
        Finding_human = False #am i looking for a human?
        global receiveAction
        global MusicalActivity
        global child_action
        global good_interaction
        firstTime = True
        still_searching = 0
        lookTo = ""
        meanAngle = 0
        prevpreviousAngle = 0
        previousAngle = 0
        angle = 0
        echo = 0
        soundDirection = ""
        interaction = 0
        tooCloseCount = 0
        tooFarCount = 0
        NSongIdentified = 0
        try_again = 0
        waitingForSounds = 0
        NSongsinLevel = 7  # number of songs in a level
        MA_interactionLevel = 0  # contains the audios for interaction in MA
        AnswerTime = 9.0 # minimum time given to reproduce a song
        TIME_OUT_SONG = 12.0 # maximum time given to reproduce a song
        answerTime = 0
        TIME_OUT_song = 0
        TIME_OUT_MA = 9.0
        time_end_MA = 0
        angle_acquisition = 0
        #identification_time = 0
        time_goodInteraction = 0
        time_loop = 0
        child_not_involved = 0


        #--> Counting the time that manages the reseach of a human
        time_out_system = 0
        start_time_out_system = 0
        current_time_out_system = 0

        #--> Counting the time of interaction
        time_out_system_hum = 0
        start_time_out_system_hum = 0
        current_time_out_system_hum = 0

        # ---> Counting MA time
        start_time_MA = 0
        duration_MA = 0
        actual_time_MA = 0


        while True:

            t1 = time.perf_counter()

            arduino.new_user_function() #Connect with the Mega and obtain data from sensors

            # Run Object Detection
            angle_acquisition = 0
            while angle_acquisition < 3:
                angle_acquisition += 1
                prevpreviousAngle = previousAngle
                previousAngle = angle
                #ANGLE from BlueCoin
                subprocess2 = subprocess.Popen("/home/pi/BlueCoin/BlueCoin", shell=True, stdout=subprocess.PIPE)
                subprocess_return = subprocess2.stdout.read()
                returnvalue = subprocess_return.decode("utf-8")
                beg = returnvalue.find("##ANGLE##")
                end = returnvalue.find("##", beg + 9)
                stringangle = returnvalue[beg + 9: end]
                #print("result")
                #print(subprocess_return)
                #print(stringangle)
                angle = int(stringangle)
                print("angle from BlueCoin=  {:.1f}".format(angle) )

            # check for voice's direction and echo
            echo = 0
            if angle < 0 and (previousAngle >= 0 or prevpreviousAngle >= 0):
                if previousAngle >= 0 and prevpreviousAngle >= 0:
                    if abs(previousAngle - prevpreviousAngle) < 100:
                        meanAngle = (previousAngle + prevpreviousAngle) // 2
                    elif ((previousAngle <= 45) or (previousAngle >= 315)) and ((prevpreviousAngle <= 45) or (prevpreviousAngle >= 315)): #if back
                        meanAngle = 1 #random number on the back
                    else:
                        echo = 1
                        soundDirection = "ECHO"
                        meanAngle = -100
                        print("echo present")
                elif previousAngle >= 0 and prevpreviousAngle < 0:
                    meanAngle = previousAngle
                elif previousAngle < 0 and prevpreviousAngle >= 0:
                    meanAngle = prevpreviousAngle
            elif angle >= 0:
                if previousAngle >= 0 and prevpreviousAngle >= 0:
                    if (abs(previousAngle - prevpreviousAngle) + abs(angle - prevpreviousAngle) + abs(previousAngle - angle)) < 200:
                        meanAngle = (angle + previousAngle + prevpreviousAngle) // 3
                    elif ((angle <= 45) or (angle >= 315)) and ((previousAngle <= 45) or (previousAngle >= 315)) and  ((prevpreviousAngle <= 45) or (prevpreviousAngle >= 315)): #if back
                        meanAngle = 1 #random number on the back
                    else:
                        echo = 1
                        soundDirection = "ECHO"
                        meanAngle = -100
                        print("echo present")
                elif previousAngle >= 0 and prevpreviousAngle < 0:
                    if abs(previousAngle - angle) < 100:
                        meanAngle = (previousAngle + angle) // 2
                    elif ((previousAngle <= 45) or (previousAngle >= 315)) and ((angle <= 45) or (angle >= 315)): #if back
                        meanAngle = 1 #random number on the back
                    else:
                        echo = 1
                        soundDirection = "ECHO"
                        meanAngle = -100
                        print("echo present")
                elif previousAngle < 0 and prevpreviousAngle >= 0:
                    if abs(angle - prevpreviousAngle ) < 100:
                        meanAngle = (angle + prevpreviousAngle) // 2
                    elif ((prevpreviousAngle <= 45) or (prevpreviousAngle >= 315)) and ((angle <= 45) or (angle >= 315)): #if back
                        meanAngle = 1 #random number on the back
                    else:
                        echo = 1
                        soundDirection = "ECHO"
                        meanAngle = -100
                        print("echo present")
                elif previousAngle < 0 and prevpreviousAngle < 0:
                    meanAngle = angle
            elif angle < 0 and previousAngle < 0 and prevpreviousAngle < 0:
                meanAngle = -100
                soundDirection = "NONE"
                print("no voice detected")
            print("meanAngle: {:.1f}".format(meanAngle))

            if ((echo == 0) and (meanAngle >= 0)):
               if ((meanAngle >= 165 ) and (meanAngle <= 195)): # sounds from the front
                   soundDirection = "FRONT"
               elif ((meanAngle >= 195) and (meanAngle <= 315)): # sounds from the right
                   soundDirection = "RIGHT"
               elif ((meanAngle >= 45) and (meanAngle <= 165)): # sounds from the left
                   soundDirection = "LEFT"
               elif (((meanAngle >= 315) or (meanAngle <= 45))): # sounds from the back
                   soundDirection = "BACK"

            if ((echo == 1) or (meanAngle >= 0)):
                waitingForSounds = 0

            print("sound Direction: {}".format(soundDirection))

            ####-----START HUMAN INTERACTION-----####
            count = 0

            #arduino.new_user_function() #Connect with the Mega and obtain data from sensors

            #interaction = 0 or interaction=1 is when the system is trying to estabilish an interaction with the child
            #interaction = 2 is when the robot is already interacting with the human

            time_loop = time.time()
            if MusicalActivity or ((time_goodInteraction != 0) and (time_goodInteraction + TIME_OUT_MA < time_loop)):
                functions_main.send_uno_lights(arduino.ser1, "happy")  # rainbow lights
                functions_main.send_initial_action_arduino("interested_excited", arduino.ser, "startactivity")  # small rotations left and right & explaination of the activity
                time_out_system_hum = 0
                TOTSongsIdentified = 0
                start_time_MA = time.time()
                print("Musical Activity")
                Nid = 0
                ActivityLevel = 1
                while ActivityLevel < 4:
                    song = 0
                    functions_main.send_uno_lights(arduino.ser1, "excited_attract") # random lights
                    functions_main.send_initial_action_arduino("interested_excited", arduino.ser, "none")  # small rotations left and right
                    functions_main.reproduce_song(ActivityLevel, song)  # Attenti alla musica!
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
                        functions_main.send_uno_lights(arduino.ser1, "angry") # red lights
                        functions_main.send_initial_action_arduino("excited_attract", arduino.ser, "myturn")  # small movements left and right & ora tocca a me
                        functions_main.reproduce_song(ActivityLevel, song)  # reproducing the song
                        functions_main.send_initial_action_arduino("backForth", arduino.ser, "yourturn") #small backforth & ora tocca a te
                        functions_main.send_uno_lights(arduino.ser1, "interested_excited") # green lights
                        # if song == 1: #before every firts song of the level
                        if (song % 2) != 0:  # every time a new song is played (odd number)(every song is reproduced twice)
                            functions_main.reproduce_action_sound("play") # suona con me! batti a tempo
                        # BEAT RECOGNITION
                        activity = AudioActivity()
                        activity.start(id=Nid)
                        print("id=")
                        print(Nid)
                        if (song % 2) != 0:  # every time a new song is played (odd number)(every song is reproduced twice)
                            Nid += 1
                        while ((activity.elapsed_time < answerTime or activity.silence < 15) and activity.elapsed_time < TIME_OUT_song): #wait in case the child is still playing (making noises)
                            time.sleep(1.0)
                            if activity.sequence_identified > 0:
                                print("Bravoooo - Song correctly reproduced")
                                functions_main.send_uno_lights(arduino.ser1, "interested_excited") # green lights
                                NSongIdentified += 1
                                #time.sleep(1.0)
                                #identification_time = time.perf_counter()
                                break
                        if activity.sequence_identified > 0:
                            while activity.silence < 15 and activity.elapsed_time < TIME_OUT_song:  # wait in case the child is still playing # oppure and (identification_time + 1.5 > activity.elapsed_time)
                                continue
                        activity.stop()
                        #reaction of the robot to the 2 songs just performed
                        if (activity.sequence_identified == 0) and (activity.other_activity > 20 or activity.Nbeat < 3):
                            print("the child is not performing the activity")
                            functions_main.send_uno_lights(arduino.ser1, "sad") # blue lights
                            functions_main.send_initial_action_arduino("openToRight", arduino.ser, "noplay") #back left & non giochi con me? :(
                            functions_main.send_initial_action_arduino("openBackToLeft", arduino.ser, "none") #forth left
                            functions_main.send_uno_lights(arduino.ser1, "happy") #rainbow lights
                            functions_main.send_initial_action_arduino("backForth", arduino.ser, "excited") #small backforth
                            child_not_involved += 1
                            if child_not_involved > 4:
                                print("the child doesn't want to play or didn't understand the activity")
                                print("Terminating the program")  # unless I receive an action from the child
                                functions_main.reproduce_action_sound("terminate")  # ciao ciao!
                                child_action = "QUIT"
                                break
                        elif activity.sequence_identified > 0: # song correctly reproduced
                            print("song well reproduced by the child")
                            functions_main.send_uno_lights(arduino.ser1, "interested_excited") # green lights
                            functions_main.send_initial_action_arduino("happy", arduino.ser, "good")
                            child_not_involved = 0
                            if ActivityLevel != 3 and (song % 2) != 0: # not reproducing the same song if the child altready reproduced it well
                                song += 1
                                NSongIdentified += 1
                        else:
                            print("the child did not reproduced the song well")
                            functions_main.send_uno_lights(arduino.ser1, "angry")  # red lights
                            functions_main.send_initial_action_arduino("excited_attract", arduino.ser, "again")  # small movements left and right & riproviamo
                            functions_main.send_uno_lights(arduino.ser1, "excited_attract")  # random lights
                        print("next song in the same level")
                        activity.sequence_identified = 0
                    if child_action == "QUIT":
                        break
                    # LEVEL CONCLUDED: checking for results. if 50% of the activity is correct: next level. else: repeat the level
                    if (song == NSongsinLevel):  # end of the level
                        if NSongIdentified >= ((NSongsinLevel - 1) // 2):  # 50% correct
                            print("yeeeyyy ready fot the next level")
                            functions_main.send_uno_lights(arduino.ser1, "interested_excited") # green lights
                            functions_main.send_initial_action_arduino("happy", arduino.ser, "happy") #rotation on itself and back & evviva
                            functions_main.reproduce_action_sound("sing") # canta con me!
                            functions_main.send_uno_lights(arduino.ser1, "happy") #rainbow lights
                            functions_main.reproduce_song(ActivityLevel, song) # long song
                            ActivityLevel += 1  # next level
                            try_again = 0
                            if ActivityLevel < 4:
                                functions_main.send_initial_action_arduino("interested_excited", arduino.ser, "nextlevel") #small rotations left and right
                        else:
                            print("well well riproviamo?")
                            functions_main.reproduce_action_sound("sad")
                            functions_main.send_uno_lights(arduino.ser1, "angry")  # red lights
                            functions_main.send_initial_action_arduino("excited_attract", arduino.ser, "again") #small movements left and right & riproviamo
                            functions_main.send_uno_lights(arduino.ser1, "excited_attract") # random lights
                            try_again += 1
                            if try_again < 3:
                                # if the child was not able to pass to the next level, the same will be reproposed
                                Nid -= ((NSongsinLevel - 1) // 2)
                            else: # if the level has been proposed too many times, pass to the next level
                                ActivityLevel += 1  # next level
                                if ActivityLevel < 4:
                                    functions_main.send_initial_action_arduino("interested_excited", arduino.ser, "nextlevel") #small rotations left and right
                        TOTSongsIdentified = TOTSongsIdentified + NSongIdentified

                    actual_time_MA = time.time()
                    duration_MA = duration_MA + (actual_time_MA - start_time_MA)
                    start_time_MA = actual_time_MA
                    print("Time MA: {:.1f}".format(duration_MA))  # the duration of each level of the activity

                functions_main.send_uno_lights(arduino.ser1, "happy") #rainbow lights
                functions_main.send_initial_action_arduino("happy", arduino.ser, "finishactivity") #rotation on itself and back & thank you for playing with me

                if duration_MA != 0:
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%y %H:%M:%S")
                    data = dt_string + ',' + str(duration_MA) + ',' + str(TOTSongsIdentified) + '\n'
                    with open('records.csv', 'a') as fp:
                        print("Record stored successfully")
                        fp.write(data)
                duration_MA = 0
                NSongIdentified = 0

                actual_time_MA = time.time()
                time_end_MA = time.time()
                while actual_time_MA < TIME_OUT_MA + time_end_MA:  # if after MA nothing happens
                    if receiveAction == True:
                        break
                    time.sleep(0.5)
                    actual_time_MA = time.time()
                if receiveAction != True:
                    print("Terminating the program") #unless I receive an action from the child
                    child_action = "QUIT"
                    MusicalActivity = False

            if interaction != 2 and not MusicalActivity: #If I'm not interacting with the human
                print("Interaction != 2, I'm not interacting with the human")
                print("arduino.new_dist !!!!!!!!!!!!!!!!!!!!!!!!! DISTANZA: {:.1f}".format(arduino.new_dist))
                if arduino.old_user != "none" and arduino.new_dist < 120.0: #if an object is detected by the sonar, and it is closer than x, check if it is a human
                    print("Object detected by sonars")
                    if ((meanAngle >= 0) or (soundDirection == "ECHO")):  # voice detected by BlueCoin
                        print("Human detected in the FOV")
                        count = 4
                        if meanAngle >= 0 and soundDirection == "FRONT":
                            tracking_a_user = functions_main.human_verification(meanAngle, arduino.old_user, count)  # it check if obstacle detected from sonar is a human
                        elif soundDirection == "ECHO": # check which one of the angle detected corresponds to what the sonar
                            tracking_a_user = functions_main.human_verification(angle, arduino.old_user, count) #it check if obstacle detected from sonar is a human
                            if tracking_a_user == False:
                                tracking_a_user = functions_main.human_verification(previousAngle, arduino.old_user, count)  # it check if obstacle detected from sonar is a human
                            if tracking_a_user == False:
                                tracking_a_user = functions_main.human_verification(prevpreviousAngle, arduino.old_user, count)  # it check if obstacle detected from sonar is a human
                        if tracking_a_user == True:
                            print("Object detected from sonar is a human")
                            interaction = 1
                            ### --- I Should check if the path between the robot and the child is clear
                            ##if the human is free
                            ##if the human is free for few instant
                            interaction = 2
                            start_time_out_system_hum = time.time()
                            #THERE IS A HUMAN READY TO INTERACT WITH!
                            Finding_human = False
                            functions_main.send_uno_lights(arduino.ser1, "excited_attract")
                            functions_main.send_initial_action_arduino("excited_attract", arduino.ser, "found") #ey ciao ti ho trovato
                        else: #if it finds an object that is not a human (angle sonar != angle BlueCoin), it must rotate until that obstacle is an human (in the angle s direction)
                            print("Object from sonar is not a human")
                            if (soundDirection == "FRONT" and arduino.new_dist > 150): #the human is in front of the robot and eventually right/left osbstacle are far
                                print("Human in front of me - Approaching ")
                                functions_main.send_uno_lights(arduino.ser1, "move")
                                functions_main.send_initial_action_arduino("move", arduino.ser, "move")
                            elif (soundDirection == "RIGHT"):
                                print("Human detected in right position...")
                                functions_main.send_uno_lights(arduino.ser1, "rotateRight")
                                functions_main.send_initial_action_arduino("rotateRight", arduino.ser, "none")
                            elif (soundDirection == "LEFT"):
                                print("Human detected in left position...")
                                functions_main.send_uno_lights(arduino.ser1, "rotateLeft")
                                functions_main.send_initial_action_arduino("rotateLeft", arduino.ser, "none")
                            elif (soundDirection == "BACK"):
                                print("Human detected in back position...")
                                functions_main.send_uno_lights(arduino.ser1, "rotateRight")
                                functions_main.send_initial_action_arduino("turnBack", arduino.ser, "none")
                    else : #if there is no human (no angle from BlueCoin), but object detected from sonar
                        #GET CLOSER TO THE OBJECT! maybe the child is to far for the BlueCoin to detect his voice
                        if arduino.new_dist > 120.0:  # if the distance to the chld is bigger than , get closer
                            functions_main.send_uno_lights(arduino.ser1, "move")
                            functions_main.send_initial_action_arduino("move", arduino.ser, "move_find")
                            print("Is the user too far?")
                        else: #the user might be in front of the robot but silent, encourage to make sounds and wait
                            if waitingForSounds < 4:
                                if waitingForSounds == 2:
                                    functions_main.send_uno_lights(arduino.ser1, "excited_attract")
                                    functions_main.send_initial_action_arduino("excited_attract", arduino.ser, "where") # dove sei? dai fatti sentire!
                                waitingForSounds += 1
                            else: #if still no sounds it might be just an object
                                functions_main.send_uno_lights(arduino.ser1, "rotateRight")
                                functions_main.send_initial_action_arduino("rotateRight", arduino.ser, "none")
                                waitingForSounds = 0
                    print("No object close")
                else:   #if no object detected from sonar
                    # ASK TO GET CLOSER
                    if meanAngle >= 0: #there is a human in the FOV of robot. angle detected from BlueCloin
                        print("No object, but human in the FOV")
                        interaction = 1
                        if (soundDirection == "FRONT"): #the human is in front of the robot
                            print("Approaching the human")
                            functions_main.send_uno_lights(arduino.ser1, "move")
                            functions_main.send_initial_action_arduino("move", arduino.ser, "move")
                        elif (soundDirection == "RIGHT"):
                            print("Searching right...")
                            functions_main.send_uno_lights(arduino.ser1, "rotateRight")
                            functions_main.send_initial_action_arduino("rotateRight", arduino.ser, "none")
                        elif (soundDirection == "LEFT"):
                            print("Searching left...")
                            functions_main.send_uno_lights(arduino.ser1, "rotateLeft")
                            functions_main.send_initial_action_arduino("rotateLeft", arduino.ser, "none")
                        elif (soundDirection == "BACK"):
                            print("Searching back...")
                            functions_main.send_uno_lights(arduino.ser1, "rotateRight")
                            functions_main.send_initial_action_arduino("turnBack", arduino.ser, "none")
                    else: #if there is no human: no sounds perceived from BlueCoin
                        if waitingForSounds < 4:
                            if waitingForSounds == 2: # dai fatti sentire!
                                functions_main.send_uno_lights(arduino.ser1, "excited_attract")
                                functions_main.send_initial_action_arduino("excited_attract", arduino.ser, "where") # dove sei? dai fatti sentire!
                            waitingForSounds += 1
                        else:  # if still no sounds it might be just an object
                            functions_main.send_uno_lights(arduino.ser1, "rotateRight")
                            functions_main.send_initial_action_arduino("rotateRight", arduino.ser, "none")
                            waitingForSounds = 0
                        print("Searching")
            elif interaction == 2 and not MusicalActivity: # interaction = 2, so i'm starting the interaction loop
                print("INTERACTION LOOP")
                if time_out_system_hum > TIME_OUT_HUM: #If there is no human for too long
                    print("INTERACTION LOOP - I've lost contact with the human")
                    Finding_human = True # Am i looking for a human?
                    time_out_system = 0
                    start_time_out_system = time.time()
                    time_out_system_hum = 0
                elif time_out_system_hum <= TIME_OUT_HUM and time_out_system<TIME_OUT and Finding_human == False:
                    still_searching = 0
                    if receiveAction and child_action == "notfound":
                        functions_main.send_uno_lights(arduino.ser1, "angry")
                        functions_main.send_initial_action_arduino("turnBack", arduino.ser, "notfound") # ah sei un oggetto! dove sei?
                        print("INTERACTION LOOP - it is not a human, but an object")
                        functions_main.send_uno_lights(arduino.ser1, "excited_attract")
                        Finding_human = True  # Am i looking for a human?
                        time_out_system = 0
                        start_time_out_system = time.time()
                        time_out_system_hum = 0
                        receiveAction = False
                        interaction = 0
                    else:
                        print("INTERACTION LOOP - Preparing the interaction")
                        #If there is a human interacting and i'm inside the timeout
                        time_out_system = 0
                        print("Distance from sonar = {:.1f}".format(arduino.new_dist))
                        if arduino.new_dist > 120.0: #if the distance to the chld is bigger than , get closer
                            tooCloseCount=0
                            tooFarCount += 1
                            if tooFarCount > 10:
                                tooFarCount = 0
                                if (soundDirection == "FRONT"): # if the voice is detected from the front or not detected because the child is too far
                                    print("INTERACTION LOOP - Child is far and in front ") #ADD and before was in front according to sonar or angle???
                                    functions_main.send_uno_lights(arduino.ser1, "move")
                                    functions_main.send_initial_action_arduino("move", arduino.ser, "move_find")
                                elif (soundDirection == "RIGHT"):
                                    print("INTERACTION LOOP - Child is on the right ")
                                    functions_main.send_uno_lights(arduino.ser1, "rotateRight")
                                    functions_main.send_initial_action_arduino("rotateRight", arduino.ser, "none")
                                elif (soundDirection == "LEFT"):
                                    print("INTERACTION LOOP - Child is on the left ")
                                    functions_main.send_uno_lights(arduino.ser1, "rotateLeft")
                                    functions_main.send_initial_action_arduino("rotateLeft", arduino.ser, "none")
                                elif (soundDirection == "BACK"):
                                    print("INTERACTION LOOP - Child is on the back ")
                                    functions_main.send_uno_lights(arduino.ser1, "rotateRight")
                                    functions_main.send_initial_action_arduino("turnBack", arduino.ser, "none")
                                elif ((soundDirection == "NONE") or (soundDirection == "ECHO")): #if no sounds perceived from BlueCoin
                                    if waitingForSounds < 4:
                                         if waitingForSounds == 2:
                                             functions_main.send_uno_lights(arduino.ser1, "excited_attract")
                                             functions_main.send_initial_action_arduino("excited_attract", arduino.ser, "where") # dove sei? dai fatti sentire! da sostituire con AVVICINATI, NON TI SENTO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                         waitingForSounds += 1
                                    else:  # if still no sounds it might be just an object I pretend the user if in front but too far for the BlueCoin to hear him
                                        functions_main.send_uno_lights(arduino.ser1, "move")
                                        functions_main.send_initial_action_arduino("move", arduino.ser, "move_find")
                                        waitingForSounds = 0
                        elif arduino.new_dist < 40.0:
                            tooCloseCount += 1
                            tooFarCount = 0
                            if tooCloseCount > 10: #If I'm too cloose for too much time ( I need this time window in order to let the children interact with the robot)
                                print("INTERACTION LOOP - Too close")
                                functions_main.send_uno_lights(arduino.ser1, "move")
                                functions_main.send_initial_action_arduino("scared", arduino.ser, "move_find")
                                tooCloseCount = 0
                        else: #if it's closer than 1.5m perform the interaction loop normally and select action of the child (child_action)
                            # Run Object Detection. I start now the timer for human time out because else comprehend no object sensed by the sonar
                            tooCloseCount = 0
                            tooFarCount = 0
                            current_time_out_system_hum = time.time()
                            time_out_system_hum = time_out_system_hum+(current_time_out_system_hum-start_time_out_system_hum)
                            start_time_out_system_hum = current_time_out_system_hum
                            if (soundDirection == "FRONT"):
                                time_out_system_hum = 0
                            if (soundDirection == "RIGHT"):
                                lookTo = "rotateRight"
                                time_out_system_hum = 10
                            elif (soundDirection == "LEFT"):
                                lookTo = "rotateLeft"
                                time_out_system_hum = 10
                            elif (soundDirection == "BACK"):
                                lookTo = "turnBack"
                                time_out_system_hum = 10 # might have been echo
                            print("INTERACTION LOOP - Correctly interacting, waiting to receive an action")

                            if firstTime:
                                functions_main.send_uno_lights(arduino.ser1,"excited_attract")
                                functions_main.send_initial_action_arduino("excited_attract", arduino.ser, "interested_excited") #giochiamo?
                                firstTime = False
                            if receiveAction:
                                if child_action != "activity" and child_action != "notfound":
                                    functions_main.decide_action(child_action) #decide robot behaviour based on action of the child and movement of the robot
                                    functions_main.send_uno_lights(arduino.ser1, functions_main.current_action)
                                    functions_main.send_initial_action_arduino( functions_main.current_action, arduino.ser, functions_main.current_action)
                                    receiveAction = False
                                    if good_interaction == True:
                                        time_goodInteraction = time.time()
                                        good_interaction = False
                                    else:
                                        time_goodInteraction = 0
                                elif child_action == "activity":
                                    MusicalActivity = True
                                    start_time_MA = time.time()
                                    duration_MA = 0
                                    receiveAction = False
                            print("Child Action: " + child_action + " | " + "Robot Action: " + functions_main.current_action)
                        print("Time Out Human {:.1f} / 10 Sec".format(time_out_system_hum) )
                if Finding_human == True and time_out_system < TIME_OUT : #if i need to find the child and i'm inside the timout
                    print("INTERACTION LOOP - Looking for a human")
                    #I need to find the human. I start counting for the general TIME_OUT
                    # Run Object Detection
                    current_time_out_system = time.time()
                    time_out_system = time_out_system+(current_time_out_system-start_time_out_system)
                    start_time_out_system = current_time_out_system
                    print("Time out: {:.1f} / 40 ".format(time_out_system))
                    if ((meanAngle >= 0) or (soundDirection == "FRONT")):  # this can be replaced with a check if it is human, so this translate to if there is a human
                        tracking_a_user = functions_main.human_verification(meanAngle, arduino.old_user, count)  # it check if obstacle detected from sonar is a human
                        waitingForSounds = 0
                    elif soundDirection == "ECHO":  # check which one of the angle detected corresponds to what the sonar
                        waitingForSounds = 0
                        tracking_a_user = functions_main.human_verification(angle, arduino.old_user, count)  # it check if obstacle detected from sonar is a human
                        if tracking_a_user == False:
                            tracking_a_user = functions_main.human_verification(previousAngle, arduino.old_user, count)  # it check if obstacle detected from sonar is a human
                        if tracking_a_user == False:
                            tracking_a_user = functions_main.human_verification(prevpreviousAngle, arduino.old_user, count)  # it check if obstacle detected from sonar is a human
                    if tracking_a_user == True:
                        print("INTERACTION LOOP - Human detected in the FOV")
                        Finding_human = False
                        functions_main.send_uno_lights(arduino.ser1, "excited_attract")
                        functions_main.send_initial_action_arduino("excited_attract", arduino.ser, "excited")
                        time_out_system_hum = 0
                        time_out_system = 0
                        still_searching = 0
                    else:
                        print("INTERACTION LOOP - Searching")
                        still_searching += 1
                        functions_main.send_uno_lights(arduino.ser1, "none")
                        functions_main.send_initial_action_arduino(lookTo, arduino.ser, "none")
                        if still_searching > 2:
                            Finding_human = True  # Am i looking for a human?
                            time_out_system = 0
                            start_time_out_system = time.time()
                            time_out_system_hum = 0
                            interaction = 0
                elif Finding_human == True and time_out_system>TIME_OUT: #If 'm looking for the children and i run out of time
                    print("Terminating the program")
                    child_action = "QUIT"

            ####-----END HUMAN INTERACTION----####
            t2 = time.perf_counter()
            elapsedTime = t2-t1
            fps = 1/elapsedTime
            i=0

            if args.no_show:
                print("Cicli al secondo: {:.1f} ".format(float(fps)))
                continue

            if child_action == "QUIT": # it saves the duration of the activity and the number of songs correctly reproduced by the child
                functions_main.send_uno_lights(arduino.ser1, "none")
                functions_main.reproduce_action_sound("terminate")  # ciao ciao!
                if duration_MA != 0 and NSongIdentified != 0:
                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%y %H:%M:%S")
                    data = dt_string + ',' + str(duration_MA) + ',' + str(NSongIdentified) + '\n'
                    with open('records.csv','a') as fp:
                        print("Record stored successfully")
                        fp.write(data)
                break
        
    #datas.stop()

if __name__ == "__main__":
    args = build_argparser().parse_args()
    run_demo(args)
