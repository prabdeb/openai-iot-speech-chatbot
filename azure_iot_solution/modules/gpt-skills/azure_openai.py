import openai
import os
from retry import retry
from typing import List, Dict

VALID_ROLES = ['system', 'user', 'assistant']

def initialize_openai():
    """Load OpenAI API key from configs"""
    openai.api_key = os.getenv("AZURE_OPENAI_API_KEY", None)
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", None)
    if endpoint:
        if endpoint.find(".azure.com") != -1:
            openai.api_type = "azure"
            openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION", None)
        openai.api_base = endpoint

def check_if_openai_is_initialized() -> bool:
    """Check if OpenAI is initialized"""
    if not openai.api_key or not openai.api_base or not openai.api_version:
        return False
    return True

@retry(tries=3, delay=0.1, jitter=(0, 2), backoff=2, max_delay=2)
def generate_chat_completion(messages: List[Dict[str, str]], **kwargs) -> str:
    """
    Calls OpenAI for the model input and stores results to model outputs

    It will raise a ValueError if the prompt is not set
    """
    if not messages:
        raise ValueError("messages must be set")

    completion = openai.ChatCompletion.create(
        engine=os.getenv("AZURE_OPENAI_CHATBOT_MODEL", None),
        messages=messages,
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", None),
        **kwargs,
    )

    return completion # type: ignore

def parse_prompt_gpt_35(file_name: str, **kwargs: str) -> List[Dict[str, str]]:
    """
    Parse the prompt file for GPT-3.5 based prompts defined in AML PromptFlow.

    Input file format:
    <role>: <prompt>
    ...
    <role>: <prompt>

    Returns a list of dictionaries with the following format:
    [
        {'role': <role>, 'content': <prompt>},
        ...
    ]
    """
    messages = []
    f = open(file_name, 'r')
    try:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        current_role = None
        current_role_content = ""
        next_role = None
        for line in lines:
            if line.startswith(tuple([role + ':' for role in VALID_ROLES])):
                next_role = line.split(':')[0]
                if current_role is not None and current_role != next_role:
                    messages.append({'role': current_role, 'content': current_role_content})
                current_role = next_role
                if len(line.split(':')) == 2:
                    current_role_content = line.split(':')[1] + '\n'
                else:
                    current_role_content = ""
            else:
                current_role_content += line + '\n'
            for key, value in kwargs.items():
                current_role_content = current_role_content.replace('{{' + key + '}}', value)
        messages.append({'role': current_role, 'content': current_role_content})
        return messages
    finally:
        f.close()
