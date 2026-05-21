from services.embedding_service import encode, search


def check_similarity(target: str, corpus: list[str]) -> list[dict]:
    all_texts = [target] + corpus
    embeddings = encode(all_texts)

    query_vec = embeddings[0:1]
    corpus_embs = embeddings[1:]
    dim = corpus_embs.shape[1]

    import faiss
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(corpus_embs)
    index.add(corpus_embs)

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