import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='notepad.env')

HF_TOKEN = os.getenv('HF_TOKEN')


BASE_URL= "https://router.huggingface.co/v1/chat/completions"

headers = { "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json" }

st.set_page_config(page_title="Mu CHATBOT")
st.title("Mu CHATBOT")
st.write("Welcome! Ask me anything. Type your message below.")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    st.markdown(f"**{msg['role'].capitalize()}:** {msg['content']}")

user_input = st.text_input("You:", key="input")

if st.button("Send") and user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )


    data = {
  "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": [
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 500
    }

    resp = requests.post(BASE_URL, headers=headers, json=data)

    
    if resp.status_code == 200:
        reply = resp.json()["choices"][0]["message"]["content"]
    else:
        reply = f"Sorry, something went wrong.{resp.status_code} - {resp.text}"

    # Show bot reply
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    st.rerun()

