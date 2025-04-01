from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os 

def text_based(model_type, prompt, Offer):
    llm = ChatGoogleGenerativeAI(model=model_type, api_key=os.getenv("GOOGLE_API_KEY"))  
    llm = llm.with_structured_output(Offer)

    content = [
        {"type": "text", "text": prompt}
    ]

    message = HumanMessage(content=content)
    response: Offer = llm.invoke([message])
    return response
