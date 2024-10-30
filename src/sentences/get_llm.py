from src.tools import llm, string2json
import json

def extract(sentence_list, references):
    data = {}
    for ref in references:
        data[ref["title"]] = {
            "authors": ", ".join(ref["author"]),
            "sentences": []
        }
    
    prompt = """
        Complete the json with the sentences are being mentioned in the sentences list."
        Help to extract where the senteces are talking about the references above.
    """
    context = f"consider the following json: \n {json.dumps(data)} \n and the following sentences: \n {sentence_list} "

    llm_data = llm.call_gpt(prompt, context)

    # Parse the data from the LLM
    try:
        llm_data = string2json.format_json_string(llm_data)
    except Exception as e:
        print(f"Error while parsing LLM data: {e}")
        return None 
    
    return llm_data