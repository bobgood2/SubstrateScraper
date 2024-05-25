import os
import numpy as np
import faiss
from flask import Flask, request, jsonify

app = Flask(__name__)

# Path to the saved FAISS index
index_file_path = r'C:\download\email_index'

# Load the FAISS index
index = faiss.read_index(index_file_path)

# Define the dimension of embeddings (should match your embeddings' dimension)
embedding_dim = 128

@app.route('/search', methods=['POST'])
def search():
    try:
        # Get the query embedding from the request
        query_embedding = np.array(request.json['embedding'], dtype='float32').reshape(1, -1)
        
        # Check if the query embedding has the correct dimension
        if query_embedding.shape[1] != embedding_dim:
            return jsonify({'error': f'Invalid embedding dimension. Expected {embedding_dim}, got {query_embedding.shape[1]}'})
        
        # Number of nearest neighbors to search for
        k = int(request.json.get('k', 5))
        
        # Perform the search
        distances, indices = index.search(query_embedding, k)
        
        # Prepare the response
        results = [{'index': int(idx), 'distance': float(dist)} for idx, dist in zip(indices[0], distances[0])]
        return jsonify({'results': results})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)