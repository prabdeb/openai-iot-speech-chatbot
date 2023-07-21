import os
import azure.cognitiveservices.speech as speechsdk

def speak(text: str) -> speechsdk.SpeechSynthesizer:
    speech_config = speechsdk.SpeechConfig(
        subscription=os.getenv('AZURE_COGNIOTIVE_SERVICE_KEY', None),
       region=os.getenv('AZURE_COGNIOTIVE_SERVICE_REGION', None))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True) # type: ignore

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='en-IN-PrabhatNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesizer.speak_text_async(text)
    return speech_synthesizer
    # speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    # speech_synthesizer.stop_speaking()

    # if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted: # type: ignore
    #     print("Speech synthesized is done playing.")
    # elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled: # type: ignore
    #     cancellation_details = speech_synthesis_result.cancellation_details # type: ignore
    #     print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #         if cancellation_details.error_details:
    #             print("Error details: {}".format(cancellation_details.error_details))
    #             print("Did you set the speech resource key and region values?")
