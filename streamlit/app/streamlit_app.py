''' Streamlit app for chatbot
streamlit run /workspaces/b3rn_zero_copilot/streamlit/app/streamlit_app.py --server.port 8502 --browser.gatherUsageStats false
 '''
import os
from openai import OpenAI
import streamlit as st
from streamlit_searchbox import st_searchbox
import streamlit as st
import time
import requests

def search_function(topic):
    """ Wrapper-Funktion für get_suggestions, die die erforderlichen Parameter übergibt. """
    if topic:
        #response = requests.get(f'http://fastapi:80/suggest/{topic}')
        response = requests.get(f'http://localhost:80/suggest/{topic}')
        if response.status_code == 200:
            suggestions = response.json()
            return suggestions
        else:
            time.sleep(1)
        return suggestions

with st.sidebar:
    if not 'OPENAI_API_KEY' in os.environ:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    else:
        openai_api_key = os.environ['OPENAI_API_KEY']
    
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/tabee/b3rn_zero_copilot)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tabee/b3rn_zero_copilot?quickstart=1)"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if len(st.session_state.messages) == 0:
    prompt1 = st_searchbox(search_function, key="box_to_search", clear_on_submit=False, placeholder="Ask me anything ...")
    def start_chat():
        st.session_state.chatmode = True
        st.write("Chat started")
        st.rerun()
    if prompt1:
        st.session_state.messages.append({"role": "user", "content": prompt1})
        st.session_state.messages.append({"role": "assistant", "content": f"fake answert to your {prompt1}"})
        st.rerun()

else:
    if prompt := st.chat_input():
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        response = "answer to your question " + prompt
        st.session_state.messages.append({"role": "assistant", "content": response})

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
