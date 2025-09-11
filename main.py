import streamlit as st
from utils import get_llm_response
from prompts import candidate_info_prompt, question_gen_prompt

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
st.title("TalentScout Hiring Assistant")

if "chat" not in st.session_state:
    st.session_state.chat = []
if "candidate" not in st.session_state:
    st.session_state.candidate = {}

user_input = st.text_input("You: ", key="user_input")

if st.button("Send") and user_input:

    st.session_state.chat.append(("User", user_input))

    response = get_llm_response(user_input)
    st.session_state.chat.append(("Bot",response))

for role, msg in st.session_state.chat:
    st.markdown(f"**{role}:**{msg}")