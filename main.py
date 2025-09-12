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
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = {}


if st.session_state.step == 0 and not st.session_state.chat:
    st.session_state.chat.append(("Bot", "Hi! I'm TalentScout, your hiring assistant. I'll ask a few short questions."))
    first_q = f"{candidate_questions[0]}?"
    st.session_state.chat.append(("Bot", first_q))

for role, msg in st.session_state.chat:
    st.markdown(f"**{role}:** {msg}")

if not st.session_state.done and isinstance(st.session_state.step, int):
    current_step = st.session_state.step
    if current_step < len(candidate_questions):
        current_question = candidate_questions[current_step] + "?"

        with st.form(key=f"form_{current_step}"):
            user_answer = st.text_input(label=current_question, key=f"input_{current_step}")
            submitted = st.form_submit_button("Submit")

        if submitted:
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
                        st.session_state.questions = generate_questions_for_stack(tech_stack)
                        if st.session_state.questions:
                            st.session_state.chat.append(("Bot", "Great, now let’s go through these questions one by one."))
                            st.session_state.step = "evaluation"
                        else:
                            st.session_state.chat.append(("Bot", "Sorry, I couldn't generate questions."))
                            st.session_state.done = True
                    else:
                        st.session_state.chat.append(("Bot", "No tech stack provided, so no questions can be generated."))
                        st.session_state.done = True

                st.rerun()
# --- Evaluation Phase ---
if st.session_state.step == "evaluation" and st.session_state.questions:
    total_qs = len(st.session_state.questions)
    answered = len(st.session_state.answers)

    if answered < total_qs:
        current_q = st.session_state.questions[answered]
        st.markdown(f"**Bot:** {current_q}")

        with st.form(key=f"eval_{answered}"):
            user_ans = st.text_area("Your Answer", key=f"ans_{answered}")
            submit_eval = st.form_submit_button("Submit Answer")

        if submit_eval and user_ans.strip():
            # Save this answer
            st.session_state.answers[current_q] = user_ans.strip()
            st.session_state.chat.append(("User", user_ans.strip()))
            st.rerun()
    else:
        # All questions answered
        st.subheader("✅ Evaluation Complete")
        st.write("Here is a summary of your answers:")

        for q, ans in st.session_state.answers.items():
            st.write(f"**Q:** {q}")
            st.write(f"**Your Answer:** {ans}")
            st.write("---")

        st.session_state.done = True