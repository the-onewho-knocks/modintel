import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def check_similarity(target: str, corpus: list[str]) -> list[dict]:
    model = _get_model()
    all_texts = [target] + corpus
    embeddings = model.encode(all_texts, convert_to_numpy=True)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(embeddings)
    index.add(embeddings[1:])

    query_vec = embeddings[0:1]
    faiss.normalize_L2(query_vec)
    scores, indices = index.search(query_vec, len(corpus))

    results = []
    for rank, idx in enumerate(indices[0]):
        results.append({
            "index": int(idx),
            "text": corpus[idx],
            "score": float(scores[0][rank]),
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results