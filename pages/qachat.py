from dotenv import load_dotenv
import psutil
import time
import platform

load_dotenv()  ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai
st.set_page_config(page_title="Q&A Demo")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## function to load Gemini Pro model and get repsonses
model = genai.GenerativeModel("models/gemini-2.5-flash")
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

# def get_gemini_response(question):
#     # Start measuring latency
#     start_time = time.time()
    
#     # Measure system usage before request
#     process = psutil.Process(os.getpid())
#     mem_before = process.memory_info().rss / (1024 * 1024)
#     cpu_before = psutil.cpu_percent(interval=None)

#     # Send message to Gemini
#     response = chat.send_message(question, stream=True)
#     full_response = "".join([chunk.text for chunk in response])

#     # Measure after response
#     end_time = time.time()
#     mem_after = process.memory_info().rss / (1024 * 1024)
#     cpu_after = psutil.cpu_percent(interval=None)

#     latency = round(end_time - start_time, 3)
#     mem_usage = round(mem_after - mem_before, 2)
#     cpu_usage = round(abs(cpu_after - cpu_before), 2)

#     metrics = {
#         "Latency (s)": latency,
#         "Memory Change (MB)": mem_usage,
#         "CPU Usage (%)": cpu_usage,
#     }

#     return full_response, metrics

##initialize the streamlit app





from performanceLogger import log_performance

def get_gemini_response(question):
    def send_message(q):
        response = chat.send_message(q, stream=True)
        return "".join([chunk.text for chunk in response])

    full_response, metrics = log_performance("Q&A Chatbot (Streaming)", question, send_message)
    return full_response, metrics


#st.header("Gemini LLM Application")
st.markdown("<h1 class='title-container'>  Q&A CHATBOT</h1>", unsafe_allow_html=True)
# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input_text = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")


if submit and input_text:
    response, metrics = get_gemini_response(input_text)
    st.session_state['chat_history'].append(("You", input_text))
    st.subheader("The Response is")
    st.write(response)

    st.session_state['chat_history'].append(("Bot", response))

    # ------------------- DISPLAY PERFORMANCE METRICS -------------------
    st.markdown("### ⚙️ Performance Metrics")
    st.metric("Latency (seconds)", metrics["Latency (s)"])
    st.metric("Memory Change (MB)", metrics["Memory Change (MB)"])
    st.metric("CPU Usage (%)", metrics["CPU Usage (%)"])

st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")


st.markdown(
    """
    <div class='footer'>
        <p><strong>Sudheendra HR</strong> </p>
        <p>&copy; 2024 AI Image & Speech App. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)