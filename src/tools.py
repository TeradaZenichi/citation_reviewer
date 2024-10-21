import PyPDF2
import re


# Função para extrair o texto de um PDF
def pdf_to_text(pdf_path):
    try:
        # Abrir o arquivo PDF
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""

            # Extrair texto de cada página do PDF
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n"

            return text.strip()  # Retornar o texto extraído
    except Exception as e:
        print(f"Erro ao ler o PDF: {e}")
        return None


def identify_reference_section(text):
    # Pattern to match common reference section headers
    # header_pattern = r'\n(?:References|Bibliography|REFRENCES)\s*\n'
    header_pattern = r'\n(.*)\bReferences|Bibliography|REFRENCES\b\s*\n'

    # Find the start of the reference section
    match = re.search(header_pattern, text, re.IGNORECASE)
    if not match:
        return "Reference section not found."

    start_index = match.start()

    # Extract the text from the start of the reference section to the end
    reference_text = text[start_index:]

    # Optional: If there is an appendix section after references, stop extracting there
    # You can add more stop keywords as necessary
    appendix_stop = re.search(r'(?i)\b(appendix|appendices)\b', reference_text)

    if appendix_stop:
        end_pos = appendix_stop.start()
        reference_text = reference_text[:end_pos]

    return reference_text.strip()


def extract_reference(text, reference_number):
    # Find sentences containing the reference number
    pattern = r'([^.]*?\[' + str(reference_number) + r'\][^.]*\.)'
    matches = re.findall(pattern, text)
    # If no matches found, return "not found"
    if not matches:
        return "not found"

    return matches
