''' Streamlit app for chatbot
streamlit run /workspaces/b3rn_zero_copilot/streamlit/app/streamlit_app2.py --server.port 8502 --browser.gatherUsageStats false
 '''
import os
from openai import OpenAI
import streamlit as st
from streamlit_searchbox import st_searchbox
import streamlit as st
import time
import asyncio
import httpx
import requests
from urllib.parse import quote
from starlette.responses import StreamingResponse
import grpc
import service_pb2
import service_pb2_grpc


# dirty hack to switch between local and docker container, depending on the environment sys_path
sys_path = os.getenv('DATA_PATH', default=os.path.join(os.path.dirname(__file__)))
server_name = "fastapi"
if str(sys_path).startswith('/workspaces'):
    server_name = "127.0.0.1"
    #print(f"workspaces ... set server_name to {server_name}")
# end dirty hack

def search_function(topic):
    """ Wrapper-Funktion für get_suggestions, die die erforderlichen Parameter übergibt. """
    if topic:
        response = requests.get(f'http://{server_name}:80/suggest/{topic}')
        if response.status_code == 200:
            suggestions = response.json()
            return suggestions
        else:
            time.sleep(1)
        return suggestions

def get_answer(question):
    """ Wrapper-Funktion für get_suggestions, die die erforderlichen Parameter übergibt. """
    if question:
        encoded_question = quote(question) # Kodieren des Strings für die URL
        response = requests.get(f'http://{server_name}:80/sqlite/answer/{encoded_question}')

        if response.status_code == 200:
            suggestions = response.json()
            return suggestions
        else:
            return "Sorry, I don't know the answer to your question."

def is_complete_response(buffer):
    """Determine if the buffer contains a complete response."""
    return buffer.endswith('.') or buffer.endswith('\n') or buffer.endswith(',') or buffer.endswith('?')

async def call_agent_for_grpc(parameter: str):
    '''Call the gRPC agent service with the given parameter and stream the response.'''
    async with grpc.aio.insecure_channel('0.0.0.0:50051') as channel:
        stub = service_pb2_grpc.PromptServiceStub(channel)
        buffer = ""

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            async for response in stub.GetResponseStream(service_pb2.PromptRequest(prompt=parameter)):
                buffer += response.answer
                if is_complete_response(buffer):  # Define a function to determine completeness of the response
                    full_response += buffer
                    message_placeholder.markdown(full_response)  # Update Streamlit placeholder with the complete response
                    buffer = ""  # Reset the buffer after updating

            return full_response



with st.sidebar:
    if not 'OPENAI_API_KEY' in os.environ:
        openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    else:
        openai_api_key = os.environ['OPENAI_API_KEY']
    "[View the source code](https://github.com/tabee/b3rn_zero_copilot)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tabee/b3rn_zero_copilot?quickstart=1)"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

# f.a.q. mode
if len(st.session_state.messages) == 0:
    prompt1 = st_searchbox(search_function, key="box_to_search", clear_on_submit=False, placeholder="Ask me anything ...")
    if prompt1:
        st.session_state.messages.append({"role": "user", "content": prompt1})
        answer = get_answer(prompt1)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
# chat mode
else:
    if prompt := st.chat_input():
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        final_answer = asyncio.run(call_agent_for_grpc(parameter=prompt))
        #Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": final_answer})
    
        st.rerun()


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])
