import signal
from .mic import MicrophoneThread


if __name__ == "__main__":
    # Start a background thread to parse audio from the microphone.
    mic = MicrophoneThread(callback=None)

    def signal_handler(signal, frame):
        mic.stop()

    signal.signal(signal.SIGINT, signal_handler)

    mic.start()
    mic.join()
