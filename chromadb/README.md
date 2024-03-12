## Installation

Copy "sample.json" file from "embeddings" folder to the folder.
First you have to pull chroma/chromadb image

```python
docker pull chromadb/chroma
```

and then to run chroma database

```python
docker run -p 8081:8000 chromadb/chroma
```

after that you have to build "app.py" service

```python
docker build -t chroma .
```

and run

```python
docker run --add-host=host.docker.internal:host-gateway chroma:latest
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

**if you use your own embedings, dont forget to put them to the "chromadb" folder and update "app.py" code