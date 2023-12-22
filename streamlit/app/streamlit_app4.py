''' Streamlit app for chatbot
streamlit run /workspaces/b3rn_zero_copilot/streamlit/app/streamlit_app4.py --server.port 8502 --browser.gatherUsageStats false
 '''
import os
from openai import OpenAI
import streamlit as st
from streamlit_searchbox import st_searchbox
import streamlit as st
import time

def search_function(topic):
    if topic:
        return ["question 1", "question 2", "question 3"]

with st.sidebar:
    
    if not 'OPENAI_API_KEY' in os.environ:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    else:
        openai_api_key = os.environ['OPENAI_API_KEY']
    
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]



with st.empty():
    if (len(st.session_state.messages) <= 2):
        selected_value = st_searchbox(search_function, key="faq_searchbox", clear_on_submit=True, placeholder="Message to ResearchCopilot...")


        if selected_value:

            st.session_state.messages.append({"role": "user", "content": selected_value})
            st.session_state.messages.append({"role": "assistant", "content": "fake answert"})

            st.empty()
        
            selected_value = st.empty()





if (len(st.session_state.messages) <= 2):
    
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


if (len(st.session_state.messages) > 2):
    if prompt := st.chat_input():
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        response = "answer to your question " + prompt
        st.session_state.messages.append({"role": "assistant", "content": response})

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])