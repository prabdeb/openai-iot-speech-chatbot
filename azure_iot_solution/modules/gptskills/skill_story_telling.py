import os
from .azure_openai import generate_chat_completion, check_if_openai_is_initialized, initialize_openai, parse_prompt_gpt_35

def get_story_telling(question: str, entities: str) -> str:
    """Get general knowledge from text"""
    if not check_if_openai_is_initialized():
        initialize_openai()
    current_directory = os.path.dirname(os.path.realpath(__file__))
    messages = parse_prompt_gpt_35(f"{current_directory}/prompts/story_telling.txt",
                                   story_context=entities)
    return generate_chat_completion(
        messages=messages,
        max_tokens=300,
        temperature=0.5,
    ).choices[0]["message"]["content"] # type: ignore
