import PyPDF2



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