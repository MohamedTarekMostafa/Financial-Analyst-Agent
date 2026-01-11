import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
import requests  
from dotenv import load_dotenv

load_dotenv(".env")

API_URL = "http://backend:8000/ask" 

def clean_message_content(content):
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get('type') == 'text':
                return item.get('text')
        return str(content)
    return content

st.set_page_config(page_title="AI Financial Analyst", page_icon="📈")

st.title(" AI Financial Analyst Agent")
st.markdown("""
This agent communicates with the **FastAPI Backend** .
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

if prompt := st.chat_input("Ex: Why is NVIDIA stock up today?"):
    
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Connecting to Backend API..."):
            try:
                payload = {"question": prompt}
                messages = requests.post(API_URL, json=payload)
                
                if messages.status_code == 200:
                    data = messages.json()
                    final_text = data.get("messages", "No response field found")
                    
                    st.markdown(final_text)
                    st.session_state.messages.append(AIMessage(content=final_text))
                else:
                    st.error(f"API Error: {messages.status_code}")
                
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()