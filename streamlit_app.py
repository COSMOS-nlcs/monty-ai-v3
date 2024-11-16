import streamlit as st
from PIL import Image
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Function to load custom CSS

def load_icon():
    img = Image.open("Data/montyface.png")
    return img

# Configure the Generative AI model
genai.configure(api_key="AIzaSyDX632_dk9k7QJeBVMK_FEtIFoYzPIsoXw")
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Read the text instruction file
text_read = open("Data/data1.txt")
text_instr = text_read.read()

# Set up the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-8b",
    generation_config=generation_config,
)

# Start chat session
chat_session = model.start_chat(
    history=[
        {"role": "user", "parts" : "You are NOT an AI, you are a friend. your name is NOT Bard it is Monty and you were created by the COSMOS Society and NOT Google."},
        {"role": "user", "parts" : "DO NOT paraphrase the information"},
        {"role": "model", "parts" : text_instr},
        {"role": "user", "parts": "YOU ARE A FRIEND TO THE USER."},
    ]
)

# Function to display right-aligned message
def right_aligned_message(message):
    st.markdown(
        f'<div style="text-align: right; padding:10px; border-radius:16px;">{message}</div>',
        unsafe_allow_html=True
    )

# Streamlit UI
st.title("Monty AI")
st.text("Created by the COSMOS Society")

hide_streamlit_style = """
            <style>
                    footer {
            display: none;
        } 
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Initialize session state messages if not already initialized
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display all messages from session state
for message in st.session_state.messages:
    if message['role'] == 'user':
        # Right-align user messages
        right_aligned_message(message['parts'])
    else:
        # Display assistant messages in default chat style
        st.chat_message(message['role'],avatar=load_icon()).markdown(message['parts'])

# Get user input
prompt = st.chat_input("chat with Monty")
# Handle user input
if prompt:
    # Display user message with right alignment
    right_aligned_message(prompt)
    st.session_state.messages.append({'role': 'user', 'parts': prompt})

    
    # Get AI response
    response = chat_session.send_message(prompt,
                                         safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
        })
    
    # Display assistant message
    st.chat_message('assistant',avatar=load_icon()).markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "parts": response.text})
