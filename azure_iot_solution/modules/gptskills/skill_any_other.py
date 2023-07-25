import os
from .azure_openai import generate_chat_completion, check_if_openai_is_initialized, initialize_openai, parse_prompt_gpt_35

def get_any_other() -> str:
    """Get general knowledge from text"""
    if not check_if_openai_is_initialized():
        initialize_openai()
    current_directory = os.path.dirname(os.path.realpath(__file__))
    messages = parse_prompt_gpt_35(f"{current_directory}/prompts/any_other.txt")
    return generate_chat_completion(
        messages=messages,
        max_tokens=100,
        temperature=1,
    ).choices[0]["message"]["content"] # type: ignore
