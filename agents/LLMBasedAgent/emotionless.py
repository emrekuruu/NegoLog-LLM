from typing import Optional, List, Dict, Any
import nenv
from nenv import Action, Bid, Offer
from .Generation.generation import text_based
import asyncio
import logging

def calculate_target_utility(recieved_offer_history: List[float], sent_offer_history: List[float], t: float, model: str,  argument: str=None) -> float:
    return text_based(recieved_offer_history, sent_offer_history, t, argument=argument, model_type=model)

class EmotionlessLLMBasedAgent(nenv.AbstractAgent):
    """
    LLM-based negotiation agent that leverages language models for negotiation strategy.
    """
    
    offer_history: List[float]
    
    @property
    def name(self) -> str:
        return "EmotionlessLLMBasedAgent"
    
    def initiate(self, opponent_name: Optional[str], model: str = "openai-gpt-4o"):
        """Initialize history tracking"""
        self.recieved_offer_history = []
        self.sent_offer_history = []
        self.model = model

    def receive_offer(self, bid: Bid, t: float):
        """Process received offer and update history"""        
        self.recieved_offer_history.append(bid.utility)
        print(bid.argument, flush=True)
        
    def act(self, t: float) -> Action:
        """Determine action based on LLM reasoning"""
        
        if len(self.recieved_offer_history) > 5:
            recieved_window = self.recieved_offer_history[-5-1:]
            sent_window = self.sent_offer_history[-4-1:]
        else:
            recieved_window = self.recieved_offer_history
            sent_window = self.sent_offer_history
                        
        if self.can_accept():

            target_utility, reasoning = calculate_target_utility(recieved_window, sent_window, t, model=self.model)

            bid = self.preference.get_bid_at(target_utility)

            if bid <= self.last_received_bids[-1]:
                return self.accept_action
        
            self.sent_offer_history.append(bid.utility)
            print(reasoning, flush=True)
            return Offer(bid)
        


