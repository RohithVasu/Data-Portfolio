from flask import Flask, request, jsonify, render_template
from movies_rag import read_data, embed_and_load, get_relevant_data, make_rag_prompt, generate_answer

app = Flask(__name__)

# Read data from CSV and embed it into ChromaDB
data = read_data('imdb_top_1000.csv')
db = embed_and_load(data)

# Flask route to handle POST requests for queries
@app.route('/ask', methods=['POST'])
def ask_question():
    query = request.json.get('query', '')
    
    # Ensure query is not empty
    if not query:
        return jsonify({'error': 'Query is empty'}), 400
    
    # Process query
    relevant_text = get_relevant_data(query, db)
    prompt = make_rag_prompt(query, relevant_passage=relevant_text)
    answer = generate_answer(prompt)
    
    return jsonify({'answer': answer})

# Flask route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
