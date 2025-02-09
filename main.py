import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import speech_recognition as sr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Streamlit Page Configuration
st.set_page_config(page_title="AI Image & Speech App", layout="wide")

# Custom CSS Styling
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
        
    
    <style>
    .stApp {
        background-color: #212f3c  !important;
        padding: 20px;
    }

    .title-container {
        text-align: center;
        margin-bottom: 30px;
    }

    .upload-container {
        text-align: center;
        margin-bottom: 40px;
    }

    .stButton>button {
        background-color: #1A2A50 !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-size: 16px;
    }

    .stTextArea textarea {
        border-radius: 10px !important;
        border: 1px solid #94A1BB !important;
        padding: 10px !important;
    }

    .center-button {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }

    .footer {
        background-color: #1A2A50;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 10px;
        margin-top: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Navigation Button
if st.button("💬 Just Chat"):
    st.switch_page("pages/chat.py")  # Navigates to chat.py in the same tab
# # Add "Just Chat" button in the top-right corner
# st.markdown("<div class='chat-button'>", unsafe_allow_html=True)
# if st.button("💬 Just Chat", key="chat_button"):
#     os.system("streamlit run chat.py")  # Runs chat.py script
# st.markdown("</div>", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='title-container'>🎙️ AI IMAGE RECOGNITION & IMAGE APP</h1>", unsafe_allow_html=True)
st.markdown("<p class='title-container'>Upload an image, enter text, or speak to interact with AI.</p>",
            unsafe_allow_html=True)

# Image Upload Section
st.markdown("<div class='upload-container'><h2>📸 Upload an Image</h2></div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="image_uploader")

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True, output_format="JPEG")

st.markdown("<br><br>", unsafe_allow_html=True)  # Add some space

# Layout with Two Columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📜 Enter Text")
    input_text = st.text_area("Type your input:", placeholder="Enter prompt here...", height=150)

with col2:
    st.subheader("🎤 Speak Input")

    # Recognized Speech Area (comes first)
    recognized_text = st.text_area("Recognized Speech:", "", height=100, disabled=True)

    # Speech Recognition Button (comes after text area)
    if st.button("Start Speech Recognition", key="speech_button"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening...")
            try:
                audio = recognizer.listen(source)
                spoken_text = recognizer.recognize_google(audio)
                recognized_text = spoken_text  # Update recognized text dynamically
                st.experimental_rerun()
            except sr.UnknownValueError:
                st.warning("Could not understand the audio.")
            except sr.RequestError:
                st.error("Speech recognition service error.")

# Centered "Generate Response" Button
st.markdown("<div class='center-button'>", unsafe_allow_html=True)
if st.button("🚀 Generate Response", key="generate_button"):
    st.success("Response Generated!")
st.markdown("</div>", unsafe_allow_html=True)

# Footer Section
st.markdown(
    """
    <div class='footer'>
        <p><strong>Project Team:</strong> AI & Data Science Department</p>
        <p><strong>Guide:</strong> Prof. XYZ</p>
        <p><strong>Team Members:</strong> Alice, Bob, Charlie, David</p>
        <p>&copy; 2024 AI Image & Speech App. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)
