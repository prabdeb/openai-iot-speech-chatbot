# Azure IoT Edge Solution

## Overview

This is a solution for Azure IoT Edge. It is based on the [Azure IoT Edge](https://docs.microsoft.com/en-us/azure/iot-edge/).

## Architecture

This solution is based on the following components:

- [GPT Skills](./modules/gptskills/README.md)
    - This module is responsible for generating text based on a prompt, where there are multiple skills (diferent prompts) that can be used to generate the text.
    - This uses the GPT3.5 model from Azure OpenAI.
    - This module is developed in Python after doing experiments in [Azure ML PromptFlow](https://learn.microsoft.com/en-us/azure/machine-learning/prompt-flow/overview-what-is-prompt-flow?view=azureml-api-2).
- [Orchestrator](./modules/orchestrator/README.md)
    - This module is responsible for orchestrating the GPT Skills and human interaction.
    - This module is developed in Python.
    - There are three primary block in it
        - Hearing the human voice via microphone and converting it to text using Azure Cognitive Services Speech to Text.
        - Generating text using GPT Skills.
        - Speaking the generated text via speaker using Azure Cognitive Services Text to Speech.

## Getting Started

To get started with this solution, you need to do the following:

### Prerequisites

- Azure Subscription
- Azure IoT Hub (Optional if you want to use Azure IoT Edge)
- Azure Container Registry (Optional if you want to use Azure IoT Edge)
- Azure OpenAI Service
- Azure Cognitive Services Speech to Text and Text to Speech
- Azure Bing Service (Web and News Search)
- Open Weather Map API Key
- Raspberry Pi 4 Model B
    - This solution consumes ~25% (1 core) of the CPU and ~1.5 GB of RAM.
- Microphone attached to the Raspberry Pi
- Speaker attached to the Raspberry Pi
- GPIO touch button or press button attached to the Raspberry Pi
    - Two required, one for starting the conversation and one for stopping it.

### Development

Standard Python development tools are required and any IDE can be used (Visual Studio Code, PyCharm, etc).

### Configuration

Create a `.env` file in this directory by copying the `.env.template` file and filling in the required values.

### Deployment (Azure IoT Edge)

To deploy this solution to Azure IoT Edge, you need to do the following:

- Create an Azure IoT Hub
- Create an Azure Container Registry
- Create an Azure IoT Edge Device
- Create an Azure IoT Edge Deployment
- Build and push the Azure IoT Edge Modules
- Deploy the Azure IoT Edge Deployment to the Azure IoT Edge Device

### Deployment (Systemd)

To deploy this solution to a Linux machine, you need to do the following:

- Install Python 3.9
- Install the required Python packages
- Install the required Linux packages
- Create a systemd service
- Start the systemd service

You can perform the above steps manually or use the [Makefile](../python_wheel_package/Makefile) to do it for you.
