''' Streamlit app for chatbot
streamlit run /workspaces/b3rn_zero_copilot/streamlit/app/streamlit_app3.py --server.port 8502 --browser.gatherUsageStats false
 '''
import os
from openai import OpenAI
import streamlit as st
from streamlit_searchbox import st_searchbox

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

    if 'suggest_question' not in st.session_state:
        st.session_state['suggest_question'] = True

    suggest_question = st.toggle('Activate feature', value=st.session_state['suggest_question'], key='suggest_question')



st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

print(f"st.session_state.messages: {len(st.session_state.messages)}\n")

if st.session_state['suggest_question'] == False :
    # suggest questions
    if prompt := st.chat_input() and st.session_state['suggest_question'] == False :
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        client = OpenAI(api_key=openai_api_key)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        print(f"st.session_state.messages: {st.session_state.messages}\n")
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
        st.session_state['suggest_question'] = True

else:
    selected_value = st_searchbox(search_function, key="faq_searchbox", clear_on_submit=True, placeholder="Message to ResearchCopilot...")

    if selected_value:
        st.session_state.messages.append({"role": "user", "content": selected_value})
        st.chat_message("user").write(selected_value)
        answer = "This is the answer to your question."
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.chat_message("assistant").write(answer)




