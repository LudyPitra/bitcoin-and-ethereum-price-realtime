import streamlit as st
from ia import create_response

#1. Starting history
#2. Show Message History
#3. Text Box to Write Messages
#4. When users send messages, call the AI
#5. Show de Message and Save in the History

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Write your question here...")

if user_input:
    st.session_state.chat_history.append({"role":"user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Searching..."):
        response = create_response(user_input)

    st.session_state.chat_history.append({"role":"assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)