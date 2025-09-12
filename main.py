import streamlit as st
from utils import generate_questions_for_stack
from prompts import candidate_questions

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
st.title("TalentScout Hiring Assistant")


if "step" not in st.session_state:
    st.session_state.step = 0
if "candidate" not in st.session_state:
    st.session_state.candidate = {}
if "chat" not in st.session_state:
    st.session_state.chat = []
if "done" not in st.session_state:
    st.session_state.done = False


if st.session_state.step == 0 and not st.session_state.chat:
    st.session_state.chat.append(("Bot", "Hi! I'm TalentScout, your hiring assistant. I'll ask a few short questions."))
    first_q = f"{candidate_questions[0]}?"
    st.session_state.chat.append(("Bot", first_q))

for role, msg in st.session_state.chat:
    if role == "Bot":
        st.markdown(f"**{role}:** {msg}")
    else:
        st.markdown(f"**{role}:** {msg}")

if st.session_state.done:
    st.write("---")
    st.subheader("Candidate summary")
    for k, v in st.session_state.candidate.items():
        st.write(f"- **{k}:** {v}")
    st.write("Thank you — the tailored questions were generated above.")
    st.stop()

current_step = st.session_state.step
current_question = candidate_questions[current_step] + "?"

with st.form(key=f"form_{current_step}"):
    user_answer = st.text_input(label=current_question, key=f"input_{current_step}")
    submitted = st.form_submit_button("Submit")

if submitted:
    # Exit handling
    if user_answer.strip().lower() in ["exit", "bye", "quit"]:
        st.session_state.chat.append(("User", user_answer))
        st.session_state.chat.append(("Bot", "Thank you for your time. Goodbye!"))
        st.session_state.done = True
        st.rerun()
    
    st.session_state.chat.append(("User", user_answer))
    st.session_state.candidate[candidate_questions[current_step]] = user_answer.strip()
    st.session_state.step += 1

    if st.session_state.step < len(candidate_questions):
        next_q = candidate_questions[st.session_state.step] + "?"
        st.session_state.chat.append(("Bot", f"Thanks. {next_q}"))
        st.rerun()

    else:
        
        tech_key = "Tech Stack (languages, frameworks, databases, tools)"
        tech_stack = st.session_state.candidate.get(tech_key, "").strip()
        st.session_state.chat.append(("Bot", "Thanks — generating tailored technical questions now..."))
        
        with st.spinner("Generating questions (may take a moment)..."):
            if tech_stack:
                questions = generate_questions_for_stack(tech_stack)
                st.session_state.chat.append(("Bot", questions))
            else:
                st.session_state.chat.append(("Bot", "No tech stack provided. If you'd like, you can type your tech stack and click Submit."))
                
        st.session_state.chat.append(("Bot", "Conversation complete. Thank you — our team will reach out with next steps."))
        st.session_state.done = True
        st.rerun()   