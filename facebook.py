import requests
import streamlit as st
st.title("Facebook Blenderbot")

def client(payload):
    headers = {"Authorization": f"Bearer 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"}
    API_URL = f"https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        data = client(prompt)[0]["generated_text"]
        st.write(data)
    st.session_state.messages.append({"role": "assistant", "content": data})