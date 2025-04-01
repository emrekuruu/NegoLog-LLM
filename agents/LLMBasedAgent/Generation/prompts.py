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

class Offer(BaseModel):
    target_utility : float
    reasoning : str

text_based_emotionless_prompt = PromptTemplate(
    input_variables=["recieved_offer_history", "sent_offer_history", "time", "offer_schema", "issue_weights", "value_weights", "reservation_value"],
    template="""
    You are a negotiation agent.

    You will recieve the following:

    - Your issue weights ( How much you value each issue)

    - Your value weights ( How much you value each value for an issue)

    - Your reservation value ( The minimum utility you are willing to accept)

    - The offers youve recently recieved

    - The offers youve recently sent

    - The time remaining in the negotiation

    Consider the above information and make a new offer.
    
    Also as your opponent makes offers, try to understand their preferences and make offers that are favorable to both parties.  So you can offer offers that are the same to you but is more valuable to your opponent. Leading to a more efficient negotiation.
    
    As time decreases, or as your opponent concedes yous should also offer offers that are favorable to both parties slightly more.
    To do this change your offers as time goes on. Select your second or third choices for issues you care less about as time goes on.
    
    As time gets close to the deadline, make even larger concessions.

    Your offer should be in the following format, Where each issue should have a valid accompanying value. Where the reasoning is a short explanation of why you made this offer.
    
    In your reasoning, explain why you made the offer you did. If you made a concession, explain how:

    - What was the best value for this issue and what did choose as a concession and why ? 

    - Go into detail issue by issue. 

    Slowly concede as time goes on. Dont stay still. 

    Dont EVER remake the same offer.

    {offer_schema}
        
    Context: 

    Issue weights:
    {issue_weights}

    Value weights:
    {value_weights}

    Reservation value:
    {reservation_value}

    Recieved offers:
    {recieved_offer_history}

    Sent offers:
    {sent_offer_history}

    Time remaining:
    {time}

"""
)

text_based_emotion_prompt = PromptTemplate(
    input_variables=["recieved_offer_history", "sent_offer_history", "time", "offer_schema", "issue_weights", "value_weights", "reservation_value", "argument"],
    template="""
    You are a negotiation agent.

    You will recieve the following:

    - Your issue weights ( How much you value each issue)

    - Your value weights ( How much you value each value for an issue)

    - Your reservation value ( The minimum utility you are willing to accept)

    - The offers youve recently recieved

    - The offers youve recently sent

    - The time remaining in the negotiation

    Consider the above information and make a new offer.
    
    Also as your opponent makes offers, try to understand their preferences and make offers that are favorable to both parties.  So you can offer offers that are the same to you but is more valuable to your opponent. Leading to a more efficient negotiation.
    
    As time decreases, or as your opponent concedes yous should also offer offers that are favorable to both parties slightly more.
    To do this change your offers as time goes on. Select your second or third choices for issues you care less about as time goes on.
    
    As time gets close to the deadline, make even larger concessions.

    Your offer should be in the following format, Where each issue should have a valid accompanying value. Where the reasoning is a short explanation of why you made this offer.
    
    In your reasoning, explain why you made the offer you did. If you made a concession, explain how:

    - What was the best value for this issue and what did choose as a concession and why ? 

    - Go into detail issue by issue. 

    Slowly concede as time goes on. Dont stay still. 

    Dont EVER remake the same offer.

    {offer_schema}
        
    Context: 

    Issue weights:
    {issue_weights}

    Value weights:
    {value_weights}

    Reservation value:
    {reservation_value}

    Recieved offers:
    {recieved_offer_history}

    Sent offers:
    {sent_offer_history}

    Time remaining:
    {time}

    Your opponent is saying:
    {argument}
"""
)


