import os
import json
import streamlit as st
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import google.generativeai as genai

# Set the environment variable for the API key
os.environ['GEMINI_API_KEY'] = '********'

# Function to read data from the JSON file
def read_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        sample_data = json.load(f)

    content = []
    for data in sample_data['data']:
        for paragraph in data['paragraphs']:
            content.append(paragraph['context'])
    return content

content = read_data('dev-v2.0.json')

# Function to embed content and load it into ChromaDB
def embed_and_load(content):
    embeddings = SentenceTransformerEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
    db = Chroma.from_texts(content, embeddings)
    return db

db = embed_and_load(content)

# Function to get relevant data from ChromaDB
def get_relevant_data(query, db):
    passage = db.similarity_search(query=query)
    return passage

# Function to create a RAG prompt
def make_rag_prompt(query, relevant_passage):
    prompt = ("""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
    Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
    However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
    strike a friendly and conversational tone. \
    If the passage is irrelevant to the answer, you may ignore it.
    QUESTION: '{query}'
    PASSAGE: '{relevant_passage}'

    ANSWER:
    """).format(query=query, relevant_passage=relevant_passage)
    return prompt

# Function to generate an answer using Gemini AI
def generate_answer(prompt):
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("Gemini API Key not provided. Please provide GEMINI_API_KEY as an environment variable")
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
    answer = model.generate_content(prompt)
    return answer.text

# Function to get the final answer
def final_answer(db, query):
    relevant_text = get_relevant_data(query, db)
    prompt = make_rag_prompt(query, relevant_passage=relevant_text)
    answer = generate_answer(prompt)
    return answer

# Streamlit app
st.title('Hello There! Ask me a question')

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

user_input = st.text_input("You: ", "What is the scientific model of a general computing machine?")

if user_input:
    answer = final_answer(db=db, query=user_input)
    
    # Update conversation history
    st.session_state.conversation.append(("You", user_input))
    st.session_state.conversation.append(("Bot", answer))

    # Display conversation history
    for speaker, text in st.session_state.conversation:
        st.write(f"{speaker}: {text}")
