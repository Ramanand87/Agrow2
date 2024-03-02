import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY=os.environ.get('API_KEY')
os.environ["OPENAI_API_KEY"]=API_KEY

st.set_page_config(page_title="Chatbot", page_icon=":robot:")
st.header("Hey, I'm your Crop Health Checker")

if "sessionMessages" not in st.session_state:
     st.session_state.sessionMessages = []


for message in st.session_state.sessionMessages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)
    elif isinstance(message, SystemMessage):
        with st.chat_message("system"):
            st.markdown(message.content)
def load_answer(question):
    assistant_answer = chat([HumanMessage(content=question)])
    st.session_state.sessionMessages.append(AIMessage(content=assistant_answer.content))
    
    return assistant_answer.content


def get_text():
    user_input = st.text_input("You: ", key="input")
    if user_input and not any(message.content == user_input for message in st.session_state.sessionMessages): 
        st.session_state.sessionMessages.append(HumanMessage(content=user_input))
    return 'Give Agriculture recommendations or information: '+ user_input

chat = ChatOpenAI(temperature=0)

user_input=get_text()
submit = st.button('Generate')  

if submit:
    # st.session_state.sessionMessages.pop()
    load_answer(user_input)
    st.experimental_rerun()


localhost_address = "http://127.0.0.1:8000"  
button_html = f"""
    <div style="position: absolute; top: 10px; left: 10px;">
        <a href="{localhost_address}/home" target="_blank">
            <button style="padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
                Home
            </button>
        </a>
    </div>  
"""

st.markdown(button_html, unsafe_allow_html=True)
