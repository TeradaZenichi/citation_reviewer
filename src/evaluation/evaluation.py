from ragas.metrics import LLMContextRecall, Faithfulness, SemanticSimilarity, FactualCorrectness
from ragas import evaluate, SingleTurnSample, EvaluationDataset
from src.tools.llm import call_gpt

# Importar wrappers necessários
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Definir o LLM e embeddings utilizando wrappers
evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
evaluator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())

# Função de avaliação
def evaluation(references):
    samples = [
        SingleTurnSample(
            user_input=f"Sentence: '{ref['sentence']}'",
            response=ref['sentence'],
            reference=ref['abstract'] if ref['abstract'] else "Abstract não disponível",
            retrieved_contexts=[ref['abstract']] if ref['abstract'] else ["Abstract não disponível"]
        )
        for ref in references  # Ignorar referências sem abstract
    ]
    
    # Verificação para evitar dataset vazio
    if not samples:
        print("Nenhuma referência com abstract disponível para avaliação.")
        return None
    
    eval_dataset = EvaluationDataset(samples=samples)
    metrics = [
        LLMContextRecall(llm=evaluator_llm),
        FactualCorrectness(llm=evaluator_llm),
        Faithfulness(llm=evaluator_llm),
        SemanticSimilarity(embeddings=evaluator_embeddings)
    ]
    
    results = evaluate(dataset=eval_dataset, metrics=metrics)
    return results.to_pandas()

# Exemplo de chamada da função com um conjunto de referências
# references = [{"sentence": "Sua citação aqui.", "abstract": "Abstract do artigo original."}, ...]
# df_results = evaluation(references)
# print(df_results.head())
