from typing import Optional, List, Dict, Any
import nenv
from nenv import Action, Bid, Offer
from .Generation.generation import text_based
import asyncio

def calculate_target_utility(offer_history: List[float], t: float, model: str,  argument: str=None) -> float:
    try:
        return asyncio.run(text_based(offer_history, 1-t, argument=argument, model_type=model))
    except Exception as e:
        pass
class EmotionalLLMBasedAgent(nenv.AbstractAgent):
    """
    LLM-based negotiation agent that leverages language models for negotiation strategy.
    """
    
    offer_history: List[float]
    
    @property
    def name(self) -> str:
        return "EmotionalLLMBasedAgent"
    
    def initiate(self, opponent_name: Optional[str], model: str = "openai-gpt-4o"):
        """Initialize history tracking"""
        self.offer_history = []
        self.model = model
    
    def receive_offer(self, bid: Bid, t: float):
        """Process received offer and update history"""        
        self.offer_history.append(bid.utility)
        
    def act(self, t: float) -> Action:
        """Determine action based on LLM reasoning"""
        
        target_utility = calculate_target_utility(self.offer_history[-5-1], t, argument=bid.argument, model=self.model)

        bid = self.preference.get_bid_at(target_utility)

        if self.can_accept() and bid <= self.last_received_bids[-1]:
            return self.accept_action
        
        return Offer(bid)


