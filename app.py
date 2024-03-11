import openai
import streamlit as st
import os
from openai import OpenAI

st.title("Chatgiller")
openai.api_key = st.secrets["OPENAI_API_KEY"] # you should paste your api key on secrets.toml file in .streamlit folder

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

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
        message_placeholder = st.empty()
        full_response = ""
        
        client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        )

        for response in client.chat.completions.create(
            model=st.session_state["openai_model"], 
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages],
                stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + " > _____")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

