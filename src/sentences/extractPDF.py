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

system_prompt_references = """
You are an expert in extracting structured references from academic research papers.
You will search the reference section of a research paper, and your task is to extract
each reference in a structured format.
In-Text Citation Field: Locate the format of the in-text citation,
as it appears in the document to retrieve this information.

Begin extracting references now!\n\n
"""

system_prompt_sentences = f"""
You are skilled at locating sentences that contain specific in-text citations within academic papers.
You will be provided with an in-text citation and your task is to search the entire document to find and
extract complete sentences that include this citation (be carefully with multiple citations).
Complete the next steps:
step 1: Scan the document for the provided in-text citation, ensuring that you capture each complete sentence where the citation appears.
step 2: Include the surrounding sentence if it provides additional context relevant to the citation.
step 3: Present each extracted sentences in a StructureSentences.

Here in-text citations:
"""


class ResearchPaperExtraction(BaseModel):
    title: str
    author: list[str]
    abstract: str
    body: str


class PaperReferencesExtraction(BaseModel):
    id: int
    title: str
    author: list[str]
    year: str
    doi: Optional[str]
    in_text_citation: str


class StructureReferences(BaseModel):
    reference: list[PaperReferencesExtraction]


class SentenceExtraction(BaseModel):
    id: int
    in_text_citation: str
    sentence: list[str]


class StructureSentences(BaseModel):
    sentences: list[SentenceExtraction]


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
        temperature=0
    )
    return completion.choices[0].message.parsed


def paper_extract_references(pdf_text: str) -> StructureReferences:
    # pdf_text = readPDF(path_pdf)
    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt_references},
            {"role": "user", "content": pdf_text}
        ],
        response_format=StructureReferences,
        temperature=0
    )
    return completion.choices[0].message.parsed


def promp_search_sentences(references: list[PaperReferencesExtraction]):
    prompt = system_prompt_sentences
    for ref in references:
        prompt += f"{ref.id}: {ref.in_text_citation}\n"
    prompt += "\nBegin locating the sentences with the provided in-text citation!\n\n"
    return prompt


def paper_extract_sentences(pdf_text: str, references: list[PaperReferencesExtraction]):
    # pdf_text = readPDF(path_pdf)
    prompt = promp_search_sentences(references)
    completion = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": pdf_text}
        ],
        response_format=StructureSentences,
        temperature=0
    )
    return completion.choices[0].message.parsed


def extract_references_metadata(path_pdf: str):
    pdf_text = readPDF(path_pdf)
    references = paper_extract_references(pdf_text)
    sentences = paper_extract_sentences(pdf_text, references.reference)
    # Convert references to a dictionary
    my_references = references.model_dump()
    my_references = my_references["reference"]

    # Merge references with sentences
    for ref in my_references:
        ref["sentence"] = [""]
        for sentence in sentences.sentences:
            if ref['id'] == sentence.id or ref['in_text_citation'] == sentence.in_text_citation:
                # Add sentences field to references
                ref['sentence'] = sentence.sentence

    return my_references


if __name__ == "__main__":
    path_pdf = "F:\\IA024_Projeto\\citation_reviewer\\dataset\\1-s2.0-S0360544224031608-main.pdf"
    # paper = paper_extraction(path_pdf)
    # print(f"\n\nTitle:{paper.title} Abstract: {paper.abstract} \n\nBody: {paper.body} ")

    my_references = extract_references_metadata(path_pdf)
    print(f"Number of citations: {len(my_references)}\n")
    for ref in my_references:
        print(f"ID: {ref['id']}\nTitle: {ref['title']}\nAuthor: {ref['author']}\nYear: {ref['year']}\nDOI: {ref['doi']}\nIn-text citation: {ref['in_text_citation']}\nSentences: {ref['sentence']}\n\n")

    print("End of program")
