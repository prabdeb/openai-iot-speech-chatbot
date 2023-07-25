# Orchestrator

This module is responsible for orchestrating the GPT Skills and human interaction.

## Overview

The flow of this module is as follows:

- Detect if the user has pressed/touched the button to start the conversation.
- Hearing the human voice via microphone once the conversation has started.
- Converting it to text using Azure Cognitive Services Speech to Text.
- Generating text using GPT Skills.
- Speaking the generated text via speaker using Azure Cognitive Services Text to Speech.
- Detect if the user has pressed/touched the button to stop the conversation.
- Stop the conversation if the user has pressed/touched the button to stop the conversation.

## Configuration

- Connect the microphone and speaker to the Raspberry Pi.
- Configure the connected speaker as the default speaker.
- Configure the connected microphone name in the `.env` file.
    - The default value is `USB PnP Audio Device`.
- Connect two GPIO buttons to the Raspberry Pi.
    - GPIO Pin 2 - For starting the conversation.
    - GPIO Pin 3 - For stopping the conversation.
    - The current channel is 1 for the microphone.

## Development

Standard Python development tools are required and any IDE can be used (Visual Studio Code, PyCharm, etc) and Raspberry Pi 4 Model B.

## Local Testing

- Create the `.env` file by copying the `.env.template` file and filling in the required values under `azure_iot_solution` directory.
- Run the following commands to source the `.env` file:

```bash
export $(grep -v '^#' ../../.env | xargs)
```

- Run the following command to increase the volume of the speaker:

```bash
alsamixer
```

- Run the following command to test the speaker:

```bash
speaker-test -t wav -c 2
```

- Run the following command to test the microphone:

```bash
arecord -D plughw:1,0 -f cd -c 1 -r 48000 -d 5 -t wav -v test.wav
aplay test.wav
```

- Run the following command to run the module:

```bash
python3 -m main.py
```

- This will start the conversation when the user presses/touches the button connected to GPIO Pin 2.
