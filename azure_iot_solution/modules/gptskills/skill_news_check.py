from .azure_openai import generate_chat_completion, check_if_openai_is_initialized, initialize_openai, parse_prompt_gpt_35
import requests, os
import datetime
import logging

logger = logging.getLogger("uvicorn")
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

def get_news_check(question: str, entities: str) -> str:
    """Get general knowledge from text"""
    if not check_if_openai_is_initialized():
        initialize_openai()
    current_directory = os.path.dirname(os.path.realpath(__file__))
    news_context = _get_news_context(question, entities)
    messages = parse_prompt_gpt_35(f"{current_directory}/prompts/news_check.txt",
                                   news_context=news_context,
                                   question=question,)
    return generate_chat_completion(
        messages=messages,
        max_tokens=300,
        temperature=1.0,
    ).choices[0]["message"]["content"] # type: ignore

def _get_news_context(question: str, entities: str) -> str:
  subscription_key = os.getenv("AZURE_BING_SEARCH_API_KEY", "")
  endpoint = os.getenv("AZURE_BING_SEARCH_ENDPOINT", "")
  mkt = 'en-IN'
  params = { 'q': entities, 'mkt': mkt }
  headers = { 'Ocp-Apim-Subscription-Key': subscription_key }
  endpoint = endpoint + "/v7.0/news/search"
  response = requests.get(endpoint, headers=headers, params=params)
  content = response.json()
  news_context = ""
  news_context = news_context + "Current Date and Time: " + str(datetime.datetime.now()) + "\n\n"
  for article in content["value"]:
    news_context += "Description: " + article["description"] + "\n"
    news_context += "Provider: " + article["provider"][0]["name"] + "\n"
    news_context += "Date Published: " + article["datePublished"] + "\n\n"

  return news_context
