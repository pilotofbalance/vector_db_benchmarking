# Vector Databese Benchmarking

In this POC we gonna compare most popular vector databases and libraries.
**FAISS**  - semantic search library
**CHROMA** - popular open-source vector database
**MILVUS** - mature open-source vector database

## Prepare embeddings

Our "embedings" folder already contain "train_set.json" file with 135k radiology medical reports.
This set has been embedded to the vectors with "test.py" code with popular semantic search 
trained model: "sentence-transformers/all-MiniLM-L6-v2". This transformation produced "sample.json" file
which we gonna use and inject to our vector databases. 
**The "sample.json" file is not included here for size reasons.FYI transformation could take around 2 hours and produce more then 1gb "sample.json" file.**

You can use your own dataset and run transformation to the vectors with this command:

```bash
python ./test.py
```
To test our embedings with same trained model, there is aslo a short query.json which contains embedded vectors.
You can find commented code into "test.py" file to change and produce your own "query set" for tests.

## Installation

Before that make sure you have a "docker" and "docker compose" installed on your machine.
There is 3 folders for each database and READMY file which could help you to build and run each one.
If you have enough powerfull machine you can run all 3 together, although the suggestion is to test them one by one.

## Usage

To execute "load test" we gonna use k6 tool, you can find it under "k6" folder.
Make sure you have k6 installed on your machine.

Check out scenarious into "k6/script.js" file and feel free to make your own.
Run test:

```python
k6 run script.js
```

## Presentation

You can find presentation slides here "vec_db_benchmarking.odp" in this project and see the results.
