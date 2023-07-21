from azure_openai import generate_chat_completion, check_if_openai_is_initialized, initialize_openai, parse_prompt_gpt_35
import requests, os
import datetime
import logging

logger = logging.getLogger("uvicorn")
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

def get_weather_check(entities: str) -> str:
    """Get general knowledge from text"""
    if not check_if_openai_is_initialized():
        initialize_openai()
    weather_context = _get_open_weather_map(entities)
    messages = parse_prompt_gpt_35("./prompts/weather_check.txt",
                                   weather_context=weather_context)
    return generate_chat_completion(
        messages=messages,
        max_tokens=100,
        temperature=0.5,
    ).choices[0]["message"]["content"] # type: ignore

def _get_open_weather_map(entities: str) -> str:
  api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY", "")
  base_url = "http://api.openweathermap.org/data/2.5/forecast?"
  complete_url = base_url + "appid=" + api_key + "&q=" + entities
  logger.info(f"Complete URL: {complete_url}")
  response = requests.get(complete_url)
  content = response.json()
  weather_context = ""
  weather_context = weather_context + "City: " + content['city']['name'] + "\n"
  weather_context = weather_context + "Current Time: " + str(datetime.datetime.now()) + "\n"
  weather_context = weather_context + "Sunset Time: " + str(datetime.datetime.fromtimestamp(content['city']['sunset'])) + "\n"
  weather_context = weather_context + "\n"
  for item in content['list']:
      weather_context = weather_context + "Future Time: " + item['dt_txt'] + "\n"
      weather_context = weather_context + "Cloudiness: " + str(item['clouds']['all']) + "%" + "\n"
      weather_context = weather_context + "Temperature: " + str(round(item['main']['temp'] - 273.15, 2)) + "°C" + "\n"
      weather_context = weather_context + "Humidity: " + str(item['main']['humidity']) + "%" + "\n"
      weather_context = weather_context + "Description: " + item['weather'][0]['description'] + "\n"
      if "rain" in item:
          weather_context = weather_context + "Rain: " + str(item['rain']['3h']) + "mm" + "\n"
      weather_context = weather_context + "\n"
  return weather_context
