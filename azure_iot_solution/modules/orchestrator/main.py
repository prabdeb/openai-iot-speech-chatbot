import os
import signal
import dotenv
from .mic import MicrophoneThread


if __name__ == "__main__":
    environment_file = ".openai_iot"
    home = os.path.expanduser("~")
    if os.path.isfile(os.path.join(home, environment_file)):
        print(f"Loading environment variables from file: {os.path.join(home, environment_file)}")
        dotenv.load_dotenv(os.path.join(home, environment_file))

    mic = MicrophoneThread(callback=None)

    def signal_handler(signal, frame):
        mic.stop()

    signal.signal(signal.SIGINT, signal_handler)

    mic.start()
    mic.join()
