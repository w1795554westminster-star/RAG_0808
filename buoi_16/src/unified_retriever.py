import os
import sys
import pandas as pd

# Add src to sys.path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from bm25_retriever import BM25Retriever
from dense_retriever import DenseRetriever
from hybrid_retriever import HybridRetriever
from reranker import Reranker

class UnifiedRetriever:
    def __init__(self, df_corpus: pd.DataFrame = None):
        if df_corpus is None:
            corpus_csv = os.path.join(base_dir, "data", "processed", "chunks_normalized.csv")
            if not os.path.exists(corpus_csv):
                raise FileNotFoundError(f"Không tìm thấy corpus tại: {corpus_csv}")
            self.df_corpus = pd.read_csv(corpus_csv, dtype=str)
        else:
            self.df_corpus = df_corpus.copy()

        self.bm25_engine = BM25Retriever(self.df_corpus)
        self.dense_engine = DenseRetriever(self.df_corpus)
        self.hybrid_engine = HybridRetriever(self.bm25_engine, self.dense_engine, rrf_k=60)
        self.reranker_engine = Reranker()

        # Load relationships CSV for Graph Hints fallback
        self.rel_csv_path = os.path.join(base_dir, "..", "kb+hops", "relationships.csv")
        self.df_relationships = None
        if os.path.exists(self.rel_csv_path):
            try:
                self.df_relationships = pd.read_csv(self.rel_csv_path, dtype=str)
            except Exception:
                self.df_relationships = None

    def retrieve(self, question: str, method: str = "hybrid_rerank", top_k: int = 5, candidate_k: int = 20) -> list:
        """
        Unified retrieval function for Buổi 14.
        Supported methods: 'bm25', 'dense', 'hybrid', 'hybrid_rerank'
        Returns list of standardized result dictionaries.
        """
        method = method.lower().strip()
        if method == "bm25":
            raw_results = self.bm25_engine.search(question, top_k=top_k)
            formatted = []
            for item in raw_results:
                formatted.append({
                    'rank': item['rank'],
                    'chunk_id': item['chunk_id'],
                    'document_id': item['document_id'],
                    'text': item['text'],
                    'score': item['retrieval_score'],
                    'citation': item['citation'],
                    'retrieval_method': 'bm25'
                })
            return formatted

        elif method == "dense":
            raw_results = self.dense_engine.search(question, top_k=top_k)
            formatted = []
            for item in raw_results:
                formatted.append({
                    'rank': item['rank'],
                    'chunk_id': item['chunk_id'],
                    'document_id': item['document_id'],
                    'text': item['text'],
                    'score': item['retrieval_score'],
                    'citation': item['citation'],
                    'retrieval_method': 'dense'
                })
            return formatted

        elif method == "hybrid":
            raw_results = self.hybrid_engine.search(question, top_k=top_k, candidate_k=candidate_k)
            formatted = []
            for item in raw_results:
                formatted.append({
                    'rank': item['final_rank'],
                    'chunk_id': item['chunk_id'],
                    'document_id': item['document_id'],
                    'text': item['text'],
                    'score': item['rrf_score'],
                    'citation': item['citation'],
                    'retrieval_method': 'hybrid',
                    'bm25_rank': item['bm25_rank'],
                    'dense_rank': item['dense_rank'],
                    'rrf_score': item['rrf_score']
                })
            return formatted

        elif method == "hybrid_rerank":
            candidates = self.hybrid_engine.search(question, top_k=candidate_k, candidate_k=candidate_k)
            reranked = self.reranker_engine.rerank(question, candidates, top_k=top_k)
            formatted = []
            for item in reranked:
                formatted.append({
                    'rank': item['final_rank'],
                    'chunk_id': item['chunk_id'],
                    'document_id': item['document_id'],
                    'text': item['text'],
                    'score': item['rerank_score'],
                    'citation': item['citation'],
                    'retrieval_method': 'hybrid_rerank',
                    'hybrid_rank': item['hybrid_rank'],
                    'hybrid_score': item['hybrid_score'],
                    'rerank_score': item['rerank_score'],
                    'rerank_method': item.get('rerank_method', 'RERANK')
                })
            return formatted
        else:
            raise ValueError(f"Method '{method}' không hợp lệ. Chọn: 'bm25', 'dense', 'hybrid', 'hybrid_rerank'.")

    def get_graph_hints(self, retrieved_results: list) -> dict:
        """
        Extracts 1-hop direct relationships for retrieved document_ids from relationships.csv or Neo4j.
        """
        doc_ids = list(dict.fromkeys([item['document_id'] for item in retrieved_results if 'document_id' in item]))
        chunk_ids = [item['chunk_id'] for item in retrieved_results if 'chunk_id' in item]

        hints = {
            'retrieved_doc_ids': doc_ids,
            'retrieved_chunk_ids': chunk_ids,
            'direct_relationships': [],
            'source': 'relationships.csv (local fallback)'
        }

        if self.df_relationships is not None and not self.df_relationships.empty:
            matched_rels = self.df_relationships[
                self.df_relationships['source'].isin(doc_ids) | self.df_relationships['target'].isin(doc_ids)
            ]
            
            rel_list = []
            for _, r in matched_rels.head(10).iterrows():
                rel_list.append({
                    'source': r['source'],
                    'relationship': r['relationship_type'],
                    'target': r['target'],
                    'evidence': str(r.get('evidence', 'N/A'))[:80]
                })
            hints['direct_relationships'] = rel_list

        return hints

# Global standalone helper function
def retrieve(question: str, method: str = "hybrid_rerank", top_k: int = 5, candidate_k: int = 20) -> list:
    engine = UnifiedRetriever()
    return engine.retrieve(question, method=method, top_k=top_k, candidate_k=candidate_k)
