import streamlit as st

from agents.router_core import route_question

st.set_page_config(
    page_title="Multi-Agent AI Assistant",
    page_icon="🤖"
)

st.title("🤖 Multi-Agent AI Assistant")

# --------------------
# MEMORY
# --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------
# SHOW OLD CHAT
# --------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------
# NEW QUESTION
# --------------------

question = st.chat_input("Ask anything...")

if question:

    # User message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.write(question)

    # Agent response

    result = route_question(
        question,
        st.session_state.messages
    )

    agent = result["agent"]
    answer = result["answer"]

    final_response = f"""
### AGENT SELECTED: {agent}

{answer}
"""

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": final_response
        }
    )

    with st.chat_message("assistant"):
        st.markdown(final_response)