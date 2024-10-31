import src.evaluation.evaluation as evaluation
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

references, report = check.fill(references)

# #convert report dict to DataFrame
report_df = pd.DataFrame(report)

# # save the report to a csv file - transposed
report_df.T.to_csv("report.csv")

# data = sentences.extract_sentences_with_citations(text)

references = dataset_sentences.extract(paper["metadata"]["referenceMentions"], references)


# save the references to a json file
with open("references.json", "w", encoding="utf-8") as f:
    json.dump(references, f, ensure_ascii=False, indent=4)

# open the references json file
with open("references.json", "r", encoding="utf-8") as f:
    references = json.load(f)


resuls = evaluation.evaluation(references)

#how to remove some columns?
resuls_clean = resuls
resuls_clean.drop(columns=["user_input", "response", "reference", "retrieved_contexts"], inplace=True) 
resuls.to_csv("results.csv")
resuls_clean.to_csv("results_clean.csv")

# join the results_clean with report csv
report_df = pd.read_csv("report.csv")
results_df = pd.read_csv("results_clean.csv")

# use concat to join the two dataframes
final_df = pd.concat([report_df, results_df], axis=1)

final_df.to_csv("final.csv")
print("end of program")