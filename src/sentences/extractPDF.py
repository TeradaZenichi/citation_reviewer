from pydantic import BaseModel
from openai import OpenAI
from typing import Optional
from pypdf import PdfReader

client = OpenAI()

system_prompt_pdf = """
You are an expert at structured data extraction. 
You will be given unstructured text from a research paper and your task is convert it into the given structure.

Body field: is the main body of the research paper from the introduction to the conclusion.

Begin extracting now!\n\n
"""


class ResearchPaperExtraction(BaseModel):
    title: str
    author: list[str]
    abstract: str
    body: str


def readPDF(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text()
    return pdf_text


def paper_extraction(path_pdf: str) -> ResearchPaperExtraction:
    pdf_text = readPDF(path_pdf)
    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt_pdf},
            {"role": "user", "content": pdf_text}
        ],
        response_format=ResearchPaperExtraction,
    )
    return completion.choices[0].message.parsed


if __name__ == "__main__":
    path_pdf = "F:\\IA024_Projeto\\citation_reviewer\\dataset\\1-s2.0-S0360544224031608-main.pdf"
    paper = paper_extraction(path_pdf)
    print(
        f"\n\nTitle:{paper.title} Abstract: {paper.abstract} \n\nBody: {paper.body} ")
    print("End of program")
