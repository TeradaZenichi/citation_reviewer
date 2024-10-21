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

print('End of the program')
