from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from .prompts import Offer, exponential_retry
from langchain_community.callbacks import get_openai_callback
import os 

@exponential_retry(max_retries=3, base_delay=1, jitter=0.1)
def text_based(model_type, prompt):
    llm = ChatGoogleGenerativeAI(model=model_type, api_key=os.getenv("GOOGLE_API_KEY"))  
    llm = llm.with_structured_output(Offer)

    content = [
        {"type": "text", "text": prompt}
    ]

    message = HumanMessage(content=content)
    response: Offer = llm.invoke([message])
    return response

# @exponential_retry(max_retries=3, base_delay=1, jitter=0.1)
# async def image_based(text, gesture, model_type, prompt):
#     llm = ChatGoogleGenerativeAI(model=model_type, api_key=os.getenv("GOOGLE_API_KEY"))  
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

#     with get_openai_callback() as cb:
#         response: Emotion = await llm.ainvoke([message])
#         print(f"Total Tokens: {cb.total_tokens}")

#     return response

