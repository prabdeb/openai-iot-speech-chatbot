from azure_openai import generate_chat_completion, check_if_openai_is_initialized, initialize_openai, parse_prompt_gpt_35

def get_general_greetings(question: str, entities: str) -> str:
    """Get general knowledge from text"""
    if not check_if_openai_is_initialized():
        initialize_openai()
    messages = parse_prompt_gpt_35("./prompts/general_greetings.txt",
                                   general_context=question)
    return generate_chat_completion(
        messages=messages,
        max_tokens=100,
        temperature=0.5,
    ).choices[0]["message"]["content"] # type: ignore
