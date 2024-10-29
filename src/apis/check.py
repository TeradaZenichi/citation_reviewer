from src.apis import crossref, openalex, semantic_scholar, arxiv

def fill(references):
    report = {}
    
    for n, ref in enumerate(references):
        report[ref["title"]] = {"abstract": None, "pdf": None}      
        references[n]["abstract"] = ""
        references[n]["full_text"] = ""


    for n, ref in enumerate(references):
        print(f"Checking reference {n+1}: {ref['title']}")
        arxiv_metadata    = arxiv.arxiv(ref["title"])
        if arxiv_metadata:
            if arxiv_metadata["title"].lower() == ref["title"].lower():
                references[n]["abstract"] = arxiv_metadata["summary"]
                pdf = arxiv.get_paper_content(ref["title"])
                report[ref["title"]]["abstract"] = "arxiv"
                if pdf:
                    references[n]["full_text"] = pdf["full_text"]
                    report[ref["title"]]["pdf"] = "arxiv"
                continue
        
        crossref_metadata = crossref.crossref(ref["title"])
        if crossref_metadata:
            if crossref_metadata["title"].lower() == ref["title"].lower():
                references[n]["abstract"] = crossref_metadata["abstract"]
                report[ref["title"]]["abstract"] = "crossref"
                continue
        
        semantic_metadata = semantic_scholar.semantic_scholar(ref["title"])
        if semantic_metadata:
            if semantic_metadata["title"].lower() == ref["title"].lower():
                references[n]["abstract"] = semantic_metadata["abstract"]
                report[ref["title"]]["abstract"] = "semantic_scholar"
                continue
            
    return references, report