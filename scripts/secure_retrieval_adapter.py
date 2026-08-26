import os
import sys
import json
import pandas as pd

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
buoi17_dir = os.path.dirname(current_dir) if os.path.basename(current_dir) == "scripts" else current_dir
base_dir = os.path.dirname(buoi17_dir)

buoi16_path = os.path.join(base_dir, "buoi_16")
if os.path.exists(buoi16_path) and buoi16_path not in sys.path:
    sys.path.insert(0, buoi16_path)

def is_role_authorized(allowed_roles_raw, user_roles):
    """
    Checks if any role in user_roles is allowed.
    """
    if "Admin" in user_roles or "Admin" in (user_roles if isinstance(user_roles, list) else [user_roles]):
        return True
    if not allowed_roles_raw:
        return True
    if isinstance(allowed_roles_raw, str):
        try:
            allowed_roles = json.loads(allowed_roles_raw)
        except Exception:
            allowed_roles = [allowed_roles_raw]
    else:
        allowed_roles = list(allowed_roles_raw)
    
    return any(r in allowed_roles for r in user_roles)

try:
    from src.secure_retriever import SecureRetriever
except ImportError:
    class SecureRetriever:
        """Standalone fallback SecureRetriever when buoi_16 is not present (e.g. inside Docker container)."""
        def __init__(self, df_corpus):
            self.df_corpus = df_corpus

        def retrieve(self, question: str, user_roles: list, method: str = "hybrid_rerank", top_k: int = 5, candidate_k: int = 20):
            total_corpus_size = len(self.df_corpus)
            authorized_rows = []
            filtered_out = 0

            for _, row in self.df_corpus.iterrows():
                allowed = row.get("allowed_roles", "[]")
                if is_role_authorized(allowed, user_roles):
                    authorized_rows.append(row.to_dict())
                else:
                    filtered_out += 1

            if not authorized_rows:
                return [], filtered_out

            q_tokens = [w.lower() for w in question.split() if len(w) > 1]
            results = []
            for row in authorized_rows:
                text = str(row.get("text", "")) + " " + str(row.get("title", "")) + " " + str(row.get("citation", ""))
                text_low = text.lower()
                
                score = sum(1.0 for tok in q_tokens if tok in text_low)
                row_dict = dict(row)
                row_dict["score"] = score
                results.append(row_dict)

            results.sort(key=lambda x: x["score"], reverse=True)
            top_results = results[:top_k]
            return top_results, filtered_out


class SecureRetrievalAdapter:
    """
    Adapter pattern wrapper around SecureRetriever.
    Standardizes output format into clean, uniform schema.
    """
    def __init__(self, csv_path: str = None):
        if csv_path is None:
            csv_path = os.path.join(buoi17_dir, "data", "chunks_combined_secure.csv")
            if not os.path.exists(csv_path):
                csv_path = os.path.join(base_dir, "buoi_16", "data", "processed", "chunks_secure.csv")
                
        self.csv_path = csv_path
        self.df_corpus = pd.read_csv(self.csv_path, dtype=str)
        self.retriever = SecureRetriever(self.df_corpus)

    def retrieve(self, question: str, user_roles: list, method: str = "hybrid_rerank", top_k: int = 5, candidate_k: int = 20) -> dict:
        """
        Unified retrieval call wrapper.
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

            citation = item.get('citation')
            if not citation or citation == 'N/A':
                doc_id = item.get('document_id', '')
                citation = f"[{title} | {so_ky_hieu} | {article} | {chunk_id}]"

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
