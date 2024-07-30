from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

st.title("Gemini-like clone")
key = "Your API Key is Here "
client = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, google_api_key=key)


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
        stream = client.stream(st.session_state.messages[-1]["content"])

        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})