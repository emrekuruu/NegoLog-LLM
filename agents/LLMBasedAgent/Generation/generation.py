import logging
from . import Openai, Claude, Google
from .prompts import *
import asyncio
import json

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def text_based(recieved_offer_history, sent_offer_history, time, argument, issue_weights, value_weights, reservation_value, offer_schema, Offer, model_type):
    provider = model_type.split("-")[0]
    model = model_type[len(provider)+1:]

    if argument is not None:
        prompt = text_based_emotion_prompt.format(recieved_offer_history=recieved_offer_history, sent_offer_history=sent_offer_history, time=time, argument=argument)
    else:
        prompt = text_based_emotionless_prompt.format(recieved_offer_history=recieved_offer_history, sent_offer_history=sent_offer_history, time=time, issue_weights=issue_weights, value_weights=value_weights, reservation_value=reservation_value, offer_schema=offer_schema)

    # logger.info(f"Prompt: {prompt}")

    if provider == "openai":
        response = Openai.text_based(model, prompt, Offer)
    elif provider == "claude":
        response = Claude.text_based(model, prompt, Offer)
    elif provider == "google":
        response = Google.text_based(model, prompt, Offer)
    else:
        raise ValueError(f"Invalid model type: {model_type}")

    response = json.loads(response.model_dump_json())
    return response