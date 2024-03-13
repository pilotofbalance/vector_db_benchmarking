import os
import sys
import flask
import os
import numpy as np
import re
import time

from flask import Flask
from flask import make_response
from flask import request
from werkzeug.utils import secure_filename

import faiss
import json
#loading data
# Opening JSON file
f = open('sample.json')
    
# returns JSON object as 
# a dictionary
data = json.load(f)
def load_index():
    #loading data
    # Opening JSON file
    # f = open('sample.json')
    
    # # returns JSON object as 
    # # a dictionary
    # data = json.load(f)
        
    vectors = []
    for item in data:
        vectors.append(item["embedding"])
    
    # Convert vectors to numpy array
    vectors_np = np.array(vectors, dtype=np.float32)
 
    # Create an index in Faiss
    dimension = len(vectors[0])  # Dimension of the vectors
     # index = faiss.IndexHNSWFlat(dimension, 16)
    index = faiss.index_factory(dimension, "HNSW32,Flat", faiss.METRIC_INNER_PRODUCT)
    index.hnsw.M = 16
    index.hnsw.efConstruction = 500
    index.hnsw.efSearch = 200
    # Set the metric to Cosine Similarity
    # index.metric_type = faiss.METRIC_INNER_PRODUCT
    print(faiss.__version__)
    print(index.is_trained)
    start = time.time()
    print("START TIME: ",start) 
    index.add(np.array(np.array(vectors_np, dtype=np.float32)))
    end = time.time()
    print("END TIME: ",end) 
    print("LOADING TIME: ",(end - start)*1000)                # add vectors to the index
    print(index.ntotal)
    return index

def create_app():
    app = Flask(__name__)
    index  = load_index()

    # @app.route('/ping', methods=['GET'])
    # def ping():
    #     return flask.jsonify(ping='pong')

    @app.route("/search", methods=["POST"])
    def get_similarities():
        result = {}
        n = 1

        content = request.json
        num = content["n"]
        vec = content["vector"]

        n = int(num)
        
        vector = np.fromstring(vec, dtype=np.float32, sep=',')
        if len(vector) == 0:
            result['status'] = 'error'
            result['message'] = 'empty value'
            return flask.jsonify(result), 400

        start = time.time()
        print("START TIME: ",start) 
        D, I = index.search(np.array([vector]), n) 
        end = time.time()
        print("END TIME: ",end) 
        print("ELAPSED TIME: ",(end - start) * 1000)  

        print(I[0], D)
        for i in I[0]:
            print(i)
            print(data[i]["sentence"], flush=True)
            print("")
        result['status'] = 'ok'
        return flask.jsonify(result), 200

    @app.errorhandler(404)
    def error_404(e):
        result = {}
        result['status'] = 'error'
        result['message'] = '404 - the requested URL is not available with this method'
        
        return flask.jsonify(result)  

    @app.errorhandler(500)
    def error_500(e):
        result = {}
        result['status'] = 'error'
        result['message'] = '500 - internal error'
        return flask.jsonify(result)

    return app

if __name__ == "__main__":
    application = create_app()
    application.run(host='0.0.0.0', port=5000)