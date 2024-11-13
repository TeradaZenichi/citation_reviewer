from src.apis import arxivref, crossref, openalex, semantic_scholar

def fill(references):
    report = {}
    
    for n, ref in enumerate(references):
        report[ref["title"]] = {"abstract": None, "pdf": None}      
        references[n]["abstract"] = ""
        references[n]["full_text"] = ""


    for n, ref in enumerate(references):
        print(f"Checking reference {n+1}: {ref['title']}")

        arxiv_metadata    = arxivref.search_by_library(ref["title"])
        if arxiv_metadata:
            if arxiv_metadata["title"].lower() == ref["title"].lower():
                references[n]["abstract"] = arxiv_metadata["summary"]
                pdf = arxivref.download_by_library(arxiv_metadata["id"], filename="my_article.pdf")
                report[ref["title"]]["abstract"] = "arxiv Library"
                if pdf:
                    references[n]["full_text"] = pdf
                    report[ref["title"]]["pdf"] = "arxiv Library"
                continue


        arxiv_metadata    = arxivref.arxivref(ref["title"])
        if arxiv_metadata:
            if arxiv_metadata["title"].lower() == ref["title"].lower():
                references[n]["abstract"] = arxiv_metadata["summary"]
                pdf = arxivref.get_paper_content(ref["title"])
                report[ref["title"]]["abstract"] = "arxiv API"
                if pdf:
                    references[n]["full_text"] = pdf["full_text"]
                    report[ref["title"]]["pdf"] = "arxiv API"
                continue
        
        crossref_metadata = crossref.crossref(ref["title"])
        if crossref_metadata:
            try:
                if crossref_metadata["title"].lower() == ref["title"].lower():
                    references[n]["abstract"] = crossref_metadata["abstract"]
                    report[ref["title"]]["abstract"] = "crossref"
                    continue
            except:
                pass
        
        # semantic_metadata = semantic_scholar.semantic_scholar(ref["title"])
        # if semantic_metadata:
        #     if semantic_metadata["title"].lower() == ref["title"].lower():
        #         references[n]["abstract"] = semantic_metadata["abstract"]
        #         report[ref["title"]]["abstract"] = "semantic_scholar"
                # continue
            
    return references, report


def doi(references ):
    report = {}
    references = []
    references.append({"title": doi})
    references, report = fill(references)
    return references[0], report