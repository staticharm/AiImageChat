from dotenv import load_dotenv

load_dotenv()  ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai
st.set_page_config(page_title="Q&A Demo")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get repsonses
model = genai.GenerativeModel("gemini-1.5-flash-latest")
chat = model.start_chat(history=[])

st.markdown(
    """
    <style>
        .title-container { text-align: center; margin-bottom: 30px;}
        .stButton>button { background-color: #1A2A50 !important; color:#E8F9FF !important; border-radius: 10px !important; padding: 12px 24px !important; font-size: 16px; }
        .stTextArea textarea { border-radius: 10px !important; border: 1px solid #C4D9FF !important; padding: 10px !important; }
        .center-button { display: flex; justify-content: center; margin-top: 30px; }
        .footer {  padding: 100px; text-align: center; border-radius: 10px; margin-top: 40px; }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("💬 Image chatbot"):
    st.switch_page("main.py")

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


##initialize the streamlit app


#st.header("Gemini LLM Application")
st.markdown("<h1 class='title-container'>  Q&A CHATBOT</h1>", unsafe_allow_html=True)
# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))
st.subheader("The Chat History is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

st.markdown(
    """
    <div class='footer'>
        <p><strong>College</strong> D.B.I.T</p>
        <p><strong>Department:</strong> AI & Data Science Department</p>
        <p><strong>Guide:</strong> Dr Gowramma G S</p>
        <p><strong>Team Members:</strong> Vaishnavi, Rishab,Navneeth , Sudheendra</p>
        <p>&copy; 2024 AI Image & Speech App. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)