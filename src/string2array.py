import re

# Função para processar a extração e limpeza
def extract_array(text):
    # Expressão regular para extrair o array
    regex = r'\[(.*?)\]'
    match = re.search(regex, text)
    if match:
        # Divide os elementos com base nas vírgulas e remove espaços extras
        return [item.strip().strip('"').strip("'") for item in match.group(1).split(',')]
    return []