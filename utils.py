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

def generate_questions_for_stack( tech_stack: str) -> list[str]:

        """
        Generate 3 questions for each technology in the stack, one by one.
        Returns a list of individual questions.
        """
        techs = [t.strip() for t in tech_stack.split(",") ]
        output = []
        for tech in techs:
            prompt = (
            f"You are TalentScout, an AI Hiring Assistant.\n"
            f"Generate exactly 3 interview-style technical questions for {tech}.\n"
            "Return only the questions, numbered 1 to 3."
            )
       
            result = generator(prompt, max_length=200, num_return_sequences=1)
            text = result[0]["generated_text"].strip()
            
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            numbered = [line for line in lines if line[0].isdigit()]
            cleaned = numbered[:3]
            
            for q in cleaned:
                output.append(f"{tech}: {q}")
        
        return output