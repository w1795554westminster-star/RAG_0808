import re
import pandas as pd
from rank_bm25 import BM25Okapi

def tokenize_vietnamese_legal(text: str) -> list:
    """
    Tokenizes Vietnamese legal text while preserving:
    - Legal document numbers (e.g., 01/2014/tt-nhnn, 67/2011/qh12)
    - Article & Chapter designations (e.g., điều 1, điều_1, chương i, mục 2)
    - Vietnamese domain words & numbers
    """
    if not text:
        return []
    text_lower = text.lower()
    # Extract terms, numbers, and document codes
    raw_tokens = re.findall(
        r'[a-z0-9àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]+(?:[\/\.\-][a-z0-9àáảãạăắằẳẵặâấầẩẫậèéẻẽẹêếềểễệìíỉĩịòóỏõọôốồổỗộơớờởỡợùúủũụưứừửữựỳýỷỹỵđ]+)*',
        text_lower
    )
    tokens = list(raw_tokens)
    # Add bigrams for legal structural anchors ('điều 1' -> 'điều_1')
    for i in range(len(raw_tokens) - 1):
        if raw_tokens[i] in ['điều', 'chương', 'mục', 'khoản', 'điểm']:
            tokens.append(f"{raw_tokens[i]}_{raw_tokens[i+1]}")
    return tokens

class BM25Retriever:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        # Build tokenized corpus from title, article, clause, and text
        self.corpus_texts = []
        for _, row in self.df.iterrows():
            combined = f"{row.get('title', '')} {row.get('so_ky_hieu', '')} {row.get('article', '')} {row.get('clause', '')} {row.get('text', '')}"
            self.corpus_texts.append(combined)
            
        print(" Tokenizing corpus for BM25...")
        self.tokenized_corpus = [tokenize_vietnamese_legal(t) for t in self.corpus_texts]
        print(f" BM25 Index ready for {len(self.tokenized_corpus)} chunks.")
        self.bm25 = BM25Okapi(self.tokenized_corpus)

    def search(self, query: str, top_k: int = 5) -> list:
        query_tokens = tokenize_vietnamese_legal(query)
        scores = self.bm25.get_scores(query_tokens)
        
        # Get top-k indices
        top_indices = scores.argsort()[::-1][:top_k]
        
        results = []
        for rank_idx, idx in enumerate(top_indices, 1):
            score = float(scores[idx])
            row = self.df.iloc[idx]
            
            # Format real citation
            so_kh = str(row.get('so_ky_hieu', '')) if pd.notna(row.get('so_ky_hieu')) else ''
            art = str(row.get('article', '')) if pd.notna(row.get('article')) else ''
            cl = str(row.get('clause', '')) if pd.notna(row.get('clause')) else ''
            title = str(row.get('title', '')) if pd.notna(row.get('title')) else ''
            c_id = str(row.get('chunk_id', '')) if pd.notna(row.get('chunk_id')) else ''
            
            citation_parts = []
            if title and title != 'nan':
                citation_parts.append(title)
            if so_kh and so_kh != 'nan':
                citation_parts.append(f"Số: {so_kh}")
            if art and art != 'nan':
                citation_parts.append(art)
            if cl and cl != 'nan':
                citation_parts.append(cl)
            citation_parts.append(c_id)
            
            citation_str = f"[{' | '.join(citation_parts)}]"
            
            results.append({
                'rank': rank_idx,
                'chunk_id': c_id,
                'document_id': row.get('document_id', ''),
                'text': row.get('text', ''),
                'retrieval_score': round(score, 4),
                'retrieval_method': 'BM25',
                'citation': citation_str
            })
            
        return results
