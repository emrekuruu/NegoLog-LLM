import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from .prompts import Offer

async def text_based(model_type, prompt):
    llm = ChatOpenAI(model=model_type, api_key=os.getenv("OPENAI_API_KEY")) 
    llm = llm.with_structured_output(Offer)
    
    content = [
        {"type": "text", "text": prompt}
    ]

    message = HumanMessage(content=content)
    response: Offer = await llm.ainvoke([message])
    return response

# async def image_based(text, gesture, model_type, prompt):
#     llm = ChatOpenAI(model=model_type, api_key=os.getenv("OPENAI_API_KEY")) 
#     llm = llm.with_structured_output(Emotion)

#     formatted_prompt = prompt.format(text=text)

#     content = []

#     frames = extract_frames(gesture)

#     for p in frames:
#         content.append({
#             "type": "image_url",
#             "image_url": {"url": f"data:image/jpeg;base64,{p}"}
#         })

#     content.append({"type": "text", "text": formatted_prompt})  

#     message = HumanMessage(content=content)
#     response: Emotion = await llm.ainvoke([message])
#     return response

