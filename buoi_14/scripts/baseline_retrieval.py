import os
import sys
import argparse
import pandas as pd

# Add src to python path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from bm25_retriever import BM25Retriever
from dense_retriever import DenseRetriever

def print_results(results: list, title: str):
    print("=" * 70)
    print(f" {title}")
    print("=" * 70)
    if not results:
        print(" Không tìm thấy kết quả phù hợp.")
        print("=" * 70 + "\n")
        return
        
    for res in results:
        print(f"Rank #{res['rank']} | Score: {res['retrieval_score']:.4f} | Method: {res['retrieval_method']}")
        print(f"Citation : {res['citation']}")
        print(f"Chunk ID : {res['chunk_id']} | Doc ID: {res['document_id']}")
        snippet = res['text'].replace('\n', ' ')
        if len(snippet) > 200:
            snippet = snippet[:200] + "..."
        print(f"Text     : {snippet}")
        print("-" * 70)
    print("\n")

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="Baseline Retrieval (BM25 vs Dense) for Buổi 14")
    parser.add_argument("--query", "-q", type=str, required=True, help="Câu hỏi truy vấn")
    parser.add_argument("--top-k", "-k", type=int, default=5, help="Số lượng kết quả lấy ra (mặc định: 5)")
    args = parser.parse_args()
    
    corpus_csv = os.path.join(base_dir, "data", "processed", "chunks_normalized.csv")
    if not os.path.exists(corpus_csv):
        print(f" Lỗi: Không tìm thấy file corpus tại {corpus_csv}")
        print("Vui lòng chạy 'python scripts/prepare_corpus.py' trước.")
        sys.exit(1)
        
    df_corpus = pd.read_csv(corpus_csv, dtype=str)
    print(f" Loaded corpus ({len(df_corpus)} chunks) from {corpus_csv}\n")
    print(f" QUERY: '{args.query}' (top_k={args.top_k})\n")
    
    # 1. BM25 Retrieval
    bm25_engine = BM25Retriever(df_corpus)
    bm25_results = bm25_engine.search(args.query, top_k=args.top_k)
    print_results(bm25_results, "BM25 RESULTS")
    
    # 2. Dense Retrieval
    dense_engine = DenseRetriever(df_corpus)
    dense_results = dense_engine.search(args.query, top_k=args.top_k)
    print_results(dense_results, "DENSE RESULTS")

if __name__ == "__main__":
    main()
