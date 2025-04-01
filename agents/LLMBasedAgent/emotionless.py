from typing import Optional, List, Dict, Any
import nenv
from nenv import Action, Bid, Offer
from .Generation.generation import text_based
from .Generation.pydantic_generator import generate_pydantic_class


def get_bid(recieved_offer_history: List[float], sent_offer_history: List[float], t: float, issue_weights: Dict[str, float], value_weights: Dict[str, Dict[str, float]], reservation_value: float, offer_schema, Offer, model: str,  argument: str=None) -> float:
    return text_based(recieved_offer_history, sent_offer_history, 1-t, argument=argument, issue_weights=issue_weights, value_weights=value_weights, reservation_value=reservation_value, offer_schema=offer_schema, Offer=Offer, model_type=model)

class EmotionlessLLMBasedAgent(nenv.AbstractAgent):
    """
    LLM-based negotiation agent that leverages language models for negotiation strategy.
    """
    
    offer_history: List[float]
    
    @property
    def name(self) -> str:
        return "EmotionlessLLMBasedAgent"
    
    def initiate(self, opponent_name: Optional[str], model: str = "google-gemini-2.0-flash"):
        """Initialize history tracking"""
        self.recieved_offer_history = []
        self.sent_offer_history = []
        self.model = model
        self.Offer = generate_pydantic_class(self.preference.value_weights)
        self.offer_schema = self.Offer()

    def receive_offer(self, bid: Bid, t: float):
        """Process received offer and update history"""        
        self.recieved_offer_history.append(bid.content)
        
    def act(self, t: float) -> Action:
        """Determine action based on LLM reasoning"""
        
        if len(self.recieved_offer_history) > 5:
            recieved_window = self.recieved_offer_history[-5-1:]
            sent_window = self.sent_offer_history[-4-1:]
        else:
            recieved_window = self.recieved_offer_history
            sent_window = self.sent_offer_history

        if len(self.last_received_bids) > 0:
            bid_content = get_bid(recieved_window, sent_window, t, argument=None, model=self.model, issue_weights=self.preference.issue_weights,
                                                                  value_weights=self.preference.value_weights, reservation_value=self.preference.reservation_value, offer_schema=self.offer_schema.model_dump_json(), Offer=self.Offer)
            
            print(bid_content, flush=True)
            print("", flush=True)
            print(bid_content["reasoning"], flush=True)
            print("", flush=True)
            issue_dict = {}
            for issue in self.preference.issues:
                issue_dict[issue] = bid_content[issue.name]
            
            bid = Bid(content=issue_dict)

            utility = self.preference.get_utility(bid)
            print(utility, flush=True)
            self.sent_offer_history.append(bid.content)
                        
            if self.can_accept():
                if utility <= self.last_received_bids[-1].utility:
                    print("Accepted by LLM", flush=True)
                    print("",flush=True)
                    return self.accept_action
            
            return Offer(bid)
        else:
            return Offer(self.preference.get_bid_at(1))

