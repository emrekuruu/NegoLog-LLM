from typing import Optional, List, Dict, Any
import nenv
from nenv import Action, Bid, Offer

def acceptance_strategy(bid: Bid, offer_history: List[Dict[str, Any]], t: float) -> bool:
    pass

def bidding_strategy(bid: Bid, offer_history: List[Dict[str, Any]], t: float) -> Bid:
    pass


class LLMBasedAgent(nenv.AbstractAgent):
    """
    LLM-based negotiation agent that leverages language models for negotiation strategy.
    
    This agent delegates all decision-making to an external LLM:
    1. Bidding strategy (what to offer)
    2. Acceptance strategy (when to accept)
    
    The agent only tracks the history of offers, providing the necessary context for the LLM to make decisions.
    """
    
    # Track offer history
    offer_history: List[Dict[str, Any]]
    
    @property
    def name(self) -> str:
        return "LLMBasedAgent"
    
    def initiate(self, opponent_name: Optional[str]):
        """Initialize history tracking"""
        self.offer_history = []
    
    def receive_offer(self, bid: Bid, t: float):
        """Process received offer and update history"""
        # Add received bid to offer history
        offer_info = {
            "role": "opponent",
            "bid": bid,
            "utility": bid.utility,
            "time": t
        }
        self.offer_history.append(offer_info)
        print("Recieved argument: ", bid.argument)
        
    def act(self, t: float) -> Action:
        """Determine action based on LLM reasoning"""
        
        if self.can_accept():
            last_bid = self.last_received_bids[-1]
            
            # TODO: Placeholder for LLM to determine if we should accept
            should_accept = (last_bid.utility >= self.preference.reservation_value + 0.1)
            
            if should_accept:
                action_info = {
                    "role": "agent",
                    "action": "accept",
                    "bid": last_bid,
                    "utility": last_bid.utility,
                    "time": t
                }
                self.offer_history.append(action_info)
                return self.accept_action
        
        # TODO: Placeholder for LLM to determine what bid to offer
        bid = self.preference.get_random_bid()
        
        action_info = {
            "role": "agent",
            "action": "offer",
            "bid": bid,
            "utility": bid.utility,
            "time": t
        }
        self.offer_history.append(action_info)
        
        return Offer(bid)

