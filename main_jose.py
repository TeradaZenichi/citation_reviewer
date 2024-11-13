from src.apis import check
from src.sentences.extract import *
from src.evaluation.metrics import *
from src.rag.citation import *
from src.sentences.extractPDF import *
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

references = paper["metadata"]["references"]

refefences, report = check.fill(references)
# dicionário de referências do paper
references = paper["metadata"]["references"]

references = dataset_sentences.extract(
    paper["metadata"]["referenceMentions"], references)

# exemplo de uso da sentença
ref = references[0]
text = paper["metadata"]["full_text"]
sentence = ref['sentence']


# fazer uma função que cria chunks de text
# Call this fuction one time for each paper
chunks, index = paper_segmentation(text)

# Call this function for each sentence
# fazer uma função que busca o chunk mais perto da sentence
similar_chunk = retrieve_chunk(sentence, chunks, index, k=1)
print(similar_chunk)
