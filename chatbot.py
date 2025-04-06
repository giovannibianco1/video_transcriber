import streamlit as st
from gem import chat

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🧠 Chatbot (powered by OpenRouter)")

# Show chat history
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"][0]["text"]
    if role == "user":
        st.chat_message("user").write(content)
    else:
        st.chat_message("assistant").write(content)

# User input
if prompt := st.chat_input("Type your message here..."):
    st.chat_message("user").write(prompt)

    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": [{"type": "text", "text": prompt}]
    })

    # Get assistant response
    response = chat(st.session_state.messages)

    # Add assistant message to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": [{"type": "text", "text": response}]
    })

    st.chat_message("assistant").write(response)
