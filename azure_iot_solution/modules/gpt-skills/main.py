from typing import List
from fastapi import FastAPI
import logging
from skill_intent_detection import get_intent
from skill_general_knowledge import get_general_knowledge
from skill_general_greetings import get_general_greetings
from skill_any_other import get_any_other

logger = logging.getLogger("gptskills")
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
logger.info("Starting GPT-3.5 Custom Skills")

app = FastAPI()
VALID_INTENTS = ['general_greetings', 'weather_check', 'news_check', 'e_commerce_search', 'story_telling', 'general_knowledge', 'any_other']

@app.get("/")
async def root():
    return {"message": "Welcome to GPT-3.5 Custom Skills"}

@app.get("/gpt/itenet")
async def itenet(q: str = ""):
    try:
        if q == "":
            logger.error("No question provided")
            return {"message": "No question was asked."}
        logger.info(f"Question: {q}")
        intent_with_context = get_intent(q)
        logger.info(f"Intent with context: {intent_with_context}")
        intent, entities = _parse_intent_with_context(intent_with_context)
        if intent not in VALID_INTENTS:
            logger.error(f"Unsuppored intent: {intent}")
            return {"message": f"Invalid intent detected, it must be one of the following {VALID_INTENTS}."}
        response = _route(q, intent, entities)
        logger.info(f"Response: {response}")
        if response == "":
            logger.error("Empty response")
            return {"message": "Sorry I don't have an answer for that."}
        return {"message": response}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"message": "Runtime error occurred, contact support."}

@app.get("/gpt/status")
async def status():
    return {"message": "Hello World"}

def _route(question: str, intent: str, entities: str):
    if intent == "general_greetings":
        return get_general_greetings(entities)
    # elif intent == "weather_check":
    #     return _weather_check(entities)
    # elif intent == "news_check":
    #     return _news_check(entities)
    # elif intent == "e_commerce_search":
    #     return _e_commerce_search(entities)
    # elif intent == "story_telling":
    #     return _story_telling(entities)
    elif intent == "general_knowledge":
        return get_general_knowledge(question)
    elif intent == "any_other":
        return get_any_other()
    else:
        raise ValueError(f"Invalid intent: {intent}")

def _parse_intent_with_context(intent_answer: str) -> List[str]:
  intent_answer = intent_answer.replace("\n", " ")
  intent = intent_answer.split("intent: ")[1].split(" entities:")[0]
  entities = intent_answer.split(" entities: ")[1]

  return [intent, entities]
