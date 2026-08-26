import os
import sys
import json
import pandas as pd

# Add parent directory and buoi_16 to path
current_dir = os.path.dirname(os.path.abspath(__file__))
buoi17_dir = os.path.dirname(current_dir)
base_dir = os.path.dirname(buoi17_dir)

buoi16_path = os.path.join(base_dir, "buoi_16")
if buoi16_path not in sys.path:
    sys.path.insert(0, buoi16_path)

from src.secure_retriever import SecureRetriever, is_role_authorized

class SecureRetrievalAdapter:
    """
    Adapter pattern wrapper around Buổi 16 SecureRetriever.
    Does NOT implement new search algorithms.
    Standardizes output format into clean, uniform schema for Buổi 17.
    """
    def __init__(self, csv_path: str = None):
        if csv_path is None:
            csv_path = os.path.join(base_dir, "buoi_16", "data", "processed", "chunks_secure.csv")
            if not os.path.exists(csv_path):
                csv_path = os.path.join(buoi17_dir, "data", "chunks_combined_secure.csv")
                
        self.csv_path = csv_path
        self.df_corpus = pd.read_csv(self.csv_path, dtype=str)
        self.retriever = SecureRetriever(self.df_corpus)

    def retrieve(self, question: str, user_roles: list, method: str = "hybrid_rerank", top_k: int = 5, candidate_k: int = 20) -> dict:
        """
        Unified retrieval call wrapper.
        Returns dict containing:
          - query: str
          - user_roles: list
          - total_corpus_size: int
          - authorized_corpus_size: int
          - total_filtered_out: int
          - results: list of standardized chunk dicts
        """
        raw_results, total_filtered_out = self.retriever.retrieve(
            question=question,
            user_roles=user_roles,
            method=method,
            top_k=top_k,
            candidate_k=candidate_k
        )

        standardized_results = []
        for idx, item in enumerate(raw_results, start=1):
            chunk_id = item.get('chunk_id', '')
            
            # Lookup row metadata in df_corpus for fields like title, article
            matched_rows = self.df_corpus[self.df_corpus['chunk_id'] == chunk_id]
            if not matched_rows.empty:
                row = matched_rows.iloc[0]
                title = str(row.get('title', 'N/A'))
                article = str(row.get('article', 'N/A'))
                so_ky_hieu = str(row.get('so_ky_hieu', ''))
            else:
                title = item.get('title', 'N/A')
                article = item.get('article', 'N/A')
                so_ky_hieu = ''

            # Generate or preserve citation
            citation = item.get('citation')
            if not citation or citation == 'N/A':
                doc_id = item.get('document_id', '')
                citation = f"[{title} | {so_ky_hieu} | {article} | {chunk_id}]"

            # Standardize roles format
            allowed_roles_raw = item.get('allowed_roles', [])
            if isinstance(allowed_roles_raw, str):
                try:
                    allowed_roles = json.loads(allowed_roles_raw)
                except Exception:
                    allowed_roles = [allowed_roles_raw]
            else:
                allowed_roles = list(allowed_roles_raw)

            standardized_item = {
                'rank': item.get('rank', idx),
                'chunk_id': chunk_id,
                'document_id': item.get('document_id', ''),
                'title': title,
                'article': article,
                'citation': citation,
                'allowed_roles': allowed_roles,
                'access_decision': 'GRANTED',
                'retrieval_method': item.get('retrieval_method', method),
                'text': item.get('text', ''),
                'score': item.get('score', 0.0)
            }
            standardized_results.append(standardized_item)

        auth_size = len(self.df_corpus) - total_filtered_out

        return {
            'query': question,
            'user_roles': user_roles,
            'total_corpus_size': len(self.df_corpus),
            'authorized_corpus_size': auth_size,
            'total_filtered_out': total_filtered_out,
            'results': standardized_results
        }

if __name__ == '__main__':
    print("Testing SecureRetrievalAdapter...")
    adapter = SecureRetrievalAdapter()
    res = adapter.retrieve("quy định vận chuyển tiền mặt", user_roles=['HR'], top_k=2)
    print(f"Query: {res['query']}")
    print(f"Roles: {res['user_roles']}")
    print(f"Results count: {len(res['results'])}")
    if res['results']:
        print("Sample standardized output keys:", list(res['results'][0].keys()))
        print("Sample item:", res['results'][0])
