import os
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma
import google.generativeai as genai

# Set Gemini API key as environment variable
os.environ['GEMINI_API_KEY'] = 'AIzaSyBWhyNY9PwVDY7PPu6BZqVfxGqFdPw97sY'

# Function to read data from CSV
def read_data(file_name):
    file_path = file_name
    loader = CSVLoader(file_path=file_path)
    data = loader.load()

    content = [doc.page_content for doc in data]
    return content

# Function to embed data and load into ChromaDB
def embed_and_load(content):
    embeddings = SentenceTransformerEmbeddings(model_name='sentence-transformers/all-mpnet-base-v2')
    db = Chroma.from_texts(content, embeddings)
    return db

# Function to retrieve relevant data based on query
def get_relevant_data(query, db):
    passage = db.similarity_search(query=query)
    return passage

# Function to create RAG prompt
def make_rag_prompt(query, relevant_passage):
    prompt = f"""You are a helpful and informative bot that gives information about movies using text from the reference passage included below.
    Be sure to respond in a complete sentence, being comprehensive, including all relevant background information.
    Strike a friendly and conversational tone.
    If the passage is irrelevant to the answer, you may ignore it.
    QUESTION: '{query}'
    PASSAGE: '{relevant_passage}'

    ANSWER:
    """
    return prompt

# Function to generate answer using Gemini AI
def generate_answer(prompt):
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("Gemini API Key not provided. Please provide GEMINI_API_KEY as an environment variable")
    
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-pro')
    answer = model.generate_content(prompt)
    return answer.text
