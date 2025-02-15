import streamlit as st
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

nltk.download('punkt')
nltk.download('stopwords')

logging.debug("Downloading NLTK data...")

chatbot = pipeline("text-generation", model="gpt2")
logging.debug("Chatbot model loaded.")

def preprocess_input(user_input):
    logging.debug(f"Preprocessing input: {user_input}")
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(user_input)
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

def healthcare_chatbot(user_input):
    logging.debug(f"Received user input: {user_input}")
    user_input = preprocess_input(user_input)
    logging.debug(f"Preprocessed input: {user_input}")
    if "sneeze" in user_input or "sneezing" in user_input:
        return "You may have a cold."
    elif "sympton" in user_input:
        return "I am not a doctor. Please consult a doctor."
    elif "appointment" in user_input:
        return "You can book an appointment at the hospital's website."
    elif "medication" in user_input:
        return "Please consult a doctor for medication."
    else:
        response = chatbot(user_input, max_length=50)
        logging.debug(f"Generated response: {response[0]['generated_text']}")
        return response[0]['generated_text']

#for web interface using streamlit
def main():
    st.title("Healthcare Chatbot by shanmugapriyan")
    user_input = st.text_input("How can i assisit you today?", "")
    if st.button("Ask"):
        if user_input:
            st.write("User: ", user_input)
            response = healthcare_chatbot(user_input)
            st.write("Healthcare Assistant: ", response)
        else:
            st.write("Please enter a question.")

if __name__ == "__main__":
    main()
