import os
import bs4
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import google.generativeai as genai

# set gemini api key as environment variable
os.environ['GEMINI_API_KEY'] = 'AIzaSyBWhyNY9PwVDY7PPu6BZqVfxGqFdPw97sY'

def load_data(url):
    loader = WebBaseLoader(web_paths = (url,),
                bs_kwargs=dict(parse_only = bs4.SoupStrainer(class_ = ("mw-content-container"))))

    text_documents=loader.load()
    
    return text_documents

text_documents = load_data('https://en.wikipedia.org/wiki/Film')

def embed_and_load(text_documents):
    # split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    docs = text_splitter.split_documents(text_documents)

    # embed load to chromaDB
    embeddings = SentenceTransformerEmbeddings(model_name = 'sentence-transformers/all-mpnet-base-v2')
    db = Chroma.from_documents(docs, embeddings)

    return db

db = embed_and_load(text_documents)

def make_rag_prompt(db, query):
    # get relevant data
    relevant_data = db.similarity_search(query = query)

    # create a prompt for LLM
    prompt = ("""You are a helpful and informative bot that answers questions using text from the reference passage included below. \
          Be sure to respond in a complete sentence, being comprehensive, including all relevant background information. \
          strike a friendly and converstional tone. \
          If the passage is irrelevant to the answer, you may ignore it.
          QUESTION: '{query}'
          PASSAGE: '{relevant_data}'

          ANSWER:
          """).format(query = query, relevant_data = relevant_data)
    
    return prompt

def generate_answer(prompt):
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("Gemini API Key not provided. Please provide GEMINI_API_KEY as an environment variable")
    genai.configure(api_key = gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
    answer = model.generate_content(prompt)
    return answer.text

def final_answer(db, query):
    prompt = make_rag_prompt(db, query)
    answer = generate_answer(prompt)

    return answer

import streamlit as st

st.title('Hello There! Ask me a question')

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

user_input = st.text_input("You: ", "")

if user_input:
    answer = final_answer(db = db, query = user_input)
    
    # Clear previous conversation to display only current question and answer
    st.session_state.conversation.clear()
    
    # Update conversation with current question and answer
    st.session_state.conversation.append(("You", user_input))
    st.session_state.conversation.append(("Bot", answer))


# Display current conversation (question and answer)
for speaker, text in st.session_state.conversation:
    st.write(f"{speaker}: {text}")