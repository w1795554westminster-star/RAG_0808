import os
import sys
import argparse
import pandas as pd

# Add src directory to python path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from bm25_retriever import BM25Retriever
from dense_retriever import DenseRetriever
from hybrid_retriever import HybridRetriever

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(description="Hybrid Search (BM25 + Dense RRF) for Buổi 14")
    parser.add_argument("--query", "-q", type=str, required=True, help="Truy vấn tìm kiếm")
    parser.add_argument("--top-k", "-k", type=int, default=5, help="Số kết quả đầu ra (mặc định: 5)")
    parser.add_argument("--candidate-k", "-c", type=int, default=20, help="Số ứng viên lấy từ mỗi retriever (mặc định: 20)")
    args = parser.parse_args()

    corpus_csv = os.path.join(base_dir, "data", "processed", "chunks_normalized.csv")
    if not os.path.exists(corpus_csv):
        print(f" Lỗi: Không tìm thấy file corpus tại {corpus_csv}")
        print("Vui lòng chạy 'python scripts/prepare_corpus.py' trước.")
        sys.exit(1)

    df_corpus = pd.read_csv(corpus_csv, dtype=str)
    print(f" Loaded corpus ({len(df_corpus)} chunks) from {corpus_csv}")
    print(f" QUERY: '{args.query}' (top_k={args.top_k}, candidate_k={args.candidate_k})\n")

    # Initialize retrievers
    bm25_engine = BM25Retriever(df_corpus)
    dense_engine = DenseRetriever(df_corpus)
    hybrid_engine = HybridRetriever(bm25_engine, dense_engine, rrf_k=60)

    results = hybrid_engine.search(args.query, top_k=args.top_k, candidate_k=args.candidate_k)

    print("=" * 85)
    print(" HYBRID RESULTS (BM25 + Dense RRF Fusion)")
    print("=" * 85)
    header = f"{'Rank':<5} | {'Chunk ID':<22} | {'BM25 rank':<10} | {'Dense rank':<10} | {'RRF Score':<10} | {'Citation'}"
    print(header)
    print("-" * 85)

    for r in results:
        b_rank_str = str(r['bm25_rank'])
        d_rank_str = str(r['dense_rank'])
        rrf_str = f"{r['rrf_score']:.6f}"
        cit_snippet = r['citation']
        if len(cit_snippet) > 40:
            cit_snippet = cit_snippet[:37] + "..."
        print(f"{r['final_rank']:<5} | {r['chunk_id']:<22} | {b_rank_str:<10} | {d_rank_str:<10} | {rrf_str:<10} | {cit_snippet}")

    print("=" * 85 + "\n")

    print(" CHI TIẾT NỘI DUNG TOP KẾT QUẢ:")
    for r in results:
        print(f"\n--- [Rank #{r['final_rank']}] {r['chunk_id']} (RRF: {r['rrf_score']:.6f}) ---")
        print(f"BM25 Rank: {r['bm25_rank']} | Dense Rank: {r['dense_rank']}")
        print(f"Citation : {r['citation']}")
        snippet = r['text'].replace('\n', ' ')
        if len(snippet) > 200:
            snippet = snippet[:200] + "..."
        print(f"Text     : {snippet}")
    print("=" * 85 + "\n")

if __name__ == "__main__":
    main()
