import json

with open('dataset/accepted_papers.json', "r", encoding="utf-8") as f:
    accepted = json.load(f)

with open('dataset/rejected_papers.json', "r", encoding="utf-8") as f:
    rejected = json.load(f)


print("fim do programa")