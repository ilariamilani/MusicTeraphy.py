#!/usr/bin/env python3

import argparse
import sys
#import cv2
import time
import numpy as np
import math
import subprocess

from datetime import datetime
from audioplayer import PlayAudio
from threading import Thread

#from edgetpu.basic import edgetpu_utils
#from pose_engine import PoseEngine
#from finalmodel import prepare_modelSingle
#from openvino.inference_engine import IECore
#from detector import Detector
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


#substituted JointAttention with MusicalActivity

def on_press(key):
    global child_action
    global MusicalActivity
    global receiveAction
    try:
        print("{0} Pressed".format(key.char))        
        if key.char == ("a"):
            child_action = "touch"
            MusicalActivity = False
            receiveAction = True
        elif key.char == ("s"):
            child_action = "push"
            MusicalActivity = False
            receiveAction = True
        elif key.char == ("d"):
            child_action = "hit"
            MusicalActivity = False
            receiveAction = True
        elif key.char == ("f"):
            child_action = "hug"
            MusicalActivity = False
            receiveAction = True
        elif key.char == ("g"):
            child_action = "strongHug"
            MusicalActivity = False
            receiveAction = True
        elif key.char == ("h"):
            child_action = "none"
            MusicalActivity = False
            receiveAction = True
        elif key.char == ("j"):
            child_action = "joint"
            MusicalActivity = False
            receiveAction = True
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
breakFromKey = False
listener = keyboard.Listener(on_press = on_press, on_release = on_release)
listener.start()

def run_demo(args):
    
    time.sleep(2)
    arduino.new_user_function()
    
    functions_main.send_uno_lights(arduino.ser1,"none") 
    functions_main.send_uno_lights(arduino.ser1, "move")
    
    #Setting communications  

##CAM    model_width   = 640
##CAM    model_height  = 480
##CAM   labels definition

##CAM    devices = edgetpu_utils.ListEdgeTpuPaths(edgetpu_utils.EDGE_TPU_STATE_UNASSIGNED)
##CAM    engine = PoseEngine(args.model_hpe, devices[0])

##CAM    ie = IECore()
##CAM    detector_object = Detector(ie, path_to_model_xml=args.model_od, device=args.device, label_class=args.person_label)

