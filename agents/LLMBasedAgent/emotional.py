from typing import Optional, List, Dict, Any
import nenv
from nenv import Action, Bid, Offer
from .Generation.generation import text_based

def calculate_target_utility(recieved_offer_history: List[float], sent_offer_history: List[float], t: float, model: str,  argument: str=None) -> float:
    return text_based(recieved_offer_history, sent_offer_history, 1-t, argument=argument, model_type=model)

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
        self.recieved_offer_history = []
        self.sent_offer_history = []
        self.model = model

    def receive_offer(self, bid: Bid, t: float):
        """Process received offer and update history"""        
        self.recieved_offer_history.append(bid.utility)
        print(" ", flush=True)
        print(bid.argument, flush=True)
        print("", flush=True)
        
    def act(self, t: float) -> Action:
        """Determine action based on LLM reasoning"""
        
        if len(self.recieved_offer_history) > 5:
            recieved_window = self.recieved_offer_history[-5-1:]
            sent_window = self.sent_offer_history[-4-1:]
        else:
            recieved_window = self.recieved_offer_history
            sent_window = self.sent_offer_history

        if len(self.last_received_bids) > 0:
            target_utility, reasoning = calculate_target_utility(recieved_window, sent_window, t, argument=self.last_received_bids[-1].argument, model=self.model)
            bid = self.preference.get_bid_at(target_utility)
            self.sent_offer_history.append(bid.utility)
                        
            if self.can_accept():
                if target_utility <= self.last_received_bids[-1].utility:
                    print("Accepted by LLM", flush=True)
                    print("",flush=True)
                    return self.accept_action
            
            print("", flush=True)
            print(reasoning, flush=True)
            print("", flush=True)
            return Offer(bid)
        else:
            return Offer(self.preference.get_bid_at(1))

