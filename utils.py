from transformers import pipeline
from prompts import question_gen_prompt

try:
    import torch
    if torch.cuda.is_available():
        device = 0  
    else:
        device = -1  
except Exception:
    device = -1


generator = pipeline('text2text-generation', model='google/flan-t5-base')

def generate_questions_for_stack( tech_stack: str) -> str:
        """
        Use the instruction prompt from prompts.py to generate interview questions.
        Returns a cleaned string.
        """
        prompt = question_gen_prompt.format(tech_stack = tech_stack)
    
        final_prompt = (
            "You are TalentScout, an AI hiring assistant.\n"
            "Respond ONLY with the requested interview questions.\n\n"
            f"{prompt}\n\n"
            "Output format example:\n"
            "Python:\n1. ...\n2. ...\n\nSQL:\n1. ...\n2. ...\n"
        )
        result = generator(final_prompt, max_length=200, num_return_sequences=1)
        text = result[0]['generated_text'].strip()
        return text