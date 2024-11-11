from sklearn.metrics import precision_score, recall_score
from sklearn.feature_extraction.text import CountVectorizer

def calculate_precision_recall(reference, response):
    vectorizer = CountVectorizer(binary=True)
    vectors = vectorizer.fit_transform([reference, response])
    ref_vector, res_vector = vectors.toarray()
    
    precision = precision_score(ref_vector, res_vector, zero_division=1)
    recall = recall_score(ref_vector, res_vector, zero_division=1)
    
    return precision, recall


if __name__ == "__main__":
    reference_text = "Zeus is known as the god of the sky and thunder."
    response_text = "Zeus is the ruler of Mount Olympus and god of the sky and thunder."
    precision, recall = calculate_precision_recall(reference_text, response_text)
    print("Precision:", precision)
    print("Recall:", recall)
    a = 1