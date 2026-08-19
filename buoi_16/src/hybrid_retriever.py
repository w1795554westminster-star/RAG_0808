import pandas as pd
from bm25_retriever import BM25Retriever
from dense_retriever import DenseRetriever

class HybridRetriever:
    def __init__(self, bm25_retriever: BM25Retriever, dense_retriever: DenseRetriever, rrf_k: int = 60):
        self.bm25_retriever = bm25_retriever
        self.dense_retriever = dense_retriever
        self.rrf_k = rrf_k
        self.df = bm25_retriever.df

    def search(self, query: str, top_k: int = 5, candidate_k: int = 20) -> list:
        """
        Executes Hybrid Search combining BM25 and Dense retrieval via Reciprocal Rank Fusion (RRF).
        """
        # Fetch candidate lists
        bm25_candidates = self.bm25_retriever.search(query, top_k=candidate_k)
        dense_candidates = self.dense_retriever.search(query, top_k=candidate_k)

        # Index candidates by chunk_id
        bm25_map = {item['chunk_id']: (item['rank'], item) for item in bm25_candidates}
        dense_map = {item['chunk_id']: (item['rank'], item) for item in dense_candidates}

        all_chunk_ids = set(bm25_map.keys()).union(set(dense_map.keys()))
        fused_scores = []

        for c_id in all_chunk_ids:
            b_tuple = bm25_map.get(c_id)
            d_tuple = dense_map.get(c_id)

            b_rank = b_tuple[0] if b_tuple else None
            d_rank = d_tuple[0] if d_tuple else None

            # RRF Score Calculation
            score_bm25 = (1.0 / (self.rrf_k + b_rank)) if b_rank is not None else 0.0
            score_dense = (1.0 / (self.rrf_k + d_rank)) if d_rank is not None else 0.0
            total_rrf_score = score_bm25 + score_dense

            # Get item payload from whichever retriever found it
            item = b_tuple[1] if b_tuple else d_tuple[1]

            fused_scores.append({
                'chunk_id': c_id,
                'document_id': item['document_id'],
                'bm25_rank': b_rank if b_rank is not None else "N/A",
                'dense_rank': d_rank if d_rank is not None else "N/A",
                'rrf_score': round(total_rrf_score, 6),
                'text': item['text'],
                'citation': item['citation']
            })

        # Sort candidates by RRF score descending
        fused_scores.sort(key=lambda x: x['rrf_score'], reverse=True)

        # Assign final rank
        final_results = []
        for rank_idx, res in enumerate(fused_scores[:top_k], 1):
            res['final_rank'] = rank_idx
            final_results.append({
                'final_rank': rank_idx,
                'chunk_id': res['chunk_id'],
                'document_id': res['document_id'],
                'bm25_rank': res['bm25_rank'],
                'dense_rank': res['dense_rank'],
                'rrf_score': res['rrf_score'],
                'text': res['text'],
                'citation': res['citation']
            })

        return final_results
