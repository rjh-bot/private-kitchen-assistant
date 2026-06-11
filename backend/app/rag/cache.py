import time
import json
import hashlib

class MemoryCache:
    """L1 内存缓存"""
    def __init__(self, ttl: int = 3600):
        self._store: dict[str, tuple[float, str]] = {}
        self.ttl = ttl

    def get(self, key: str) -> str | None:
        data = self._store.get(key)
        if data:
            ts, val = data
            if time.time() - ts < self.ttl:
                return val
            del self._store[key]
        return None

    def set(self, key: str, value: str):
        self._store[key] = (time.time(), value)

class VectorCache:
    """L2 向量缓存 (简化版，基于关键词匹配)"""
    def __init__(self, ttl: int = 7200):
        self._store: dict[str, tuple[float, list]] = {}
        self.ttl = ttl

    def get(self, query: str) -> list | None:
        # 分词后找缓存中的高相似度结果
        q_words = set(query.lower().split())
        best_score = 0.0
        best_result = None
        now = time.time()
        for k, (ts, val) in self._store.items():
            if now - ts > self.ttl:
                continue
            k_words = set(k.lower().split())
            if len(q_words) == 0:
                continue
            score = len(q_words & k_words) / len(q_words | k_words)
            if score > best_score and score > 0.3:
                best_score = score
                best_result = val
        return best_result

    def set(self, query: str, results: list):
        self._store[query] = (time.time(), results)

class CacheManager:
    def __init__(self):
        self.l1 = MemoryCache(ttl=3600)   # 精确匹配
        self.l2 = VectorCache(ttl=7200)   # 语义近似

    def get(self, query: str) -> str | list | None:
        key = hashlib.md5(query.encode()).hexdigest()
        # L1 尝试
        result = self.l1.get(key)
        if result is not None:
            return json.loads(result)
        # L2 尝试
        result = self.l2.get(query)
        return result

    def set(self, query: str, data):
        key = hashlib.md5(query.encode()).hexdigest()
        self.l1.set(key, json.dumps(data, ensure_ascii=False))
        self.l2.set(query, data)
