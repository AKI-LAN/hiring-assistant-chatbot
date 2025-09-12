from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

MODEL_NAME ="unsloth/llama-3-8b-instruct"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
    )

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=256,
    temperature=0.7,
    top_p=0.9,
)

def generate_questions_for_stack(tech_stack: str):

    techs = [t.strip() for t in tech_stack.split(",") if t.strip()]
    questions = []

    for tech in techs:
        prompt =  f"""
You are a senior technical interviewer.
Generate 3 challenging, practical interview questions for a candidate skilled in {tech}.
- Ask about coding, system design, debugging, optimization, or real-world usage.
- Be specific and technical.
- Number the questions 1, 2, 3.
Only output the questions.

Examples:
Python:
1. How does Python's Global Interpreter Lock (GIL) affect multithreading performance?
2. Write a Python function to reverse a linked list.
3. Explain Python's garbage collection mechanism and how it manages memory.

Now generate 3 interview questions for {tech}:
"""
        result = pipe(prompt)[0]["generated_text"]
        seen = set()
        for line in result.split("\n"):
            line = line.strip()
            if line and line[0] in "123" and line[1] == ".":
                q = line[2:].strip()
                if q not in seen:
                    questions.append(f"{tech}: {q}")
                    seen.add(q)


    return questions
