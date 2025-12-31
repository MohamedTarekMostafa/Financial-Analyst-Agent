import streamlit as st
from agent import create_agent
from langchain_core.messages import HumanMessage, AIMessage
from langfuse.langchain import CallbackHandler
from dotenv import load_dotenv
import os

load_dotenv()

def clean_message_content(content):
    if isinstance(content, list):
        for item in content:
            if isinstance(item, dict) and item.get('type') == 'text':
                return item.get('text')
        return str(content)
    return content

st.set_page_config(page_title="AI Financial Analyst", page_icon="📈")

st.title("📈 AI Financial Analyst Agent")
st.markdown("""
This intelligent agent analyzes stock market data and searches global news using **LangGraph** and **Tavily**.  
Performance and costs are monitored via **Langfuse**.
""")

if "agent" not in st.session_state:
    st.session_state.agent = create_agent()
    if "messages" not in st.session_state:
        st.session_state.messages = []

for msg in st.session_state.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

if prompt := st.chat_input("Ex: Why is Tesla stock down today?"):
    
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing markets and searching news..."):
            try:
                langfuse_handler = CallbackHandler()

                config = {
                    "configurable": {"thread_id": "st_session_v1"},
                    "callbacks": [langfuse_handler],
                    "run_name": "Financial_Query_Execution"
                }

                input_data = {"messages": st.session_state.messages}
                response = st.session_state.agent.invoke(input_data, config)
                
                raw_response = response["messages"][-1].content
                final_text = clean_message_content(raw_response)
                
                st.markdown(final_text)
                st.session_state.messages.append(AIMessage(content=final_text))
                
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")

if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()