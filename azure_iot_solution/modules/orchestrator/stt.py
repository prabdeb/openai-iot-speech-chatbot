import os
import azure.cognitiveservices.speech as speechsdk


def recognize_from_microphone(tmp_audio_file: str) -> str:
    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv('AZURE_COGNIOTIVE_SERVICE_KEY', None),
       region=os.getenv('AZURE_COGNIOTIVE_SERVICE_REGION', None))
    speech_config.speech_recognition_language="en-US"

    audio_input = speechsdk.AudioConfig(filename=tmp_audio_file)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech: # type: ignore
        print("Recognized: {}".format(speech_recognition_result.text)) # type: ignore
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch: # type: ignore
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details)) # type: ignore
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled: # type: ignore
        cancellation_details = speech_recognition_result.cancellation_details # type: ignore
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

    # Delete the temporary file.
    os.remove(tmp_audio_file)

    return speech_recognition_result.text # type: ignore
