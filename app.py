import streamlit as st

from agents.router_core import route_question

st.set_page_config(
    page_title="Multi-Agent AI Assistant",
    page_icon="🤖"
)

st.title("🤖 Multi-Agent AI Assistant")

question = st.chat_input(
    "Ask anything..."
)

if question:

    st.chat_message("user").write(question)

    answer = route_question(question)

    st.chat_message("assistant").write(answer)