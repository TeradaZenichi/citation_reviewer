from src.evaluation import faithfulness
from src.evaluation import precision_recall
from src.evaluation import semantic_similarity

def fill(references, report):
    results = {}
    for i, ref in enumerate(references):
        title = ref['title']
        results[title] = {}
        if title not in report:
            continue
        results[title]['pdf'] = report[title]['pdf']
        if report[title]['abstract'] == None:
            results[title]['abstract'] = None
            results[title]["faithfulness"] = None
            results[title]["precision_recall"] = None
            results[title]["semantic_similarity"] = None
            continue
        results[title]['abstract'] = report[title]['abstract']
        results[title]["faithfulness"] = faithfulness.calculate_faithfulness(
            ref['abstract'], ref['sentence']
        )
        results[title]["precision"], results[title]['recall'] = precision_recall.calculate_precision_recall(
            ref['abstract'], ref['sentence']
        )
        results[title]["semantic_similarity"] = semantic_similarity.calculate_semantic_similarity(
            ref['abstract'], ref['sentence']
        )

  
    return results