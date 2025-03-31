import logging
from . import Openai, Claude, Google
from .prompts import *

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def text_based(recieved_offer_history, sent_offer_history, time, argument, model_type):
    provider = model_type.split("-")[0]
    model = model_type[len(provider)+1:]

    if argument is not None:
        prompt = text_based_emotion_prompt.format(recieved_offer_history=recieved_offer_history, sent_offer_history=sent_offer_history, time=time, argument=argument)
    else:
        prompt = text_based_emotionless_prompt.format(recieved_offer_history=recieved_offer_history, sent_offer_history=sent_offer_history, time=time)

    if provider == "openai":
        response = await Openai.text_based(model, prompt)
    elif provider == "claude":
        response = await Claude.text_based(model, prompt)
    elif provider == "google":
        response = await Google.text_based(model, prompt)
    else:
        raise ValueError(f"Invalid model type: {model_type}")

    return response.target_utility, response.reasoning