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
        Generate 3 questions for each technology in the stack, one by one.
        """
        techs = [t.strip() for t in tech_stack.split(",") if t.strip()]
        output = []
        for tech in techs:
            prompt = (
            f"You are TalentScout, an AI Hiring Assistant.\n"
            f"Generate exactly 3 interview-style technical questions for {tech}.\n"
            "Return only the questions, numbered 1 to 3.\n"
            )
       
            result = generator(prompt, max_length=200, num_return_sequences=1)
            return result[0]["generated_text"].strip()
            
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            cleaned = "\n".join(lines[:3])
            output.append(f"### {tech}\n{cleaned}")
        
        return "\n\n".join(output)