import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

def text_based(model_type, prompt, Offer):
    llm = ChatOpenAI(model=model_type, api_key=os.getenv("OPENAI_API_KEY"), temperature=0.4) 
    llm = llm.with_structured_output(Offer)
    
    content = [
        {"type": "text", "text": prompt}
    ]

    message = HumanMessage(content=content)
    response: Offer = llm.invoke([message])
    return response



