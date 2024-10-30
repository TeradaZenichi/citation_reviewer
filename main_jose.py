from src.apis import check
from src.sentences.extract import *
import pandas as pd
import json

filename = "dataset/combined_papers.json"

# read data in dataset\combined_papers.json
with open(filename, "r", encoding="utf-8") as f:
    papers = json.load(f)

# extract the first paper
paper = papers[0]

# Texto completo do paper que vamos analisar
text = paper["metadata"]["sections"]
# dicionário de referências do paper
references = paper["metadata"]["references"]

# extrair as sentenças que contêm a citação
for refs in references:
    refs["sentences"] = extract_sentences_with_citation(
        text, refs['shortCiteRegEx'])

print(references)

# references, report = check.fill(references)

# convert report dict to DataFrame
# report_df = pd.DataFrame(report)

# save the report to a csv file - transposed
# report_df.T.to_csv("report.csv")

print("end of program")
