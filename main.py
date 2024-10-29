from src.apis import check
import json

filename = "dataset/combined_papers.json"

#read data in dataset\combined_papers.json
with open(filename, "r", encoding="utf-8") as f:
    papers = json.load(f)

#extract the first paper
paper = papers[0]

references = paper["metadata"]["references"]

references, report = check.fill(references)

print("end of program")