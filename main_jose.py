from src.string2json import format_json_string
from src.tools import *
from src.llm import call_gpt


# Exemplo de uso: Extrair o texto de um PDF e passá-lo como contexto
pdf_path = "dataset\The_Influence_of_ChatGPT_on_Student_Learning_and_Academic_Performance.pdf"
pdf_text = pdf_to_text(pdf_path)
# Extract the text from the reference section
references_text = identify_reference_section(pdf_text)

prompt = """
Return JSON file structure based on the references provided.
This JSON structure organizes the references with their key details, such as the id, author(s), title, year of publication, journal or publisher, volume, issue, pages and any relevant information.
"""

# if pdf_text:
#    response = call_gpt(prompt, references_text)
#    print(response)

# Read file
with open("dataset\\response.txt", 'r', encoding='utf-8') as file:
    response = file.read()

response = format_json_string(response)
print(response)

# Extract the sentences with REGEX
sentences_regex = extract_reference(pdf_text, response['references'][9]['id'])
print(f"Sentences with REGEX:\n{sentences_regex}")


# Extract the sentences with LLM
prompt_refs = f"""
Extract the sentences that contains the reference [{response['references'][0]['id']}] in provide text and response with a list of sentences.
If the reference is not explicitly found, return "not found".

Use the next text to search the reference:

"""
sentences_llm = call_gpt(prompt_refs, pdf_text)
print(f"Sentences with LLM:\n{sentences_llm}")

print('End of the program')
