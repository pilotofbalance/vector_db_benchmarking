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

import chromadb
import json
import math

#loading data
f = open('sample.json')
data = json.load(f)

def load_index():
    client = chromadb.HttpClient(host="host.docker.internal", port=8081)
    collection_name = "reports"
    collection = client.list_collections()
    if len(collection) > 0:
        # If the collection exists, drop it
        client.delete_collection(collection_name)
    collection_metadata = {
        "hnsw:space": "cosine",
        "hnsw:M": 16,
        "hnsw:construction_ef": 500,
        "hnsw:search_ef": 200
    }
    # collection = client.create_collection(name="reports", metadata={"hnsw:space": "cosine", "hnsw:construction_ef": 20, "hnsw:M": 5}, )
    collection = client.create_collection(name=collection_name, metadata=collection_metadata, )

    vectors = []
    for item in data:
        vectors.append(item["embedding"])
    
    # Convert vectors to numpy array
    vectors_np = np.array(vectors, dtype=np.float32)
    start = time.time()
    print("START TIME: ",start) 
    batch_size=41666
    num=math.ceil(len(vectors_np)/batch_size)
    print(num) 
    for n in range(num):
        ids = []
        counter=len(vectors_np) - n * batch_size
     
        to=batch_size
        if counter < batch_size:
            to=counter

        for x in range(n*batch_size,n*batch_size + to): 
            ids.append(str(x))
        
        collection.add(
            embeddings=vectors_np[n*batch_size:n*batch_size + to],
            ids=ids
        )
        
    end = time.time()
    print("END TIME: ",end) 
    print("LOADING TIME: ",(end - start)*1000)                # add vectors to the index
    print(collection.count())
    return collection

def create_app():
    app = Flask(__name__)
    collection  = load_index()

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
        res = collection.query(
            query_embeddings=np.array([vector]),
            n_results=n,
        )
        end = time.time()
        print("END TIME: ",end) 
        print("ELAPSED TIME: ",(end - start) * 1000)  
        print(res["ids"][0], res["distances"][0])
        for i in res["ids"][0]:
            print(int(i), flush=True)
            print(data[int(i)]["sentence"], flush=True)
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
    application.run(host='0.0.0.0', port=5005)