import streamlit as st
import time
import pandas as pd
import numpy as np
import requests
import streamlit as st
from streamlit_searchbox import st_searchbox



def search_function(topic):
    """ Wrapper-Funktion für get_suggestions, die die erforderlichen Parameter übergibt. """
    

    if topic:
        #response = requests.get(f'http://fastapi:80/suggest/{topic}')
        response = requests.get(f'http://localhost:80/suggest/{topic}')
        if response.status_code == 200:
            suggestions = response.json()
            for suggestion in suggestions:
                st.write(suggestion)
        else:
            time.sleep(2)

        return suggestions

selected_value = st_searchbox(search_function, key="faq_searchbox", clear_on_submit=True, placeholder="Message to ResearchCopilot...")

if selected_value:
    st.chat_message("user").write(selected_value)
    answer = "This is the answer to your question."
    st.chat_message("🔗").write(answer)

















# st.write(st.session_state)

# # With magic:
# st.session_state

# def proc():
#     topic = st.session_state.text_key
#     if topic:
#         response = requests.get(f'http://127.0.0.1:80/suggest/{topic}')
#         if response.status_code == 200:
#             suggestions = response.json()
#             for suggestion in suggestions:
#                 st.write(suggestion)
#         else:
#             st.write("Fehler bei der Anfrage an die API")

# topic = st.text_input('Eingabe:', on_change=proc, key='text_key')


# st.title("Themenbasierte Fragen")