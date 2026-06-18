import streamlit as st

from agents.router_core import route_question

from memory_manager import (
    load_messages,
    save_message
)

st.set_page_config(
    page_title="Multi-Agent AI Assistant",
    page_icon="🤖"
)

st.title("🤖 Multi-Agent AI Assistant")

# ====================
# USER LOGIN
# ====================

username = st.sidebar.text_input(
    "Username",
    value="guest"
)

st.sidebar.success(
    f"Logged in as: {username}"
)

# ====================
# LOAD USER HISTORY
# ====================

messages = load_messages(username)

# ====================
# SHOW OLD CHAT
# ====================

for message in messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

# ====================
# NEW QUESTION
# ====================

question = st.chat_input(
    "Ask anything..."
)

if question:

    # Save user message

    save_message(
        username,
        "user",
        question
    )

    # Show user message

    with st.chat_message("user"):
        st.write(question)

    # Reload memory

    messages = load_messages(username)

    # Ask router

    result = route_question(
        question,
        messages
    )

    # Extract answer

    if isinstance(result, dict):

        agent = result["agent"]
        answer = result["answer"]

        final_response = f"""
AGENT SELECTED: {agent}

{answer}
"""

    else:

        final_response = str(result)

    # Save assistant response

    save_message(
        username,
        "assistant",
        final_response
    )

    # Show assistant response

    with st.chat_message("assistant"):
        st.write(final_response)

    # Refresh

    st.rerun()