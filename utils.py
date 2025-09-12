from transformers import pipeline
from prompts import question_gen_prompt

generator = pipeline('text2text-generation', model='google/flan-t5-base')

def get_llm_response(user_input, tech_stack=None):
    """
    Generate a chatbot response using Hugging Face Flan-T5 model.
    If tech_stack is provided, include it in the prompt for generating technical questions.
    """
    base_instructions = "You are TalentScout, a hiring assistant. Respond politely, ask questions step by step, and gather candidate information.keep answer short"

    if tech_stack:
        prompt =  question_gen_prompt.format(tech_stack=tech_stack)
    else:
        prompt = f"{base_instructions}\nCandidate said: {user_input}\nYour response:"

    response = generator(prompt, max_length=200, num_return_sequences=1)

    return response[0]['generated_text']