import json
import re

# Função para remover as marcações de bloco de código (```json e similares)
def remove_code_block_markers(json_string):
    # Remover as marcações como ```json
    return re.sub(r'```[a-zA-Z]*\n|```', '', json_string)

# Função para remover quebras de linha e outros caracteres desnecessários
def remove_newline_and_escape(json_string):
    # Substituir \n por quebras de linha reais
    json_string = json_string.replace('\\n', '\n')
    
    # Substituir \" por aspas reais
    json_string = json_string.replace('\\"', '"')
    
    # Substituir \\ por uma barra invertida real
    json_string = json_string.replace('\\\\', '\\')
    
    return json_string

# Função para validar e converter a string JSON em um dicionário Python
def convert_to_dict(json_string):
    try:
        # Tentar converter a string formatada para um dicionário
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Erro ao converter string em dicionário: {e}")
        return None

# Função principal que combina todas as operações
def format_json_string(raw_json_string):
    # 1. Remover as marcações de bloco de código
    cleaned_json = remove_code_block_markers(raw_json_string)
    
    # 2. Remover quebras de linha e caracteres de escape
    formatted_json = remove_newline_and_escape(cleaned_json)
    
    # 3. Converter a string formatada em um dicionário Python
    json_dict = convert_to_dict(formatted_json)
    
    return json_dict

if __name__ == "__main__":
    # Exemplo de uso com a string JSON dada
    raw_json = '''```json\n{\n  "title": "The Influence of ChatGPT on Student Learning and Academic Performance",\n  "paper_source": "2023 International Conference on Computer and Applications (ICCA)",\n  "authors": [\n    {\n      "name": "Shehab Eldeen Ayman",\n      "affiliation": "Faculty of Informatics and Computer Science, The British University In Egypt"\n    },\n    {\n      "name": "Samir A. El-Seoud",\n      "affiliation": "Faculty of Informatics and Computer Science, The British University In Egypt"\n    },\n    {\n      "name": "Khaled Nagaty",\n      "affiliation": "Faculty of Informatics and Computer Science, The British University In Egypt"\n    },\n    {\n      "name": "Omar H. Karam",\n      "affiliation": "Faculty of Informatics and Computer Science, The British University In Egypt"\n    }\n  ],\n  "abstract": "This study delves into the integration of ChatGPT, an artificial intelligence-driven language model, within undergraduate education...",\n  "references": [\n    {\n      "title": "ChatGPT: A comprehensive review on background, applications, key challenges, bias, ethics, limitations and future scope",\n      "authors": "P. P. Ray",\n      "year": "2023",\n      "source": "Internet of Things and Cyber-Physical Systems"\n    },\n    {\n      "title": "ChatGPT is not all you need. A State of the Art Review of large Generative AI models",\n      "authors": "R. Gozalo-Brizuela and E. C. Garrido-Merchan",\n      "year": "2023",\n      "source": "arXiv"\n    }\n  ]\n}\n```'''

    # Formatando a string e convertendo em dicionário
    formatted_dict = format_json_string(raw_json)

    # Verificando o resultado final
    if formatted_dict:
        print(formatted_dict)
