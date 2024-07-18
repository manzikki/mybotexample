import streamlit as st
import openai
import os
import sys
try:
    __import__('pysqlite3') 
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except:
    pass
from main import query

openai.api_key = st.secrets["OPENAI_API_KEY"]
MODEL_ENGINE = "gpt-4o"

st.title("🤖 Chatbot App")
chat_placeholder = st.empty()


def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]


def start_chat():
    # Display chat messages from history on app rerun
    with chat_placeholder.container():
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Please ask about our organization!"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response from Chat models
        response = query(prompt)

        # message_placeholder.markdown(response)
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    init_chat_history()
    start_chat()
