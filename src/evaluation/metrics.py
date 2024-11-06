from ragas import SingleTurnSample, EvaluationDataset
from ragas.metrics import Faithfulness, SemanticSimilarity
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from ragas import evaluate
import os
import json

"""
LLMContextRecall,    # user_input, reference and  retrieved_contexts
ContextEntityRecall, # reference and retrieved_contexts
Faithfulness,        # response and retrieved_context.
FactualCorrectness,  # response and reference.
SemanticSimilarity,  # response and ground truth.
BleuScore,           # response and reference
RougeScore,          # response and reference
ExactMatch,          # response and reference
StringPresence,      # response and reference
ResponseRelevancy,   # user_input, retrived_contexts and response
NoiseSensitivity,    # user_input, reference, response, and retrieved_contexts
"""


def citations_dataset(references):
    # Create a list of SingleTurnSample objects
    samples = []
    for ref in references:
        # Joint the sentences that contain the citation
        # sentences = "\n".join(ref["sentence"])
        sentences = ref["sentence"]
        abstract = ref["abstract"]
        # Create a SingleTurnSample object
        sample = SingleTurnSample(
            response=sentences,
            # user_input=sentences,
            # retrieved_contexts=[abstract],
            # response=abstract,
            reference=abstract,
        )
        samples.append(sample)

    return EvaluationDataset(samples)


def calculate_metrics(references):
    # os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY_EMB")

    evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
    evaluator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())

    metrics = [
        # Faithfulness(llm=evaluator_llm),
        SemanticSimilarity(embeddings=evaluator_embeddings)
    ]

    eval_dataset = citations_dataset(references)

    results = evaluate(dataset=eval_dataset, metrics=metrics)

    return results.to_pandas()


if __name__ == "__main__":
    # Load the references from a file
    with open("references.json", "r", encoding="utf-8") as f:
        references = json.load(f)

    # samples = citations_dataset(references)
    # print(samples[0])

    results = calculate_metrics(references)
    print(results)

    # save the results to a csv file
    results.to_csv("results.csv")

    print("end of program")
