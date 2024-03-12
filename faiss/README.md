## Installation

Copy "sample.json" file from "embeddings" folder to the folder.
First you have to build "app.py" service

```python
docker build -t faiss .
```

and run

```python
docker run faiss:latest
```

now your "app.py" service is running and you can query vector:

```python
curl -X POST http://HOST:PORT/search \
    -H 'Content-Type: application/json' \
    -d '{
    "vector": "0.003143557347357273, 0.04049545153975487, ..., -0.01583821326494217",
    "n": 10
}'
```
vector param should contain "string" vector
n param should contain "int" num of requested nearest vectors

see service logs for more info

**if you use your own embedings, dont forget to put them to the "faiss" folder and update "app.py" code