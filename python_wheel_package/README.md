# Deploy as Systemd service

## Prerequisites

All prerequisites as mentined in [Azure IoT Solution](../azure_iot_solution/README.md) are required. The Azure IoT services are not required.

## Configuration

- Create the `.env` file by copying the `.env.template` file and filling in the required values under `azure_iot_solution` directory.

## Deployment

- Run the following commands to build the wheel package:

```bash
make build
```

- Run the following commands to install the wheel package:

```bash
make install
```

- Run the following commands to install update the wheel package:

```bash
make install-force
```

- Run the following commands to deploy the systemd service:

```bash
make service
```

- Run the following commands to stop and disable the systemd service:

```bash
make service-stop
```

- Run the following commands to uninstall the wheel package:

```bash
make uninstall
```

## Testing

Just press/touce the button to start the conversation and speak to the microphone. The speaker will speak the generated text. Press/touch the button to stop the conversation to stop the conversation.
