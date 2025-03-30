import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
import asyncio
import random
from functools import wraps

load_dotenv()

def exponential_retry(max_retries=3, base_delay=1, jitter=0.1):
    """
    Decorator that applies exponential backoff retry logic to async functions.
    
    Args:
        max_retries (int): Maximum number of retry attempts
        base_delay (float): Base delay in seconds between retries
        jitter (float): Random jitter factor to add to delay
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries > max_retries:
                        raise e
                    
                    # Calculate exponential backoff with jitter
                    delay = base_delay * (2 ** (retries - 1))
                    delay += random.uniform(0, jitter * delay)
                    
                    print(f"API request failed. Retrying in {delay:.2f} seconds... (Attempt {retries}/{max_retries})")
                    await asyncio.sleep(delay)
            
        return wrapper
    return decorator

class Offer(BaseModel):
    target_utility : float
    reasoning : str

text_based_emotionless_prompt = PromptTemplate(
    input_variables=["offer_history", "time"],
    template="""
    You are a negotiation agent.

    You are given the history of the given and received offer's utility between you and your opponent and the remaining time of the negotiation.

    You need to determine the target utility for the next offer.

    Your response should be a json object with the following fields, Where the target_utility is the utility of the next offer and the reasoning is the reasoning for the target utility:

    {{
        "target_utility": float,
        "reasoning": str
    }}

    Offer History: {offer_history}
    Remaining Time: {time}
"""
)

text_based_emotion_prompt = PromptTemplate(
    input_variables=["offer_history", "time", "argument"],
    template="""
    You are a negotiation agent.

    You are given the history of the given and received offer's utility between you and your opponent and the remaining time of the negotiation and the argument your opponent made in response to your last offer.

    First consider the argument your opponent made. Decide on their emotional state.

    Whether they are pleased, frustrated or worried. Consider this in your decision making process.

    Then, consider the offer history and the remaining time.

    Now, make a decision based on the above information.

    You need to determine the target utility for the next offer.

    Your response should be a json object with the following fields, Where the target_utility is the utility of the next offer and the reasoning is the reasoning for the target utility:

    {{
        "target_utility": float,
        "reasoning": str
    }}

    Offer History: {offer_history}
    Remaining Time: {time}
    Argument: {argument}
"""
)


