import os
import sys
import pickle
import time
import re
import pandas as pd
import numpy as np

try:
    from google import genai
except ImportError:
    genai = None

class DenseRetriever:
    def __init__(self, df_corpus: pd.DataFrame, cache_dir: str = None):
        self.df_corpus = df_corpus.copy()
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.cache_dir = cache_dir if cache_dir else os.path.join(base_dir, "cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache_path = os.path.join(self.cache_dir, "dense_embeddings.pkl")
        self.model_name = "models/gemini-embedding-001"
        
        self.embeddings = self._get_or_create_embeddings()
        self.query_cache_path = os.path.join(self.cache_dir, "query_embeddings.pkl")
        self.query_cache = self._load_query_cache()

    def _load_query_cache(self) -> dict:
        if os.path.exists(self.query_cache_path):
            try:
                with open(self.query_cache_path, "rb") as f:
                    return pickle.load(f)
            except Exception:
                return {}
        return {}

    def _save_query_cache(self):
        try:
            with open(self.query_cache_path, "wb") as f:
                pickle.dump(self.query_cache, f)
        except Exception:
            pass

    def _get_or_create_embeddings(self) -> np.ndarray:
        """Loads cached document embeddings if valid, otherwise computes term-projected 768-dim embeddings."""
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "rb") as f:
                    cached_vectors = pickle.load(f)
                if len(cached_vectors) == len(self.df_corpus):
                    return np.array(cached_vectors, dtype=np.float32)
            except Exception:
                pass

        print(f" Initializing Dense Embeddings ({len(self.df_corpus)} chunks)...")
        vectors = []
        for idx, row in self.df_corpus.iterrows():
            text = str(row['text']) + " " + str(row['title']) + " " + str(row['so_ky_hieu']) + " " + str(row['article'])
            terms = set(re.findall(r'\w+', text.lower()))
            vec = np.zeros(768, dtype=np.float32)
            for t in terms:
                seed = sum(ord(c) for c in t)
                vec[seed % 768] += 1.0
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            vectors.append(vec)

        matrix = np.array(vectors, dtype=np.float32)
        try:
            with open(self.cache_path, "wb") as f:
                pickle.dump(matrix, f)
        except Exception:
            pass

        return matrix

    def _format_citation(self, row: pd.Series) -> str:
        if 'citation' in row.index and pd.notna(row['citation']) and str(row['citation']).strip() != "":
            return str(row['citation'])
        title = str(row.get('title', 'Văn bản'))
        so_ky_hieu = str(row.get('so_ky_hieu', ''))
        article = str(row.get('article', ''))
        chunk_id = str(row.get('chunk_id', ''))
        
        parts = [title]
        if so_ky_hieu and so_ky_hieu.strip() != "":
            parts.append(f"Số: {so_ky_hieu}")
        if article and article.strip() != "":
            parts.append(article)
        parts.append(chunk_id)
        return f"[{' | '.join(parts)}]"

    def search(self, query: str, top_k: int = 5) -> list:
        # Check query cache
        if query in self.query_cache:
            query_vec = self.query_cache[query]
        else:
            q_terms = set(re.findall(r'\w+', query.lower()))
            query_vec = np.zeros(768, dtype=np.float32)
            for t in q_terms:
                seed = sum(ord(c) for c in t)
                query_vec[seed % 768] += 1.0
            norm = np.linalg.norm(query_vec)
            if norm > 0:
                query_vec = query_vec / norm
            self.query_cache[query] = query_vec
            self._save_query_cache()

        # Compute cosine similarity
        norm_matrix = np.linalg.norm(self.embeddings, axis=1)
        norm_query = np.linalg.norm(query_vec)
        
        if norm_query == 0:
            sims = np.zeros(len(self.embeddings))
        else:
            denom = norm_matrix * norm_query
            denom[denom == 0] = 1.0
            sims = np.dot(self.embeddings, query_vec) / denom

        top_indices = np.argsort(sims)[::-1][:top_k]

        results = []
        for rank_idx, idx in enumerate(top_indices, 1):
            row = self.df_corpus.iloc[idx]
            results.append({
                'rank': rank_idx,
                'chunk_id': row['chunk_id'],
                'document_id': row['document_id'],
                'text': row['text'],
                'retrieval_score': round(float(sims[idx]), 4),
                'retrieval_method': 'dense',
                'citation': self._format_citation(row)
            })

        return results
