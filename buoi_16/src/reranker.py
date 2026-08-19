import re
import pandas as pd

class Reranker:
    def __init__(self, model_name: str = "cross-encoder/mmarco-mMiniLMv2-L6-H384-v1"):
        self.model_name = model_name
        self.use_neural = False
        self.cross_encoder = None
        
        # Check environment for PyTorch & SentenceTransformers CrossEncoder
        try:
            from sentence_transformers import CrossEncoder
            print(f" Checking Neural Cross-Encoder availability for model: {self.model_name}...")
            self.cross_encoder = CrossEncoder(self.model_name, max_length=512)
            self.use_neural = True
            print(f" Successfully loaded Neural Cross-Encoder: {self.model_name}")
        except Exception as e:
            print(f" [FALLBACK RERANKER MODE]: Không thể load Neural Cross-Encoder ({e}).")
            print(" Chuyển sang dùng Exact Lexical-Semantic Alignment Reranker (FALLBACK RERANKER).")
            print(" Ghi chú: Đây là thuật toán Fallback để demo pipeline, KHÔNG PHẢI Neural Cross-Encoder.")
            self.use_neural = False

    def _fallback_score(self, query: str, candidate: dict) -> float:
        """
        Calculates exact phrase match, legal article anchor density, and term coverage score for Fallback mode.
        """
        q_lower = query.lower()
        text_lower = (candidate['text'] + " " + candidate['citation']).lower()
        
        # 1. Exact legal code match (e.g., '01/2014/tt-nhnn', 'điều 4')
        exact_score = 0.0
        codes = re.findall(r'\d+/\d+/[a-z\-]+|\bđiều\s+\d+\b', q_lower)
        for code in codes:
            if code in text_lower:
                exact_score += 1.5
                
        # 2. Term overlap ratio
        q_words = set(re.findall(r'\w+', q_lower))
        t_words = set(re.findall(r'\w+', text_lower))
        overlap_count = len(q_words.intersection(t_words))
        overlap_ratio = overlap_count / max(len(q_words), 1)
        
        # 3. Base RRF contribution
        rrf_contrib = candidate.get('rrf_score', 0.0) * 10.0
        
        total_score = exact_score + (overlap_ratio * 2.0) + rrf_contrib
        return round(total_score, 4)

    def rerank(self, query: str, candidates: list, top_k: int = 5) -> list:
        """
        Reranks a candidate list returned by Hybrid Search.
        Input: list of candidates from Hybrid Search.
        Output: reranked top_k list with schema:
                final_rank, chunk_id, document_id, hybrid_rank, hybrid_score, rerank_score, text, citation
        """
        if not candidates:
            return []

        reranked_items = []

        if self.use_neural and self.cross_encoder:
            # Neural Cross-Encoder scoring
            pairs = [[query, item['text'][:1000]] for item in candidates]
            scores = self.cross_encoder.predict(pairs)
            for idx, item in enumerate(candidates):
                reranked_items.append({
                    'chunk_id': item['chunk_id'],
                    'document_id': item['document_id'],
                    'hybrid_rank': item.get('final_rank', idx + 1),
                    'hybrid_score': item.get('rrf_score', 0.0),
                    'rerank_score': round(float(scores[idx]), 4),
                    'text': item['text'],
                    'citation': item['citation'],
                    'rerank_method': 'NEURAL_CROSS_ENCODER'
                })
        else:
            # Fallback Reranker scoring
            for idx, item in enumerate(candidates):
                score = self._fallback_score(query, item)
                reranked_items.append({
                    'chunk_id': item['chunk_id'],
                    'document_id': item['document_id'],
                    'hybrid_rank': item.get('final_rank', idx + 1),
                    'hybrid_score': item.get('rrf_score', 0.0),
                    'rerank_score': score,
                    'text': item['text'],
                    'citation': item['citation'],
                    'rerank_method': 'FALLBACK_RERANKER'
                })

        # Sort by rerank_score descending
        reranked_items.sort(key=lambda x: x['rerank_score'], reverse=True)

        # Build output schema
        final_results = []
        for rank_idx, item in enumerate(reranked_items[:top_k], 1):
            final_results.append({
                'final_rank': rank_idx,
                'chunk_id': item['chunk_id'],
                'document_id': item['document_id'],
                'hybrid_rank': item['hybrid_rank'],
                'hybrid_score': item['hybrid_score'],
                'rerank_score': item['rerank_score'],
                'text': item['text'],
                'citation': item['citation'],
                'rerank_method': item['rerank_method']
            })

        return final_results
