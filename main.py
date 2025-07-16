import streamlit as st
import speech_recognition as sr
import nltk
from nltk.chat.util import Chat, reflections

# Download NLTK data (only once)
nltk.download('punkt')

# Define chatbot conversation pairs
pairs = [
    (r"hi|hello|hey", ["Hello!", "Hi there!", "Hey!"]),
    (r"how are you ?", ["I'm fine, thank you!", "Doing well, how about you?"]),
    (r"what is your name ?", ["I am a chatbot. You can call me ChatBot."]),
    (r"quit", ["Bye! Take care."]),
    # Add more patterns and responses here
]

# Initialize chatbot
chatbot = Chat(pairs, reflections)

def transcribe_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Please speak now...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        st.success(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
    except sr.RequestError:
        st.error("Could not request results from Google Speech Recognition service.")
    return ""

def chatbot_response(user_input):
    response = chatbot.respond(user_input)
    if response:
        return response
    else:
        return "Sorry, I don't understand."

def main():
    st.title("🎤 Speech-enabled Chatbot")
    
    input_type = st.radio("Choose input type:", ("Text", "Speech"))
    
    if input_type == "Text":
        user_text = st.text_input("Enter your message:")
        if user_text:
            response = chatbot_response(user_text.lower())
            st.text_area("Chatbot response:", value=response, height=100)
    
    else:  # Speech input
        if st.button("Record Speech"):
            user_speech = transcribe_speech()
            if user_speech:
                response = chatbot_response(user_speech.lower())
                st.text_area("Chatbot response:", value=response, height=100)

if __name__ == "__main__":
    main()
