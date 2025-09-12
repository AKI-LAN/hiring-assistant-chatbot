from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

def generate_questions_for_stack(tech_stack: str):
    if not tech_stack:
        return []

    techs = [t.strip() for t in tech_stack.split(",") if t.strip()]
    questions = []

    for tech in techs:
        prompt = f"""
You are a senior technical interviewer for a software engineering candidate.

Generate 3 detailed, practical technical interview questions for {tech}. 
- Include coding, data structures, framework usage, tools, or real-world scenarios.
- Number the questions 1, 2, 3.
- Only output questions. Do not output instructions or placeholder text.
- Example for {tech}:
1. Explain a real-world use case of {tech} and write a small code snippet or query if applicable.
2. Describe a common challenge when using {tech} and how to solve it.
3. Give a technical problem that tests the candidate's understanding of {tech}.

Now generate 3 interview questions specifically for {tech}:
"""
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=250)
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Split by numbers or lines
        for line in text.split("\n"):
            line = line.strip()
            if line and any(char.isalnum() for char in line):
                questions.append(f"{tech}: {line}")

    return questions
