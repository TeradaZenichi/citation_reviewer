from src.string2json import format_json_string
from src.string2array import extract_array
from src.tools import pdf_to_text
from src.llm import call_gpt
import src.apis as apis



# Exemplo de uso: Extrair o texto de um PDF e passá-lo como contexto
pdf_path = "dataset\\1-s2.0-S0378779624006175-main.pdf"
pdf_text = pdf_to_text(pdf_path)

if pdf_text:
    prompt = "Return the json object containing the references of the paper. Use a dictionary with the keys 'title', 'authors', 'year' and 'source' related with the citation. example \"[1]\": \{\}."
    llm_response = call_gpt(prompt, pdf_text)
    print(llm_response)

response = format_json_string(llm_response)

metadata = apis.crossref(response['title'])

references_metadata = []

sentences = dict()

for item, reference in response['references'].items():
    reference_metadata = apis.crossref(reference['title'])
    references_metadata.append(reference_metadata)
    prompt = f"Return the sentences where the refence {item} is cited in the paper, even if the reference is not explicit like [2] is in [1-3]. Use an array format. If you don't find the reference, return an empty array'."
    response_llm = call_gpt(prompt, pdf_text)
    sentences[item] = extract_array(response_llm)
    print('stop')

prompt = """
Return a json object with the sentence where each citation was used in the paper. 
The key should be the citation number and the value should be an array with the sentences where the citation was used.
Consider the existence of implicit citations like [2] in [1-3].
"""

response_llm = call_gpt(prompt, pdf_text)
citations_sentences = format_json_string(response_llm)

doi = metadata['doi']

print('End of the program')
