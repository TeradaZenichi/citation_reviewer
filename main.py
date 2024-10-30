import src.sentences.get_dataset as dataset_sentences
import src.sentences.dataset as sentences
import src.sentences.get_llm as llm_sentences
from src.apis import check
import pandas as pd
import json

filename = "dataset/combined_papers.json"

#read data in dataset\combined_papers.json
with open(filename, "r", encoding="utf-8") as f:
    papers = json.load(f)

#extract the first paper
paper = papers[0]

text = paper["metadata"]["sections"]           # Texto completo do paper que vamos analisar
references = paper["metadata"]["references"]   # dicionário de referências do paper

# references, report = check.fill(references)

# #convert report dict to DataFrame
# report_df = pd.DataFrame(report)

# # save the report to a csv file - transposed
# report_df.T.to_csv("report.csv")

# data = sentences.extract_sentences_with_citations(text)

references = dataset_sentences.extract(text, references)



print("end of program")