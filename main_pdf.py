from src.sentences import extractPDF
from src.evaluation import calculate
from src.apis import check
import pandas as pd
import json

pdf = "2411.06855v1.pdf"
path_pdf = f"dataset/{pdf}"

references = extractPDF.extract_references_metadata(path_pdf)
print(f"Number of citations: {len(references)}\n")
for ref in references:
    print(f"ID: {ref['id']}\nTitle: {ref['title']}\nAuthor: {ref['author']}\nYear: {ref['year']}\nDOI: {ref['doi']}\nIn-text citation: {ref['in_text_citation']}\nSentences: {ref['sentence']}\n\n")

for ref in references:
    #join all sentences in a single string
    ref['sentence'] = " ".join(ref['sentence'])

refefences, report = check.fill(references)
results = calculate.fill(references, report)

#save references in a json file
with open(f"Results/{pdf}_references.json", "w", encoding="utf-8") as f:
    json.dump(references, f, indent=4)

#convert results dict to DataFrame trasposed
final_df = pd.DataFrame(results).T
final_df.to_csv(f"Results/{pdf}.csv")

print("End of program")

print('fim do programa')