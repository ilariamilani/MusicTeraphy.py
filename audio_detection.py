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
LOW_THRESHOLD = 35

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
Nbeat = 0
#deltaT = 0.095
deltaT = 0
silence = 0 #pause between beats
noise = 0

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
        noise += 1
        if Nbeat == 0:
            t.start() #oppure timer parte prima e alla fine sottraggo il valore temporale del primo battito
            print("start timer")
            #clap_time.append(t.elapsed_time())
            clap_time.append(0)
            print("performance started")
            print("clap")
            print(clap_time[Nbeat])
            Nbeat += 1
            silence = 0
        else :
            deltaT = t.elapsed_time() - clap_time[Nbeat-1]
            if (deltaT > 0.093) and (silence >= 1):
                # test a 85 BPM devo avere un battito ogni 0.7 sec
                print("clap")
                clap_time.append(t.elapsed_time())
                print(clap_time[Nbeat])
                print(clap_time[:])
                Nbeat += 1
                silence = 0
            if silence == 0 and noise >= 10 :
                print("other activity is detected")
    elif decibel < LOW_THRESHOLD:
            silence += 1
            noise = 0
            #print("silence")
            if silence >= 20:
                print("no activity detected from the child")
    continue

t.stop()

# stop and close the stream
stream.stop_stream()
stream.close()

# close PyAudio
p.terminate()
