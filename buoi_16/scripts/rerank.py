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
from hybrid_retriever import HybridRetriever
from reranker import Reranker

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(description="Hybrid Search + Reranking for Buổi 14")
    parser.add_argument("--query", "-q", type=str, required=True, help="Truy vấn tìm kiếm")
    parser.add_argument("--top-k", "-k", type=int, default=5, help="Số kết quả hiển thị cuối cùng (mặc định: 5)")
    parser.add_argument("--candidate-k", "-c", type=int, default=20, help="Số ứng viên từ Hybrid Search (mặc định: 20)")
    args = parser.parse_args()

    corpus_csv = os.path.join(base_dir, "data", "processed", "chunks_normalized.csv")
    if not os.path.exists(corpus_csv):
        print(f" Lỗi: Không tìm thấy corpus tại {corpus_csv}")
        sys.exit(1)

    df_corpus = pd.read_csv(corpus_csv, dtype=str)
    print(f" Loaded corpus ({len(df_corpus)} chunks)")
    print(f" QUERY: '{args.query}' (candidate_k={args.candidate_k}, top_k={args.top_k})\n")

    # 1. Initialize Hybrid Search
    bm25_engine = BM25Retriever(df_corpus)
    dense_engine = DenseRetriever(df_corpus)
    hybrid_engine = HybridRetriever(bm25_engine, dense_engine, rrf_k=60)

    # 2. Get Hybrid candidates
    hybrid_candidates = hybrid_engine.search(args.query, top_k=args.candidate_k, candidate_k=args.candidate_k)

    # 3. Print BEFORE RERANK
    print("=" * 85)
    print(" BEFORE RERANK (Hybrid Search Top Candidates)")
    print("=" * 85)
    header = f"{'Rank':<5} | {'Chunk ID':<22} | {'BM25 rank':<10} | {'Dense rank':<10} | {'RRF Score':<10} | {'Citation'}"
    print(header)
    print("-" * 85)
    for r in hybrid_candidates[:args.top_k]:
        b_rank_str = str(r['bm25_rank'])
        d_rank_str = str(r['dense_rank'])
        rrf_str = f"{r['rrf_score']:.6f}"
        cit_snippet = r['citation']
        if len(cit_snippet) > 40:
            cit_snippet = cit_snippet[:37] + "..."
        print(f"{r['final_rank']:<5} | {r['chunk_id']:<22} | {b_rank_str:<10} | {d_rank_str:<10} | {rrf_str:<10} | {cit_snippet}")
    print("=" * 85 + "\n")

    # 4. Execute Reranking
    reranker_engine = Reranker()
    reranked_results = reranker_engine.rerank(args.query, hybrid_candidates, top_k=args.top_k)

    # 5. Print AFTER RERANK
    print("=" * 85)
    print(f" AFTER RERANK ({reranked_results[0]['rerank_method'] if reranked_results else 'RERANKED'})")
    print("=" * 85)
    header_after = f"{'Final':<5} | {'Chunk ID':<22} | {'Hybrid rank':<11} | {'Hybrid RRF':<10} | {'Rerank Score':<12} | {'Citation'}"
    print(header_after)
    print("-" * 85)
    for r in reranked_results:
        h_rank_str = str(r['hybrid_rank'])
        h_score_str = f"{r['hybrid_score']:.6f}"
        r_score_str = f"{r['rerank_score']:.4f}"
        cit_snippet = r['citation']
        if len(cit_snippet) > 40:
            cit_snippet = cit_snippet[:37] + "..."
        print(f"{r['final_rank']:<5} | {r['chunk_id']:<22} | {h_rank_str:<11} | {h_score_str:<10} | {r_score_str:<12} | {cit_snippet}")
    print("=" * 85 + "\n")

if __name__ == "__main__":
    main()
