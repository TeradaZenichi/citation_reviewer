import re


def extract_sentences_with_citation(text, citation_pattern):
    """
    Extract sentences containing the citation pattern.

    Args:
        text (str): Input text to search
        citation_pattern (str): Regex pattern to match
        n (int, optional): Maximum number of sentences to return. If None, returns all matches

    Returns:
        list: List of sentences containing the citation pattern
    """
    # Split text into sentences (basic splitting on periods followed by spaces)
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Compile the regex pattern
    pattern = re.compile(citation_pattern)

    # Find all sentences that contain the pattern
    matching_sentences = [
        sentence for sentence in sentences
        if pattern.search(sentence)
    ]

    return matching_sentences


if __name__ == "__main__":
    # Example text
    text = """1. Introduction Many recent empirical breakthroughs in supervised machine learning have been achieved through the application of deep neural networks. Network depth (referring to the number of successive computation layers) has played perhaps the most important role in these successes. For instance, the top-5 image classification accuracy on the 1000-class ImageNet dataset has increased from ∼84% (Krizhevsky et al., 2012) to ∼95% (Szegedy et al., 2014; Simonyan & Zisserman, 2014) through the use of ensembles of deeper architectures and smaller receptive fields (Ciresan et al., 2011a;b; 2012) in just a few years."""

    # Citation pattern
    # citation_pattern = r'Krizhevsky et al\.,? \Q2012\E'
    # citation_pattern = r'Krizhevsky et al\.,?\s*2012'
    citation_pattern = 'Krizhevsky et al\\.'

    # Extract the sentence
    result = extract_sentences_with_citation(text, citation_pattern)
    print(result)
