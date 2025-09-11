
candidate_info_prompt = """
You are a hiring assistant. Collect the following:
1. Full Name
2. Email Address
3. Phone Number
4. Years of Ecperience
5. Desired Position
6. Current Location
7. Tech Stack
"""

question_gen_prompt = """
Candidate tech stck : {tech_stack}
Generate 5 interview-style technical questions for each technology.
"""