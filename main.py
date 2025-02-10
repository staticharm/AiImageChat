import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
from dotenv import load_dotenv
from pydub import AudioSegment
import base64

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Streamlit Page Configuration
st.set_page_config(page_title="AI Image & Speech App", layout="wide")

# JavaScript for Audio Recording in Browser
AUDIO_RECORDER_JS = """
<script>
let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };
        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            const reader = new FileReader();
            reader.readAsDataURL(audioBlob);
            reader.onloadend = () => {
                const base64Audio = reader.result.split(',')[1];
                fetch('/record_audio', {
                    method: "POST",
                    body: JSON.stringify({ audio: base64Audio }),
                    headers: { "Content-Type": "application/json" }
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("speech_output").innerText = data.text;
                });
            };
        };
        mediaRecorder.start();
    });
}

function stopRecording() {
    mediaRecorder.stop();
}
</script>
"""

# Custom CSS Styling
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        .stApp { background-color: #212f3c !important; padding: 20px; }
        .title-container { text-align: center; margin-bottom: 30px; }
        .upload-container { text-align: center; margin-bottom: 40px; }
        .center-button { display: flex; justify-content: center; margin-top: 30px; }
        .footer { background-color: #1A2A50; color: white; padding: 10px; text-align: center; border-radius: 10px; margin-top: 40px; }
    </style>
    """,
    unsafe_allow_html=True
)

# Add JavaScript for Live Recording
st.markdown(AUDIO_RECORDER_JS, unsafe_allow_html=True)

# Title
st.markdown("<h1 class='title-container'>🎙️ AI IMAGE & SPEECH APP</h1>", unsafe_allow_html=True)

# Image Upload Section
st.markdown("<h2>📸 Upload an Image</h2>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="image_uploader")

image = None
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True, output_format="JPEG")

st.markdown("<br><br>", unsafe_allow_html=True)  # Add space

# Layout with Two Columns
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📜 Enter Text")
    input_text = st.text_area("Type your input:", placeholder="Enter prompt here...", height=150)

with col2:
    st.subheader("🎤 Speak Input")

    # JavaScript Buttons for Recording
    st.markdown(
        """
        <button onclick="startRecording()">Start Recording</button>
        <button onclick="stopRecording()">Stop Recording</button>
        <p id="speech_output">Speech will appear here...</p>
        """,
        unsafe_allow_html=True
    )

# Backend: Process Recorded Audio
if "recorded_audio" not in st.session_state:
    st.session_state["recorded_audio"] = ""


def process_audio(base64_audio):
    # Decode Base64 to WAV
    audio_data = base64.b64decode(base64_audio)
    audio_path = "temp_audio.wav"

    with open(audio_path, "wb") as f:
        f.write(audio_data)

    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            text = "Speech not recognized."
        except sr.RequestError:
            text = "Speech recognition service error."

    return text


# AI Response Function
def get_gemini_response(input_text, speech_text, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    combined_input = f"{input_text}\n{speech_text}" if speech_text else input_text
    if combined_input.strip():
        response = model.generate_content([combined_input, image] if image else [combined_input])
        return response.text
    return "Please provide some input."


# Text-to-Speech Function
def text_to_speech(response_text):
    tts = gTTS(text=response_text, lang="en")
    audio_path = "response_audio.mp3"
    tts.save(audio_path)
    return audio_path


# Generate AI Response
st.markdown("<div class='center-button'>", unsafe_allow_html=True)
if st.button("🚀 Generate Response", key="generate_button"):
    final_text = input_text.strip() + "\n" + st.session_state["recorded_audio"].strip()
    if not final_text.strip():
        st.warning("Please enter text or speak before generating a response.")
    else:
        with st.spinner("Generating response..."):
            response = get_gemini_response(input_text, st.session_state["recorded_audio"], image)
            st.session_state["ai_response"] = response
            st.session_state["audio_file"] = text_to_speech(response)
        st.success("Response Generated!")
        st.write(response)
st.markdown("</div>", unsafe_allow_html=True)

# Play AI-Generated Speech
if "audio_file" in st.session_state and st.session_state["audio_file"]:
    st.audio(st.session_state["audio_file"], format="audio/mp3")

# Footer
st.markdown(
    """
    <div class='footer'>
        <p><strong>Project Team:</strong> AI & Data Science Department</p>
        <p>&copy; 2024 AI Image & Speech App. All rights reserved.</p>
    </div>
    """,
    unsafe_allow_html=True
)
