def extract(sentence_list, references):
    for n, ref in enumerate(references):
        references[n]["sentence"] = ""

    for sentence in sentence_list:
        ref_id = sentence["referenceID"]
        references[ref_id]["sentence"] += " " + sentence["context"]
    return references