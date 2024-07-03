import os
import google.generativeai as genai
import streamlit as st

# set gemini api key as environment variable
os.environ['GEMINI_API_KEY'] = 'AIzaSyBWhyNY9PwVDY7PPu6BZqVfxGqFdPw97sY'
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure genai
genai.configure(api_key = gemini_api_key)
model = genai.GenerativeModel('gemini-pro')

# Configure Streamlit page settings
st.set_page_config(page_title='Chat with Gemini-Pro!')
st.title('Hello 👋🏽')

if 'chat_session' not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.initial_prompt_given = False

def translate_role_for_streamlit(user_role):
    if user_role == 'model':
        return 'assistant'
    else:
        return user_role

# Display chat history
for chat in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(chat.role)):
        st.markdown(chat.parts[0].text)

# Initial prompt to set the context for product recommendation
if not st.session_state.initial_prompt_given:
    #initial_prompt = (
     #   "You are an electronic product recommender. Start by asking me what type of electronic product I am looking for, "
      #  "and then continue to ask few short relevant questions based on my responses to recommend the best product."
       #  "Please make it a conversational manner and stick to one question at a time."
    #)

    initial_prompt = (
        """You are a helpful bot that recommends products based on preferences. \
          Start by asking me what type of electronic product I'm looking for and then continue to ask few question based on my responses to recommend the best product. \
          Please stick to one short question at a time. \
          Please respond in a friendly and conversational tone. \
          Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
          Keep continuing the conversation until the user is satisfied and wants to end the conversation. \
          Once the conversation ends provide me search words based on the user input to search for the product in my vector db. Please don't include the product details in it."""
    )

    response = st.session_state.chat_session.send_message(initial_prompt)
    
    with st.chat_message('assistant'):
        st.markdown(response.text)
    
    st.session_state.initial_prompt_given = True

# Input field for user to type their message
prompt = st.chat_input('Your response')

if prompt:
    # Display user message
    with st.chat_message('user'):
        st.markdown(prompt)
    
    # Get response from LLM based on user input
    response = st.session_state.chat_session.send_message(prompt)

    # Display LLM response
    with st.chat_message('assistant'):
        st.markdown(response.text)


