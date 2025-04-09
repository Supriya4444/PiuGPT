import os
import json
import streamlit as st
from groq import Groq

# Configuring API key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
GROQ_API_KEY = config_data["LLAMA_API_KEY"]  # Assuming LLAMA_API_KEY is the correct key for Groq
client = Groq(api_key=GROQ_API_KEY)

# Configuring Streamlit page settings
st.set_page_config(
    page_title="LLaMA ChatBot",
    page_icon="🤖",
    layout="centered"
)

# Initialize retained chat session in Streamlit
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Streamlit page title
st.title("🤖 MyGPT - Any Query, Any Time!")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Ask me anything 👩🏻‍💻...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Call Groq LLaMA 3.3 model
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            *st.session_state.chat_history
        ]
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