##CAM    model_gaze.load_weights('/home/pi/Detection-and-Human-Pose-Estimation---RASPBERRY/models/trainedOnGazeFollow_weights.h5')

    #Framerate variables
    fps = ""
    
    #Human Interaction variables
    TIME_OUT = 40 # How much time do i have if i'm searching a human during the interaction loop?
    TIME_OUT_HUM = 10 # How much time can I stay without human?
    MA_TIME = 30 #duration of MA task analisys
    child_action_prec = "none"
    tracking_a_user = False #is the obstacle i read from sonar an human?
    Finding_human = False #am i looking for a human?
    global receiveAction
    global MusicalActivity
    global child_action
    firstTime = True
    lookTo = ""
    meanAngle = 0
    prevMeanAngle = 0
    prevpreviousAngle = 0
    previousAngle = 0
    angle = 0
    echo = 0
    soundDirection = ""
    interaction = 0
    tooCloseCount = 0
    tooFarCount = 0
    NSongIdentified = 0
    waitingForSounds = 0
    
    
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
    
    start_time_TOLERANCE = 0 
    duration_TOLERANCE = 0
    actual_time_TOLERANCE = 0
    
    PlayAudio().play("sounds/Giochiamo.wav")
    functions_main.send_uno_lights(arduino.ser1,"none") 
    
    while True:
        
        t1 = time.perf_counter()
                
        arduino.new_user_function() #Connect with the Mega and obtain data from sensors
   
        # Run Object Detection
        echo = 0
        prevpreviousAngle = previousAngle
        previousAngle = angle
        prevMeanAngle = meanAngle
        #ANGLE from BlueCoin
        subprocess2 = subprocess.Popen("/home/pi/BlueCoin/BlueCoin", shell=True, stdout=subprocess.PIPE)
        subprocess_return = subprocess2.stdout.read()
        returnvalue = subprocess_return.decode("utf-8")
        beg = returnvalue.find("##ANGLE##")
        end = returnvalue.find("##", beg + 9)
        stringangle = returnvalue[beg + 9: end]
        print("result")
        print(subprocess_return)
        print(stringangle)
        angle = int(stringangle)
        print(angle)


        # check for voice's direction and echo
        if angle < 0 and (previousAngle >= 0 or prevpreviousAngle >= 0):
            if previousAngle >= 0 and prevpreviousAngle >= 0:
                if abs(previousAngle - prevpreviousAngle) < 100:
                    meanAngle = (previousAngle + prevpreviousAngle) // 2
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
                    meanAngle = (previousAngle + prevpreviousAngle) // 2
                else:
                    echo = 1
                    soundDirection = "ECHO"
                    meanAngle = -100
                    print("echo present")
            elif previousAngle >= 0 and prevpreviousAngle < 0:
                if abs(previousAngle - angle) < 100:
                    meanAngle = (previousAngle + angle) // 2
                else:
                    echo = 1
                    soundDirection = "ECHO"
                    meanAngle = -100
                    print("echo present")
            elif previousAngle < 0 and prevpreviousAngle >= 0:
                if abs(angle - prevpreviousAngle ) < 100:
                    meanAngle = (angle + prevpreviousAngle) // 2
                else:
                    echo = 1
                    soundDirection = "ECHO"
                    meanAngle = -100
                    print("echo present")
            elif previousAngle < 0 and prevpreviousAngle < 0:
                meanAngle = angle
        else:
            meanAngle = -100
            soundDirection = "NONE"
            print("no voice detected")
        print("meanAngle: {:.1f}".format(meanAngle))

        if ((echo == 0) and (meanAngle >= 0)):
           if ((meanAngle >= 155 ) and (meanAngle <= 205)): # sounds from the front
               soundDirection = "FRONT"
           elif ((meanAngle <= 205) and (meanAngle >= 315)): # sounds from the right
               soundDirection = "RIGHT"
           elif ((meanAngle >= 45) and (meanAngle <= 155)): # sounds from the left
               soundDirection = "LEFT"
           elif (((meanAngle >= 315) and (meanAngle <= 45))): # sounds from the back
               soundDirection = "BACK"

        if ((echo == 1) or (meanAngle >= 0)):
            waitingForSounds = 0

        ####-----START HUMAN INTERACTION-----####
        count = 0
        
        #arduino.new_user_function() #Connect with the Mega and obtain data from sensors
                    
        #interaction = 0 or interaction=1 is when the system is trying to estabilish an interaction with the child
        #interaction = 2 is when the robot is already interacting with the human

        if MusicalActivity:
        #if JointAttention:
            time_out_system_hum = 0
            # actual_time_TOLERANCE = time.time()
            # print("Joint Attention Task")
            # if angleTeddy != 0 and greetedTeddy == False: #there is a teddy in the FOV of robot
            #     print("Teddy Bear in the FOV")
            #     if (abs(angleTeddy)<=10): #the teddy is in front of the robot
            #         if arduino.new_dist < 80:
            #             print("Inviting to play with the teddy...")
            #             functions_main.send_uno_lights(arduino.ser1, "excited_attract")
            #             functions_main.send_initial_action_arduino("backForth", arduino.ser, "happy")
            #             functions_main.send_initial_action_arduino("scared", arduino.ser, "none")
            #             functions_main.send_uno_lights(arduino.ser1, "none")
            #             greetedTeddy = True
            #             start_time_LOOKING = time.time()
            #         elif arduino.new_dist > 80:
            #             print("Teddy too far, approaching...")
            #             functions_main.send_initial_action_arduino("move", arduino.ser, "none")
            #     elif angleTeddy >=10:
            #             print("Adjusting right...")
            #             functions_main.send_uno_lights(arduino.ser1, "rotateRight")
            #             functions_main.send_initial_action_arduino("rotateRight", arduino.ser, "none")
            #     elif angleTeddy <= -10:
            #         print("Adjusting left...")
            #         functions_main.send_uno_lights(arduino.ser1, "rotateLeft")
            #         functions_main.send_initial_action_arduino("rotateLeft", arduino.ser, "none")
            # elif targetBox == oldTargetBox: #if there is no Teddy Bear identified for a frame
            #     toleranceFrame += 1
            #     if toleranceFrame == 10 and greetedTeddy == False: #if there actually is no teddy bear in the scene
            #         print("Searching for a Teddy Bear...")
            #         functions_main.send_uno_lights(arduino.ser1, "rotateRight")
            #         functions_main.send_initial_action_arduino("rotateRight", arduino.ser, "none")
            #         toleranceFrame = 0
            #     duration_TOLERANCE = duration_TOLERANCE + abs(actual_time_TOLERANCE - start_time_TOLERANCE)
            #     if duration_TOLERANCE >= 5 and greetedTeddy:
            #         #Task Completed (?)
            #         functions_main.send_uno_lights(arduino.ser1, "happy")
            #         functions_main.send_initial_action_arduino("happy", arduino.ser, "happy")
            #         duration_LOOKING = duration_LOOKING-duration_TOLERANCE
            #         duration_TOLERANCE = 0
            #         JointAttention = False
            #         child_action = "hug" #Interested Interacting state
            # else:
            #      duration_TOLERANCE = 0
            # start_time_TOLERANCE = actual_time_TOLERANCE
            #
            # if greetedTeddy:
            #     #I pretend that it did not spontaneously went out of the scene, so I can assume that Teddy is still on position
            #     actual_time_JA = time.time()
            #     duration_JA = duration_JA + (actual_time_JA - start_time_JA)
            #     start_time_JA = actual_time_JA
            #     print("Time JA: {:.1f}".format(duration_JA))
            #     prep_image = frame[:, :, ::-1].copy()
            #     res, inference_time = engine.DetectPosesInImage(prep_image)
            #     if res:
            #         head, scores_head = elaborate_pose(res)
            #         frame = overlay_on_image(frame, res, model_width, model_height, main_person, args.modality)
            #         frame, gazeAngle, headCentroid, prediction = elaborate_gaze(frame, head, scores_head, model_gaze)
            #         if headCentroid[1] == 0: gazeAngle = 0
            #         if gazeAngle < 0: gazeAngle = 360 + gazeAngle
            #         targetAngleMax = -360
            #         targetAngleMin = 360
            #         if targetBox:
            #             for vertices in targetBox:
            #                 targetAngle=-math.degrees(math.atan2(vertices[1]-headCentroid[1],vertices[0]-headCentroid[0]))
            #                 cv2.line(frame, (vertices[0],vertices[1]), (int(headCentroid[0]), int(headCentroid[1])), (255,255,255), 1)
            #                 if targetAngle > targetAngleMax:
            #                     targetAngleMax = targetAngle
            #                     print("update max")
            #                 if targetAngle < targetAngleMin:
            #                     targetAngleMin = targetAngle
            #                     print("update min")
            #             if targetAngleMax < 0: targetAngleMax = 360 + targetAngleMax
            #             if targetAngleMin < 0: targetAngleMin = 360 + targetAngleMin
            #             print(targetAngleMin, targetAngleMax)
            #             print(gazeAngle)
            #             actual_time_LOOKING = time.time()
            #             if gazeAngle > (targetAngleMin-5) and gazeAngle < (targetAngleMax+5):
            #                 color = (0,255,0)
            #                 duration_LOOKING = duration_LOOKING + abs(actual_time_LOOKING - start_time_LOOKING)
            #             start_time_LOOKING = actual_time_LOOKING
            #     print("Time spent looking at the teddy: {:.1f}".format(duration_LOOKING))
            #     print("Time without teddy in the frame: {:.1f}".format(duration_TOLERANCE))
        else:
            if duration_MA != 0:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%y %H:%M:%S")
                data = dt_string + ',' + str(duration_MA) + ',' + str(NSongIdentified) + '\n'
                with open('records.csv','a') as fp:
                    print("Record stored successfully")
                    fp.write(data)   
            duration_MA = 0
            NSongIdentified = 0
                    
        if interaction != 2 and not MusicalActivity: #If I'm not interacting with the human
            print("Interaction != 2, I'm not interacting with the human")
            if arduino.old_user != "none": #if an object is detected by the sonar, check if it is a human
                print("Object detected by sonars")                              
                if ((meanAngle >= 0) or (prevMeanAngle >= 0) or (soundDirection == "ECHO")):  # voice detected by BlueCoin
                    print("Human detected in the FOV")
                    count = 4
                    if meanAngle >= 0:
                        tracking_a_user = functions_main.human_verification(meanAngle, arduino.old_user, count)  # it check if obstacle detected from sonar is a human
                    elif prevMeanAngle >= 0: # voice detected in the previous cycle
                        tracking_a_user = functions_main.human_verification(prevMeanAngle, arduino.old_user, count)  # it check if obstacle detected from sonar is a human
                    elif soundDirection == "ECHO": # check which one of the angle detected corresponds to what the sonar found
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
                            functions_main.send_initial_action_arduino("rotateRight", arduino.ser, "none")
                            #functions_main.send_initial_action_arduino("rotateRight", arduino.ser, "none") rifare gira a dx 2 volte????????????????????????????????????????????????????????????????????????????????????????????????????
                else : #if there is no human (no angle from BlueCoin), but object detected from sonar
                    #GET CLOSER TO THE OBJECT! maybe the child is to far for the BlueCoin to detect his voice
                    if arduino.new_dist > 120.0:  # if the distance to the chld is bigger than , get closer
                        functions_main.send_uno_lights(arduino.ser1, "move")
                        functions_main.send_initial_action_arduino("move", arduino.ser, "move_find")
                        print("Is the user too far?")
                    else: #the user might be in front of the robot but silent, encourage to make sounds and wait
                        if waitingForSounds < 3:
                            if waitingForSounds == 0:
                                functions_main.send_uno_lights(arduino.ser1, "excited_attract")
                                functions_main.send_initial_action_arduino("excited_attract", arduino.ser, "excited_attract")
                            waitingForSounds += 1
                        else: #if still no sounds it might be just an object
                            functions_main.send_uno_lights(arduino.ser1, "rotateRight")
                            functions_main.send_initial_action_arduino("rotateRight", arduino.ser, "none")
                            waitingForSounds = 0
                print("No object close")
            else:   #if no object detected from sonar
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
                            functions_main.send_initial_action_arduino("rotateRight", arduino.ser, "none")
                            #functions_main.send_initial_action_arduino("rotateRight", arduino.ser, "none") rifare gira a dx 2 volte????????????????????????????????????????????????????????????????????????????????????????????????????
                else: #if there is no human: no sounds perceived from BlueCoin
                    if waitingForSounds < 3:
                        if waitingForSounds == 0:
                            functions_main.send_uno_lights(arduino.ser1, "excited_attract")
                            functions_main.send_initial_action_arduino("excited_attract", arduino.ser, "excited_attract")
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
                            functions_main.send_initial_action_arduino("rotateRight", arduino.ser, "none")
                            #functions_main.send_initial_action_arduino("rotateRight", arduino.ser, "none") rifare gira a dx 2 volte????????????????????????????????
                        elif ((soundDirection == "NONE") or (soundDirection == "ECHO")): #if no sounds perceived from BlueCoin
                            if waitingForSounds < 3:
                                 if waitingForSounds == 0:
                                     functions_main.send_uno_lights(arduino.ser1, "excited_attract")
                                     functions_main.send_initial_action_arduino("excited_attract", arduino.ser, "excited_attract")
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
                    # Run Object Detection. I start now the timer for human time out because else comprehend 20 < dist 130 AND dist = Max dist, so no object sensed by the sonar
                    tooCloseCount = 0
                    tooFarCount = 0
                    current_time_out_system_hum = time.time()
                    time_out_system_hum = time_out_system_hum+(current_time_out_system_hum-start_time_out_system_hum)
                    start_time_out_system_hum = current_time_out_system_hum
                    if (soundDirection == "RIGHT"):
                        lookTo = "rotateRight"
                    elif (soundDirection == "LEFT"):
                        lookTo = "rotateLeft"
                    elif (soundDirection == "BACK"):
                        lookTo = "rotateRight"
                        # lookTo = "rotateRight" rifare gira a dx 2 volte????????????????????????????????

                    print("INTERACTION LOOP - Correctly interacting, waiting to receive an action")
                    time_out_system_hum = 0
                    if firstTime:
                            functions_main.send_uno_lights(arduino.ser1,"excited_attract")
                            functions_main.send_initial_action_arduino("excited_attract", arduino.ser, "excited_attract")
                            firstTime = False
                    if receiveAction:
                        if child_action != "joint":
                            functions_main.decide_action(child_action) #decide robot behaviour based on action of the child and movement of the robot
                            functions_main.send_uno_lights(arduino.ser1, functions_main.current_action)
                            functions_main.send_initial_action_arduino( functions_main.current_action, arduino.ser, functions_main.current_action)
                            receiveAction = False
                        else:
                            MusicalActivity = True
                            start_time_MA = time.time()
                            duration_MA = 0

                    print("Child Action: " + child_action + " | " + "Robot Action: " + functions_main.current_action)
                print("Time Out Human {:.1f} / 10 Sec".format(time_out_system_hum) )
            elif Finding_human == True and time_out_system < TIME_OUT : #if i need to find the child and i'm inside the timout
                print("INTERACTION LOOP - Looking for a human")
                #I need to find the human. I start counting for the general TIME_OUT
                # Run Object Detection
                current_time_out_system = time.time()
                time_out_system = time_out_system+(current_time_out_system-start_time_out_system)
                start_time_out_system = current_time_out_system
                print("Time out: {:.1f} / 40 ".format(time_out_system))
                
                if ((meanAngle >= 0) or (soundDirection == "ECHO")):  # this can be replaced with a check if it is human, so this translate to if there is a human
                    print("INTERACTION LOOP - Human detected in the FOV")
                    Finding_human = False
                    functions_main.send_uno_lights(arduino.ser1, "excited_attract")
                    functions_main.send_initial_action_arduino("excited_attract", arduino.ser, "excited_attract")
                    time_out_system_hum = 0   
                    time_out_system = 0                     
                else:
                    if waitingForSounds < 3:
                        waitingForSounds += 1
                    print("INTERACTION LOOP - Searching")
                    functions_main.send_uno_lights(arduino.ser1, "none")
                    functions_main.send_initial_action_arduino(lookTo, arduino.ser, "none")
            elif Finding_human == True and time_out_system>TIME_OUT: #If 'm looking for the children and i run out of time
                print("Terminating the program")
                child_action = "QUIT"
                
        ####-----END HUMAN INTERACTION----####
        
##CAM        oldTargetBox = targetBox.copy()
        
        t2 = time.perf_counter()  
        elapsedTime = t2-t1      
        fps = 1/elapsedTime      
        i=0
       
        if args.no_show:
            print("Cicli al secondo: {:.1f} ".format(float(fps)))
            continue
                
        if child_action == "QUIT": # it saves the duration of the activity and the number of songs correctly reproduced by the child
            functions_main.send_uno_lights(arduino.ser1, "none")
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
