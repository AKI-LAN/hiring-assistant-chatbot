import os 
from openai import OpenAI
from dotenv import load_dotenv
from prompts import question_gen_prompt

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_llm_response(user_input, tech_stack=None):
    """Send user input to LLM and return chatbot response"""
    messages = [{"role":"system","content":"You are a hiring assitant chatbot."},{"role":"user","content": user_input}]


    if tech_stack:
        messages.append({
            "role":"user",
            "content": question_gen_prompt.format(tech_stack=tech_stack)
        })

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages
    )

    return response.choices[0].message.content