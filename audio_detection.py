import audioop
import pyaudio
import math
import time
import wave
from timer import Timer
from playaudio import PlayAudio
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100 # Record at 44100 samples per second
CHUNK = 1024 * 2 # Number of samples in a chunk
# this is the threshold that determines whether or not sound is detected
THRESHOLD = 45

clap_time = []


# instantiate PyAudio
p = pyaudio.PyAudio() # Create an interface to PortAudio

t = Timer()

#open your audio stream
stream = p.open(format=FORMAT,
                rate=RATE,
                channels=CHANNELS,
                input=True,
                output=True,
                frames_per_buffer=CHUNK)
                #stream_callback=callback) possibile AGGIUNTA

# start the stream
stream.start_stream()
time.sleep(2)
#t.start()
i = 0
#deltaT = 0.095
deltaT = 0

# wait until the sound data breaks some level threshold
while True:
    data = stream.read(CHUNK)
    rms = audioop.rms(data, 2)  # quadratic mean of the data. width=2 for format=paInt16
    #print(rms)
    if rms == 0:
        decibel = 0
    else :
        decibel = 20 * math.log10(rms)  # transforms into db
    # check level against threshold
    print(decibel)
    if decibel > THRESHOLD:
        if i == 0:
            t.start()
            print("start timer")
            #clap_time.append(t.elapsed_time())
            clap_time.append(0)
            print("performance started")
            print("clap")
            print(clap_time[i])
            i = i + 1
        else :
            deltaT = t.elapsed_time() - clap_time[i-1]
            if (deltaT > 0.093) :
                # test a 85 BPM devo avere un battito ogni 0.7 sec
                print("clap")
                clap_time.append(t.elapsed_time())
                print(clap_time[i])
                print(clap_time[:])
                i = i + 1
    else:
        print("silence")
    continue

t.stop()

# stop and close the stream
stream.stop_stream()
stream.close()

# close PyAudio
p.terminate()
