
import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from datetime import datetime
import requests 
from streamlit import components
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY=os.environ.get('API_KEY')
os.environ["OPENAI_API_KEY"]=API_KEY


# os.environ["OPENAI_API_KEY"]=""
chat = ChatOpenAI(temperature=0)
st.set_page_config(page_title="Check your crop health", page_icon=":herb:")
st.header("Hey, I'm your Crop Health Checker")
is_first=1
chat = ChatOpenAI(temperature=0)
if "sessionMessages" not in st.session_state:
    st.session_state.sessionMessages = []
def load_answer(question):
    assistant_answer = chat(st.session_state.sessionMessages)
    st.session_state.sessionMessages.append(AIMessage(content=assistant_answer.content))
    return assistant_answer.content

def get_text():
    user_input = st.text_input("You: ", key="input")
    if user_input and not any(message.content == user_input for message in st.session_state.sessionMessages): 
        st.session_state.sessionMessages.append(HumanMessage(content=user_input))
    return 'Give Agriculture recommendations or information: '+ user_input

st.markdown(
    """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css" integrity="sha384-oS3vJWskMzfuMztfHH9x0kx91IMQmTYFy87Loz9IEeq6PD8tdMz1ZN/sMO7spwF" crossorigin="anonymous">
    """,
    unsafe_allow_html=True
)
if len(st.session_state.sessionMessages)==0:
    with st.form(key='my_form'):
        language_choice = st.radio("Select language:", ["English", "Hindi"])
        lg_change = st.form_submit_button(label="Change")
        if lg_change:
            st.rerun()
        if language_choice == "Hindi":
            label_crop_name = 'फसल का नाम'
            label_growth_stage = 'विकास-स्तर'
            label_crop_condition = 'फसल की स्थिति'
            label_crop_issues = 'फसल की समस्याएँ'
            label_generate = 'उत्पन्न करें'
            label_weather="अगले 5 दिनों का मौसम"
            label_gen="मुझे फसल स्वास्थ्य के बारे में जानकारी और उपलब्ध मौसम आंकड़ों के अनुसार कुछ सिफारिशें भी दें"
            
        else:
            label_crop_name = 'Crop Name'
            label_growth_stage = 'Growth-Stage'
            label_crop_condition = 'Crop Condition'
            label_crop_issues = 'Issues with Crop'
            label_generate = 'Generate'
            label_weather='Next 5 day weather'
            label_gen="Give me information about crop health and some recommendations according to provided weather data also"
       
        crop_name = st.text_input(label=label_crop_name)
        growth_stage = st.text_input(label=label_growth_stage)
        crop_condition = st.text_input(label=label_crop_condition)
        crop_issues = st.text_input(label=label_crop_issues)
        submit_button = st.form_submit_button(label=label_generate)
        city = 'Pune'
        API_key = 'ec3c5349acccf30efb4e7c6727731563'
        url2 = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_key}'
        city_weather2=requests.get(url2).json()
        filtered_weather2=[]
        stri=""
        now = datetime.now().date()
        date_checked = set()
        for item in city_weather2['list']:
            if item['dt_txt'][:10] != str(now) and item['dt_txt'][:10] not in date_checked:
                filtered_weather2.append(item)
                date_checked.add(item['dt_txt'][:10])

        for item in filtered_weather2:
            item['main']['temp_min'] = str(int(int(item['main']['temp_min']) - 273.15))
            item['main']['temp_max'] = str(int(int(item['main']['temp_max'])- 273.15))
            dt_txt = item['dt_txt']
            date_obj = datetime.strptime(dt_txt[:10], '%Y-%m-%d')
        is_hindi=False
        
        for item in filtered_weather2:
             stri= stri + "\n" + " Date: "+ item['dt_txt'][0:10] + " Temp min : " + (item['main']['temp_min']) + "°C " + " Temp max: " + (item['main']['temp_max']) + "°C" + " Humidity: "+ str(item['main']['humidity'])
        if submit_button:
            user_input = f'{label_crop_name}: {crop_name}, {label_growth_stage}: {growth_stage}, {label_crop_condition}: {crop_condition}, {label_crop_issues}: {crop_issues}'
            question=user_input+f' \n {label_weather}:{stri}   {label_gen}'
            st.session_state.sessionMessages.append(HumanMessage(content=user_input))
            assistant_answer = chat([HumanMessage(content=question)])
            st.session_state.sessionMessages.append(AIMessage(content=assistant_answer.content))
            st.rerun()
else:
    for message in st.session_state.sessionMessages:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown('<i class="fas fa-leaf" style="color: green;"></i>  ' + message.content, unsafe_allow_html=True)
        elif isinstance(message, SystemMessage):
            with st.chat_message("system"):
                st.markdown(message.content)



    user_input = get_text()
    submit = st.button('Generate')  
    if submit:
        load_answer(user_input)
        st.experimental_rerun()
        
localhost_address = "http://127.0.0.1:8000"  
button_html = f"""
    <div style="position: fixed; top: 50px; left: 60px;">
        <a href="{localhost_address}/home" target="_blank">
            <button style="padding: 10px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">
                Home
            </button>
        </a>
    </div>      
"""

st.markdown(button_html, unsafe_allow_html=True)


st.markdown(
    """
    <style>
    .st-emotion-cache-1wbqy5l {color:white;}
    .st-emotion-cache-1pbsqtx {color:white;}
    </style>
    """,
    unsafe_allow_html=True
)

# import speech_recognition as sr
# r=sr.Recognizer()
# while True:
#     try:
#         with sr.Microphone() as source:
#             print("Say")
#             audio=r.listen(source)
#             text=r.recognize_google(audio)
#             text=text.lower()
#             print(text)
#     except:
#         print("Nothing")
#         r=sr.Recognizer()
#         continue
            
