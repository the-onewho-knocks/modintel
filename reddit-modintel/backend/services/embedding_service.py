import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

_model = None
_index = None
_index_texts = []


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def encode(texts: list[str]) -> np.ndarray:
    model = _get_model()
    embeddings = model.encode(texts, convert_to_numpy=True)
    faiss.normalize_L2(embeddings)
    return embeddings


def build_index(embeddings: np.ndarray):
    global _index, _index_texts
    dim = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)
    _index.add(embeddings)
    _index_texts = []


def search(query_vec: np.ndarray, k: int) -> tuple[np.ndarray, np.ndarray]:
    return _index.search(query_vec, k)