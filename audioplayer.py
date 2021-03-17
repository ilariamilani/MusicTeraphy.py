import pyaudio
import wave
import time
import threading

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "file.wav"
THREESHOLD = 5

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

class PlayAudio:

    def __init__(self):
        self.wf = None
        self.stream = None

    def play(self, wav_file):
        with suppress_stdout_stderr:
            self.wf = wave.open(wav_file, 'rb')
            p = pyaudio.PyAudio()
            self.stream = p.open(format=p.get_format_from_width(self.wf.getsampwidth()),
                                 channels=self.wf.getnchannels(),
                                 rate=self.wf.getframerate(),
                                 output=True,
                                 stream_callback=self.callback)
            self.stream.start_stream()
            while self.stream.is_active():
                time.sleep(0.1)
            # stop stream (6)
            self.stream.stop_stream()
            self.stream.close()
            self.wf.close()
            # close PyAudio (7)
            p.terminate()

    # define callback (2)
    def callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        return data, pyaudio.paContinue
