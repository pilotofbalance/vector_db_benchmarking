#!/bin/bash

chroma run --host 0.0.0.0 --port 8081 --path ./my_chroma_data & 
P1=$!
python app.py & # your second application
P2=$!
wait $P1 $P2
