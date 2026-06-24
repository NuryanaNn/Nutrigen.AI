from fastembed import TextEmbedding

MODEL_NAME = "BAAI/bge-small-en-v1.5"

embedding_model = TextEmbedding(
    model_name=MODEL_NAME
)

def get_embedding_chat(text):

    embedding = next(
        embedding_model.embed([text])
    )

    return embedding.tolist()

def preprocess_text(text: str) -> str:
    return "Represent this sentence for retrieval: " + text

def get_embedding_knowledge(text: str):

    processed_text = preprocess_text(text)

    # fastembed returns generator → take first vector
    embedding = next(embedding_model.embed([processed_text]))

    return embedding.tolist()
