from langchain_core.messages import HumanMessage
from .prompts import Offer
from langchain_anthropic import ChatAnthropic
import os

async def text_based(model_type, prompt):
    llm = ChatAnthropic(api_key=os.getenv("CLAUDE_API_KEY"), model="claude-3-5-sonnet-20241022") 
    llm = llm.with_structured_output(Offer)

    content = [
        {"type": "text", "text": prompt}
    ]

    message = HumanMessage(content=content)
    response: Offer = await llm.ainvoke([message])
    return response


# async def image_based(text, gesture, model_type, prompt):
#     llm = ChatAnthropic(api_key=os.getenv("CLAUDE_API_KEY"), model="claude-3-5-sonnet-20241022") 
#     llm = llm.with_structured_output(Emotion)

#     frames = extract_frames(gesture)

#     formatted_prompt = prompt.format(text=text)

#     content = []

#     for p in frames:
#         content.append({
#             "type": "image",
#             "source": {
#                 "type": "base64",
#                 "media_type": "image/jpeg", 
#                 "data": p[0]
#             }
#         })

#     content.append(HumanMessage(content=formatted_prompt))

#     message = HumanMessage(content=content)
#     response: Emotion = await llm.ainvoke([message])
#     return response
    
