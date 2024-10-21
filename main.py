from src.string2json import format_json_string
from src.tools import pdf_to_text
from src.llm import call_gpt
import src.apis as apis



# Exemplo de uso: Extrair o texto de um PDF e passá-lo como contexto
pdf_path = "dataset\The_Influence_of_ChatGPT_on_Student_Learning_and_Academic_Performance.pdf"
pdf_text = pdf_to_text(pdf_path)

if pdf_text:
    prompt = "Return the json object containing the title, paper source, authors, abstract, and the references of the paper. For the references use a sub dictionary with the keys 'title', 'authors', 'year' and 'source'."
    response = call_gpt(prompt, pdf_text)
    print(response)

response = format_json_string(response)

metadata = apis.crossref(response['title'])

references_metadata = []

for reference in response['references']:
    reference_metadata = apis.crossref(reference['title'])
    references_metadata.append(reference_metadata)


doi = metadata['doi']

print('End of the program')
