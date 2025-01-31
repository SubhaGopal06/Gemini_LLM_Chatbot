import os
import streamlit as st # type: ignore 
from dotenv import load_dotenv #type: ignore
import google.generativeai as gen_ai #type: ignore

#Loading the environment variables
load_dotenv()

#configure streamlit page settings
st.set_page_config(
    page_title = "Chat with Gemini!",
    page_icon = ":brain:", 
    layout = "centered"
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

#Set-up the AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

#Function to translate between gemini-pro and streamlit
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role
    
#Initialize chat session in streamlit if not present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

#Here is the main page title
st.title("🤖 Gemini Pro - Chatbot")  

#Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

#Input field for user message
user_prompt = st.chat_input("Ask Gemini-Pro....")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    #Adding user's message to chat and display

    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    #Send user message and get response back

    #Display response
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
