from transformers import pipeline
from prompts import question_gen_prompt

generator = pipeline('text2text-generation', model='google/flan-t5-base')

def get_llm_response(user_input, tech_stack=None):
    """
    Generate a chatbot-like response using Hugging Face DistilGPT-2 model.
    If tech_stack is provided, include it in the prompt for generating technical questions.
    """
    prompt = user_input

    if tech_stack:
        prompt += "\n" + question_gen_prompt.format(tech_stack=tech_stack)

    response = generator(prompt, max_length=150, num_return_sequences=1)

    return response[0]['generated_text']