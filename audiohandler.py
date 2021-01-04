import numpy as np
import pyaudio
import time
import librosa


class AudioHandler(object):
    def __init__(self):
        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024 * 250 # circa 3 secondi di audio da analizzare alla volta
        self.p = None
        self.stream = None
        #self.variabili controllo performance bimbo

    def start(self):
        self.p = pyaudio.PyAudio()
        print(self.p.get_default_input_device_info())
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  output=False,
                                  stream_callback=self.callback,
                                  frames_per_buffer=self.CHUNK)

    def stop(self):
        self.stream.close()
        self.p.terminate()

    #ogni quanto pyaudio chiama callback???
    def callback(self, in_data, frame_count, time_info, flag):
        #if robot is not speaking
        numpy_array = np.frombuffer(in_data, dtype=np.float32)
        tempo, beat_frames = librosa.beat.beat_track(y=numpy_array, sr=self.RATE)
        onset_env = librosa.onset.onset_strength(y=numpy_array, sr=self.RATE)
        pulse = librosa.beat.plp(onset_envelope=onset_env, sr=self.RATE)
        print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
        print(beat_frames)
       # print("Beat principale : ", np.flatnonzero(librosa.util.localmax(pulse)))
        #beat_times = librosa.frames_to_time(beat_frames, self.RATE)
       # print(beat_times)
        return None, pyaudio.paContinue

    def mainloop(self):
        while (self.stream.is_active()):# if using button you can set self.stream to 0 (self.stream = 0), otherwise you can use a stop condition
            continue

            #trasformo in funz isactive chiamato da funz listen da main
        #if db> continue
        #else stop callback

        #play interazione con bimbo: wow, si, no


#audio = AudioHandler()
#audio.start()  # open the the stream
#audio.mainloop()  # main operations with librosa
#audio.stop()
