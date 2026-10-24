
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

st.set_page_config(
    page_title="Ragesh Chatbot",
    page_icon="💜",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #240046, #5a189a, #7b2cbf);
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #18002e;
}
.stChatMessage {
    background-color: rgba(255,255,255,0.08);
    border-radius: 12px;
}
h1, p, label {
    color: white;
}
.stChatInput textarea {
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("💜 Ragesh Chatbot")
st.caption("Powered by Groq • Qwen 3.8 27B")

with st.sidebar:
    st.header("⚙️ Settings")

    temperature = st.slider(
        "Temperature", 0.0, 2.0, 0.7, 0.1
    )
    max_tokens = st.slider(
        "Max Tokens", 128, 8192, 1024, 128
    )
    top_k = st.slider(
        "Top K", 1, 100, 20
    )
    top_p = st.slider(
        "Top P", 0.0, 1.0, 0.8, 0.05
    )

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is missing. Add it to your .env file.")
    st.stop()

client = Groq(api_key=api_key)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Message Ragesh Chatbot...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="qwen/qwen3.8-27b",
                    messages=st.session_state.messages,
                    temperature=temperature,
                    max_completion_tokens=max_tokens,
                    top_p=top_p,
                    reasoning_effort="none"
                )

                answer = response.choices[0].message.content
                st.markdown(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })

        except Exception as e:
            st.error(f"Groq API Error: {e}")
