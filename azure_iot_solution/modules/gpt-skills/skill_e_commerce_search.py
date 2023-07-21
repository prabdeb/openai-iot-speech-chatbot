from azure_openai import generate_chat_completion, check_if_openai_is_initialized, initialize_openai, parse_prompt_gpt_35
import requests, os

def get_e_commerce_search(question: str, entities: str) -> str:
    """Get general knowledge from text"""
    if not check_if_openai_is_initialized():
        initialize_openai()
    products_context = _get_products_context(entities)
    messages = parse_prompt_gpt_35("./prompts/e_commerce_search.txt",
                                   products_context=products_context,
                                   query=question)
    return generate_chat_completion(
        messages=messages,
        max_tokens=300,
        temperature=1.0,
    ).choices[0]["message"]["content"] # type: ignore

def _get_products_context(entities: str) -> str:
  subscription_key = os.getenv("AZURE_BING_SEARCH_API_KEY", "")
  endpoint = os.getenv("AZURE_BING_SEARCH_ENDPOINT", "")
  mkt = 'en-IN'
  headers = { 'Ocp-Apim-Subscription-Key': subscription_key }
  endpoint = endpoint + "/v7.0/search"
  product_context = ""
  q_entities = entities + "site:amazon.in"
  params = { 'q': q_entities, 'mkt': mkt }
  response = requests.get(endpoint, headers=headers, params=params)
  content = response.json()
  product_context += "Products from Amazon:\n\n"
  for i, article in enumerate(content["webPages"]["value"]):
    item = i + 1
    product_context += f"{item}. " + article["snippet"] + "\n"
    if i == 4:
      break
  product_context += "\n"
  q_entities = entities + "site:flipkart.com"
  params = { 'q': q_entities, 'mkt': mkt }
  response = requests.get(endpoint, headers=headers, params=params)
  content = response.json()
  product_context += "Products from Flipkart:\n\n"
  for i, article in enumerate(content["webPages"]["value"]):
    item = i + 1
    product_context += f"{item}. " + article["snippet"] + "\n"
    if i == 4:
      break

  return product_context
