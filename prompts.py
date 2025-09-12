
candidate_questions = [
    "Full Name",
    "Email Address",
    "Phone Number",
    "Years of Experience",
    "Desired Position",
    "Current Location",
    "Tech Stack (languages, frameworks, databases, tools)"
]
question_gen_prompt = """
Candidate tech stck : {tech_stack}.
You are an interviewer. For each technology listed, generate 3 interview-style technical questions.
Return a clear numbered list grouped by technology. Keep questions concise and practical.
"""