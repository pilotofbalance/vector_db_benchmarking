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

from pymilvus import (
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility,
)
import json
import math

#loading data
f = open('sample.json')
data = json.load(f)

def load_index():

    connections.connect("default", host="host.docker.internal", port="19530")

    start = time.time()
    print("START TIME: ",start) 
    vectors = []
    for item in data:
        vectors.append(item["embedding"])
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="embedings", dtype=DataType.FLOAT_VECTOR, dim=len(vectors[0]))
    ]
    schema = CollectionSchema(fields, "milvus test")
    utility.drop_collection("reports")
    collection = Collection("reports", schema)
    index_params = {
        "metric_type":"COSINE",
        "index_type":"HNSW",
        "params": {
            "M": 16,
            "efConstruction": 500,
            "efSearch": 200
        }
    }
    collection.create_index(field_name="embedings", index_params=index_params)

    # Convert vectors to numpy array
    vectors_np = np.array(vectors, dtype=np.float32)

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
            ids.append(int(x))

        entities = [
            ids,  # field id
            vectors_np[n*batch_size:n*batch_size + to],  # field embeddings
        ]
        insert_result = collection.insert(entities)

    collection.flush()  
    
    end = time.time()
    print("END TIME: ",end) 
    print("LOADING TIME: ",(end - start)*1000)  
    print(collection.num_entities)              # add vectors to the index
    print(insert_result)
    collection = Collection("reports")      # Get an existing collection.
    collection.load()
    return collection

def create_app():
    app = Flask(__name__)
    collection = load_index()
    
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
        # collection = Collection("reports")      # Get an existing collection.
        # collection.load()
        search_params = {
            "metric_type": "COSINE", 
            "offset": 0, 
            "ignore_growing": False, 
            "params": {"ef": 200}
        }
        res = collection.search(
            data=np.array([vector]), 
            anns_field="embedings", 
            param=search_params,
            limit=n,
            expr=None,
            consistency_level="Bounded"
        )
        
        end = time.time()
        print("END TIME: ",end) 
        print("ELAPSED TIME: ",(end - start) * 1000)  
    
        # get the IDs of all returned hits
        print(res[0].ids, flush=True)

        # get the distances to the query vector from all returned hits
        print(res[0].distances, flush=True)
        for i in res[0].ids:
            print(i, flush=True)
            print(data[i]["sentence"], flush=True)
            print("")
        result['status'] = 'ok'
        # collection.release()
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
    application.run(host='0.0.0.0', port=5010)