# check for voice's direction and echo
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
               if ((meanAngle >= 170 ) and (meanAngle <= 190)): # sounds from the front
                   soundDirection = "FRONT"
               elif ((meanAngle >= 190) and (meanAngle <= 315)): # sounds from the right
                   soundDirection = "RIGHT"
               elif ((meanAngle >= 45) and (meanAngle <= 170)): # sounds from the left
                   soundDirection = "LEFT"
               elif (((meanAngle >= 315) or (meanAngle <= 45))): # sounds from the back
                   soundDirection = "BACK"

            #if ((echo == 1) or (meanAngle >= 0)):
             #   waitingForSounds = 0
