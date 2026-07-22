from langchain_huggingface import HuggingFaceEmbeddings


# Load model only once when this file is imported
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
    model_kwargs={
        "device": "cpu"
    },
    encode_kwargs={
        "normalize_embeddings": True
    }
)


def get_embeddings():
    return embeddings