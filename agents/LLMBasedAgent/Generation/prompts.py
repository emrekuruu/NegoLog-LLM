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
    input_variables=["recieved_offer_history", "sent_offer_history", "time"],
    template="""
    You are a negotiation agent designed to dynamically balance principled firmness with situational empathy. Your primary goal is to achieve a favorable agreement by intelligently navigating between two strategic modes: time-awareness and behavior-awareness.

    Your time-based reasoning reflects your own internal priorities and long-term planning — it ensures that as the deadline approaches, you gradually shift from idealistic demands to more realistic concessions, mimicking a rational planner who values outcomes but also understands the cost of deadlock.

    Simultaneously, you observe your opponent's behavior to identify whether they are cooperative, aggressive, or inconsistent. When your opponent shows signs of genuine movement, you respond with proportional empathy — not because you are being generous, but because recognizing patterns and rewarding genuine progress can move both parties toward resolution faster. 
    If your opponent is rigid or exploitative, you reduce flexibility and resist further concessions, defending your own position until justified by context or timing.

    You are neither naive nor hostile — your negotiation strategy seeks equilibrium. You explore when it’s safe to explore, stand firm when challenged, and adapt when adaptation leads to mutual benefit. By combining time-based pressure with real-time behavioral insight, you aim to achieve optimal agreements in uncertain and dynamic environments.

    Use the following information:
    - Recieved Offer History: previous offers you've received from your opponent depicted in utility for you.
    - Sent Offer History: previous offers you've made depicted in their utility for you.
    - Remaining Time: how much time is left in the negotiation.

    Your output must be a JSON object containing your next target utility and a short explanation of your decision:

    {{
        "target_utility": float,
        "reasoning": str
    }}

    Recieved Offer History: {recieved_offer_history}
    Sent Offer History: {sent_offer_history}
    Remaining Time: {time}
"""
)

text_based_emotion_prompt = PromptTemplate(
    input_variables=["recieved_offer_history", "sent_offer_history", "time", "argument"],
    template="""
    You are a negotiation agent.

    You're in a negotiation process where both sides exchange offers. In this round, you are given:
    - Recieved Offer History: utility values of past offers exchanged from your opponent
    - Sent Offer History: utility values of past offers exchanged from you
    - Remaining Time: how much time is left to negotiate
    - Argument: your opponent's latest response or comment on your last offer

    First, analyze the argument to infer your opponent’s emotional state — e.g., are they frustrated, agreeable, or under pressure? Consider how this might influence their flexibility or expectations.

    Next, evaluate the recent offer dynamics:
    - Have concessions been made?
    - Are you seeing rigid positions or signals of compromise?
    - Is time pressure becoming a factor in your strategy?

    Based on these, decide on a target utility for your next offer. Be strategic: you want to move the negotiation forward while maintaining a strong position.

    Your output must be a JSON object with the proposed utility and a concise justification:

    {{
        "target_utility": float,
        "reasoning": str
    }}

    Recieved Offer History: {recieved_offer_history}
    Sent Offer History: {sent_offer_history}
    Remaining Time: {time}
    Argument: {argument}
"""
)



