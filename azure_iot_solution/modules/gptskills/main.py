from typing import List
from fastapi import FastAPI
import uvicorn
import logging
from .skill_intent_detection import get_intent
from .skill_general_knowledge import get_general_knowledge
from .skill_general_greetings import get_general_greetings
from .skill_any_other import get_any_other
from .skill_story_telling import get_story_telling
from .skill_weather_check import get_weather_check
from .skill_news_check import get_news_check
from .skill_e_commerce_search import get_e_commerce_search

logger = logging.getLogger("uvicorn")
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)
logger.info("Starting GPT-3.5 Custom Skills")

class StatusLock:
    def __init__(self):
        self._status = False

    def set_status(self, status: bool):
        self._status = status

    def get_status(self):
        return self._status

app = FastAPI()
VALID_INTENTS = [
    'general_greetings',
    'weather_check',
    'news_check',
    'e_commerce_search',
    'story_telling',
    'general_knowledge',
    'any_other',
    'multiturn'
]
running_status = StatusLock()

@app.get("/")
async def root():
    return {"message": "Welcome to GPT-3.5 Custom Skills"}

@app.get("/gpt/itenet")
async def itenet(q: str = ""):
    try:
        running_status.set_status(True)
        if q == "":
            logger.error("No question provided")
            return {"message": "No question was asked."}
        logger.info(f"Question: {q}")
        intent_with_context = get_intent(q)
        intent, entities = _parse_intent_with_context(q, intent_with_context)
        logger.info(f"Intent: {intent}")
        logger.info(f"Entities: {entities}")
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
        logger.exception(e)
        return {"message": "Runtime error occurred, contact support."}
    finally:
        running_status.set_status(False)

@app.get("/gpt/status")
async def status():
    return {"message": running_status.get_status()}

def _route(question: str, intent: str, entities: str):
    if intent == "general_greetings":
        return get_general_greetings(question, entities)
    elif intent == "weather_check":
        return get_weather_check(question, entities)
    elif intent == "news_check":
        return get_news_check(question, entities)
    elif intent == "e_commerce_search":
        return get_e_commerce_search(question, entities)
    elif intent == "story_telling":
        return get_story_telling(question, entities)
    elif intent == "general_knowledge":
        return get_general_knowledge(question)
    elif intent == "any_other":
        return get_any_other()
    elif intent == "multiturn":
        return entities
    else:
        raise ValueError(f"Invalid intent: {intent}")

def _parse_intent_with_context(question: str, intent_answer: str) -> List[str]:
    intent_answer = intent_answer.replace("\n", " ")
    logger.info(f"Intent answer: {intent_answer}")
    try:
        intent = intent_answer.split("intent: ")[1].split(" entities:")[0]
        intent = intent.replace(".", "")
        intent = "".join(intent.split())
    except IndexError:
        intent = "multiturn"
        entities = intent_answer
        return [intent, entities]
    try:
        entities = intent_answer.split(" entities: ")[1]
    except IndexError:
        entities = question

    return [intent, entities]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
