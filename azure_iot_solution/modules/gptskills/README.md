# GPT Skills

This module contains the GPT Skills that are used by the Orchestrator to generate text.

## Overview

This module contains the following skills:

- Intent detection skill
    - This skill is used to detect the intent of the user and extract the entities (if any).
    - This is the first skill that is used by the Orchestrator.
    - Based on the intent, the Orchestrator will use the appropriate skill to generate the text.
- General greeting skill
    - This skill is used to greet the user.
- Weather skill
    - This skill is used to get the weather information based on the entities extracted by the Intent detection skill.
    - This uses the Open Weather Map API to get latest weather information (top 10 results).
- News skill
    - This skill is used to get the latest news based on the entities extracted by the Intent detection skill.
    - This uses the Bing News Search API to get latest news (top 10 results).
- E-Commerce skill
    - This skill is used to find the latest products based on the entities extracted by the Intent detection skill.
    - This uses the Bing Web Search API to get latest products.
        - Top 5 results from Amazon
        - Top 5 results from Flipkart
- General Knowledge skill
    - This skill is used to get the general knowledge based on the entities extracted by the Intent detection skill.
- Storry Teller skill
    - This skill is used to tell a story based on the entities extracted by the Intent detection skill.
    - This is configired to tell a story for a 4 year old kid.
- Any Other skill
    - This skill is used when the Intent detection skill is not able to detect the intent of the user.

## Development

Standard Python development tools are required and any IDE can be used (Visual Studio Code, PyCharm, etc).

## Local Testing

- Create the `.env` file by copying the `.env.template` file and filling in the required values under `azure_iot_solution` directory.
- Run the following commands to source the `.env` file:

```bash
export $(grep -v '^#' ../../.env | xargs)
```

- Run the following command to run the module:

```bash
python3 -m main.py
```

- This will create an API endpoint at `http://localhost:8000/gpt/itenet?q=<query>` that can be used to generate text.
