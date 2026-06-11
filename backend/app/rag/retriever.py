import json
import numpy as np
from rank_bm25 import BM25Okapi
from app.rag.cache import CacheManager

class RecipeRetriever:
    def __init__(self, recipes: list[dict]):
        self.recipes = recipes
        self.cache = CacheManager()
        # BM25 索引
        corpus = [self._tokenize(r["name"] + " " + r.get("tags", "") + " " + r.get("description", ""))
                  for r in recipes]
        self.bm25 = BM25Okapi(corpus) if corpus else None
        # 简单向量 (基于词袋)
        self.vocab = self._build_vocab(corpus)
        self.vectors = np.array([self._bow(t) for t in corpus]) if corpus else np.array([])

    def _tokenize(self, text: str) -> list[str]:
        import re
        return re.findall(r"[\w\u4e00-\u9fff]+", text.lower())

    def _build_vocab(self, corpus: list[list[str]]) -> dict:
        vocab = {}
        for doc in corpus:
            for w in doc:
                if w not in vocab:
                    vocab[w] = len(vocab)
        return vocab

    def _bow(self, tokens: list[str]) -> list[float]:
        vec = [0.0] * len(self.vocab)
        for w in tokens:
            idx = self.vocab.get(w)
            if idx is not None:
                vec[idx] += 1.0
        return vec

    def _cosine_sim(self, a: np.ndarray, b: np.ndarray) -> float:
        norm = np.linalg.norm(a) * np.linalg.norm(b)
        return float(np.dot(a, b) / norm) if norm > 0 else 0.0

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        # 检查缓存
        cached = self.cache.get(query)
        if cached:
            return cached

        tokens = self._tokenize(query)

        # BM25 分数
        bm25_scores = []
        if self.bm25:
            bm25_scores = self.bm25.get_scores(tokens)

        # 向量相似度
        vec_scores = []
        if len(self.vectors) > 0:
            q_vec = np.array(self._bow(tokens))
            vec_scores = [self._cosine_sim(q_vec, v) for v in self.vectors]

        # 混合评分 (BM25 * 0.5 + 向量 * 0.5)
        scored = []
        for i, recipe in enumerate(self.recipes):
            b = bm25_scores[i] if i < len(bm25_scores) else 0
            v = vec_scores[i] if i < len(vec_scores) else 0
            total = b * 0.5 + v * 0.5
            scored.append((total, recipe))

        scored.sort(key=lambda x: x[0], reverse=True)
        results = [r for _, r in scored[:top_k]]

        # 写入缓存
        self.cache.set(query, results)
        return results
