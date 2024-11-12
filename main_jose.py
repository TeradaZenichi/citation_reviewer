from src.apis import check
from src.sentences.extract import *
from src.evaluation.metrics import *
import pandas as pd
import json
import src.sentences.get_dataset as dataset_sentences


filename = "dataset/combined_papers.json"
# filename = "dataset/accepted_papers.json"

# read data in dataset\combined_papers.json
with open(filename, "r", encoding="utf-8") as f:
    papers = json.load(f)

# extract the first paper
paper = papers[1]

# Texto completo do paper que vamos analisar
text = paper["metadata"]["sections"]
# dicionário de referências do paper
references = paper["metadata"]["references"]

references = dataset_sentences.extract(
    paper["metadata"]["referenceMentions"], references)

#exemplo de uso da sentença
ref = references[0]
sentence = ref['sentence']

# fazer uma função que cria chunks de text
chunks = create_chunks(text)
# fazer uma função que busca o chunk mais perto da sentence
chunk = faiss(sentence, chunks)

