## Installation
Copy "sample.json" file from "embeddings" folder to the "app" folder.
First you have to run milvus database

```python
bash standalone_embed.sh start
```

this script will pull and run for you milvus db
after that you have to build "app.py" service, go to "app" folder

```python
cd app
```
and build your "app.py" service

```python
docker build -t milvus .
```
then just run it

```python
docker run --add-host=host.docker.internal:host-gateway milvus:latest
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

**if you use your own embedings, dont forget to put them to the "milvus/app" folder and update "app.py" code