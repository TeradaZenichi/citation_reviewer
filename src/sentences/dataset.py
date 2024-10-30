import re

def extract_sentences_with_citations(text):
    # Padrão para identificar citações comuns
    citation_patterns = [
        r"\b[A-Z][a-z]+ et al\.,? \d{4}",      # Ex: "Autor et al., 2021"
        r"\b[A-Z][a-z]+,? \d{4}",              # Ex: "Autor, 2021" ou "Autor 2021"
        r"\b[A-Z][a-z]+ & [A-Z][a-z]+,? \d{4}",  # Ex: "Autor & Autor, 2021"
        r"\[\d+\]",                            # Ex: "[1]"
        r"\b[A-Z][a-z]+(?:, [A-Z][a-z]+)* \(\d{4}\)",  # Ex: "Autor1, Autor2 (2021)" ou "Autor (2021)"
    ]
    combined_pattern = "|".join(citation_patterns)
    
    # Divide o texto em frases usando delimitadores comuns (., ?, !)
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences_with_citations = []

    # Procura por citações em cada frase
    for sentence in sentences:
        if re.search(combined_pattern, sentence):
            sentences_with_citations.append(sentence.strip())
    
    return sentences_with_citations