from src.apis import crossref, openalex, semantic_scholar, arxiv

def fill(references):
    report = {}
    for n, ref in enumerate(references):
        arxiv_metadata    = arxiv.arxiv(ref["title"])
        if arxiv_metadata:
            if arxiv_metadata[0]["title"].lower() == ref["title"].lower():
                references[n]["abstract"] = arxiv_metadata[0]["summary"]
                pdf = arxiv.get_paper_content(ref["title"])
                if pdf:
                    references[n]["full_text"] = pdf["full_text"]
                    report[ref["title"]] = "pdf was found in arxiv"
                    continue
                else:
                    report[ref["title"]] = "pdf was not found in arxiv"
            else:
                report[ref["title"]] = "arxiv title does not match"
                continue
        else:
            report[ref["title"]] = "metadata was not found in arxiv"

        crossref_metadata = crossref.crossref(ref["title"])
        if crossref_metadata:
            if crossref_metadata["title"].lower() == ref["title"].lower():
                references[n]["abstract"] = crossref_metadata["abstract"]
                report[ref["title"]] = "metadata was found in crossref"
                continue
        
        # openalex_metadata = openalex.openalex(ref["title"])
        # if openalex_metadata:
        #     if openalex_metadata[0]["title"].lower() == ref["title"].lower():
        #         references[n]["abstract"] = openalex_metadata[0]["abstract"]
                
        #         report[ref["title"]] = "metadata was found in openalex"
        #         continue
        
        semantic_metadata = semantic_scholar.semantic_scholar(ref["title"])
        if semantic_metadata:
            if semantic_metadata["title"].lower() == ref["title"].lower():
                references[n]["abstract"] = semantic_metadata["abstract"]
                report[ref["title"]] = "metadata was found in semantic_scholar"
                continue
            
        references[n]["abstract"] = ""
        references[n]["full_text"] = ""
        report[ref["title"]] = "metadata was not found"

    return references, report