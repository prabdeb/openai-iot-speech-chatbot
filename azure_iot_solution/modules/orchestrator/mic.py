import os
import threading
import wave
import pocketsphinx as ps
import pyaudio
import RPi.GPIO as GPIO
import requests
from stt import recognize_from_microphone
from tts import speak
import azure.cognitiveservices.speech as speechsdk

tmp_audio_file = "tmp.wav"
gpt_skill_endpoint = os.getenv("GPT_SKILL_ENDPOINT", "http://localhost:8000")

class MicrophoneThread(threading.Thread):
    SAMPLE_RATE = 44100
    CHUNK_SIZE = 8096
    FORMAT = pyaudio.paInt16
    WIDTH = 2
    CHANNELS = 1
    TOUCH_BUTTON = 2
    STOP_PIN_BUTTON = 3

    def __init__(self, callback):
        threading.Thread.__init__(self, target=self.run)
        self._stop_event = threading.Event()
        self._callback = callback
        self._is_speaking = False

        GPIO.setmode(GPIO.BCM) # type: ignore
        GPIO.setup(self.TOUCH_BUTTON, GPIO.IN) # type: ignore
        GPIO.setup(self.STOP_PIN_BUTTON, GPIO.IN) # type: ignore

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        self.stt = ps.Pocketsphinx()

        # Find best audio device to use.
        p = pyaudio.PyAudio()
        audio_device = int(self.get_audio_device(p))
        print('Using audio device: {}'.format(p.get_device_info_by_index(audio_device)))

        self.mic = p.open(format=self.FORMAT,
                     channels=self.CHANNELS,
                     rate=self.SAMPLE_RATE,
                     frames_per_buffer=self.CHUNK_SIZE,
                     input=True,
                     input_device_index=audio_device)
        self.mic.start_stream()

        self.process_mic(self.mic)

    def process_mic(self, mic):
        audio_frames = []
        speech_synthesizer = None
        print("Waiting for user to press the touch button ...")
        while not self.stopped():
            # Capture audio while the TOUCH_BUTTON is held.
            if GPIO.input(self.TOUCH_BUTTON) and self._is_speaking == False: # type: ignore
                if len(audio_frames) == 0:
                    print("Listening ...")

                frames = mic.read(self.CHUNK_SIZE, exception_on_overflow = False)
                audio_frames.append(frames)

            # The TOUCH_BUTTON is not held down, run speech-to-text.
            elif len(audio_frames) > 0:
                print("Processing {} bytes ... ".format(len(audio_frames)))
                waveFile = wave.open(tmp_audio_file, 'wb')
                waveFile.setnchannels(self.CHANNELS)
                waveFile.setsampwidth(self.WIDTH)
                waveFile.setframerate(self.SAMPLE_RATE)
                waveFile.writeframes(b''.join(audio_frames)) # type: ignore
                waveFile.close()

                # Call GPT skill.
                text = recognize_from_microphone(tmp_audio_file)
                if text:
                    gpt_response = self._call_gpt_skill(text)
                    print("GPT Response: {}".format(gpt_response))
                    if gpt_response:
                        print("Speaking ...")
                        self._is_speaking = True
                        speech_synthesizer = speak(gpt_response)
                        speech_synthesizer.synthesis_completed.connect(self.speech_synthesizer_synthesis_completed_cb)

                # Reset audio frames.
                audio_frames = []

            # Stop the speech synthesizer if the STOP_PIN_BUTTON is pressed.
            elif GPIO.input(self.STOP_PIN_BUTTON) and speech_synthesizer: # type: ignore
                print("Stopping speech synthesizer ...")
                speech_synthesizer.stop_speaking()
                speech_synthesizer = None
                print("Waiting for user to press the touch button ...")

    def get_audio_device(self, p):
        index = 0
        for i in range(p.get_device_count()):
            di = p.get_device_info_by_index(i)
            if di['name'].startswith(os.getenv('AUDIO_DEVICE_NAME', 'USB PnP Audio Device')):
                return di['index']
            if di['name'] == 'default':
                index = i

        # Return 'default' sound device, if found.
        return index

    def _call_gpt_skill(self, question: str) -> str:
        """Call GPT skill"""
        response = requests.get(f"{gpt_skill_endpoint}/gpt/itenet?q={question}")
        return response.json()["message"]

    def _get_gpt_skill_status(self) -> str:
        """Get GPT skill status"""
        response = requests.get(f"{gpt_skill_endpoint}/gpt/status")
        return response.json()["message"]

    def speech_synthesizer_synthesis_completed_cb(self, evt: speechsdk.SessionEventArgs):
        print("Waiting for user to press the touch button ...")
        self._is_speaking = False
