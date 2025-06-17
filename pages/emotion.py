import streamlit as st
import google.generativeai as genai
from transformers import pipeline
import cv2
import numpy as np
from deepface import DeepFace

# Set up Google Gemini API
GOOGLE_API_KEY = 'YOUR_API_KEY'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# Load Emotion Detection Model
text_emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

# Emotion Mapping for Responses
emotion_responses = {
    'joy': "I'm glad to hear you're happy! 😊",
    'anger': "I sense you're upset. Let me know how I can help. 😡",
    'sadness': "I'm here to listen. Sending virtual hugs. 💙",
    'fear': "It's okay to feel scared. You're not alone. 🤗",
    'surprise': "Wow, that sounds exciting! 🎉",
    'neutral': "Got it! Let's continue our chat. 😌"
}

def detect_text_emotion(user_input):
    emotion_scores = text_emotion_classifier(user_input)[0]
    detected_emotion = max(emotion_scores, key=lambda x: x['score'])['label']
    return detected_emotion

def detect_image_emotion(image):
    image_np = np.array(image)
    try:
        faces = DeepFace.analyze(image_np, actions=['emotion'], enforce_detection=False)
        if not faces:
            return "No emotion detected"
        emotions = [face['dominant_emotion'] for face in faces]
        unique_emotions = set(emotions)
        if len(unique_emotions) == 1:
            return f"Detected emotion: {emotions[0]}"
        else:
            return f"Detected emotions: {', '.join(unique_emotions)}"
    except Exception as e:
        return f"Error in detecting emotion: {str(e)}"

def generate_response(user_input, emotion):
    prompt = f"User is feeling {emotion}. Respond appropriately: {user_input}"
    gemini_response = model.generate_content(prompt)
    return gemini_response.text

# Streamlit UI
st.title("Emotion-Aware AI Chatbot")
st.write("Chat with me and I'll understand your emotions! 🧠")

# Chat History
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# User Input
user_input = st.text_input("You:", key="user_input")
if user_input:
    # Detect Text Emotion
    detected_emotion = detect_text_emotion(user_input)

    # Generate Emotion-Aware Response
    gemini_response = generate_response(user_input, detected_emotion)

    # Store chat history
    st.session_state.chat_history.append((user_input, gemini_response))

    # Display Chat
    for user_msg, bot_msg in st.session_state.chat_history:
        st.write(f"**You:** {user_msg}")
        st.write(f"**Bot:** {bot_msg}")

    # Display Emotion Response
    st.write(f"🧠 Detected Emotion: {detected_emotion}")
    st.write(f"🤖 Emotion-Aware Reply: {emotion_responses.get(detected_emotion, 'I am here to assist you.')}")

# Image Upload
uploaded_file = st.file_uploader("Upload an image to detect facial emotion", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    if st.button("Detect Emotion"):
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
        image_emotion = detect_image_emotion(image)
        st.write(f"🖼️ {image_emotion}")
