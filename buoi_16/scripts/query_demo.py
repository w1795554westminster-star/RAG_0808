import os
import sys
import argparse
import pandas as pd

# Add src to python path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from unified_retriever import UnifiedRetriever

def main():
    sys.stdout.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(description="Unified RAG Query Demo CLI — Buổi 14")
    parser.add_argument("--query", "-q", type=str, required=True, help="Câu hỏi tìm kiếm")
    parser.add_argument("--method", "-m", type=str, default="hybrid_rerank", choices=["bm25", "dense", "hybrid", "hybrid_rerank"], help="Phương thức retrieval")
    parser.add_argument("--top-k", "-k", type=int, default=5, help="Số kết quả trả về")
    args = parser.parse_args()

    engine = UnifiedRetriever()

    print("\n" + "=" * 85)
    print(f" RAG UNIFIED RETRIEVAL DEMO — BUỔI 14")
    print(f" Query  : '{args.query}'")
    print(f" Method : {args.method.upper()}")
    print(f" Top-K  : {args.top_k}")
    print("=" * 85 + "\n")

    # If method is hybrid_rerank, demonstrate BEFORE vs AFTER RERANK
    if args.method == "hybrid_rerank":
        before_candidates = engine.retrieve(args.query, method="hybrid", top_k=args.top_k, candidate_k=20)
        print("-" * 85)
        print(" BEFORE RERANK (Hybrid Search Top Candidates)")
        print("-" * 85)
        header_b = f"{'Rank':<5} | {'Chunk ID':<22} | {'BM25 rank':<10} | {'Dense rank':<10} | {'RRF Score':<10} | {'Citation'}"
        print(header_b)
        print("-" * 85)
        for r in before_candidates:
            b_rank = str(r.get('bm25_rank', 'N/A'))
            d_rank = str(r.get('dense_rank', 'N/A'))
            rrf_str = f"{r['score']:.6f}"
            cit = r['citation'][:35] + "..." if len(r['citation']) > 35 else r['citation']
            print(f"{r['rank']:<5} | {r['chunk_id']:<22} | {b_rank:<10} | {d_rank:<10} | {rrf_str:<10} | {cit}")
        print("-" * 85 + "\n")

    # Final retrieval execution
    results = engine.retrieve(args.query, method=args.method, top_k=args.top_k)

    print("=" * 85)
    print(f" FINAL RETRIEVAL RESULTS ({args.method.upper()})")
    print("=" * 85)
    header_f = f"{'Rank':<5} | {'Chunk ID':<22} | {'Doc ID':<10} | {'Score':<10} | {'Citation'}"
    print(header_f)
    print("-" * 85)
    for r in results:
        score_str = f"{r['score']:.4f}"
        cit = r['citation'][:40] + "..." if len(r['citation']) > 40 else r['citation']
        print(f"{r['rank']:<5} | {r['chunk_id']:<22} | {r['document_id']:<10} | {score_str:<10} | {cit}")
    print("=" * 85 + "\n")

    # GRAPH HINTS section
    hints = engine.get_graph_hints(results)
    print("=" * 85)
    print(" GRAPH HINTS (Bằng chứng liên kết Mini Knowledge Graph)")
    print("=" * 85)
    print(f" Retrieved Document IDs : {hints['retrieved_doc_ids']}")
    print(f" Retrieved Chunk IDs    : {hints['retrieved_chunk_ids']}")
    print(f" Relationship Source    : {hints['source']}")
    print("-" * 85)
    print(f"{'Source Doc':<15} | {'Relationship':<25} | {'Target Node / Entity':<25} | {'Evidence Snippet'}")
    print("-" * 85)
    if hints['direct_relationships']:
        for rel in hints['direct_relationships']:
            src = rel['source']
            rtype = rel['relationship']
            tgt = rel['target']
            ev = rel['evidence']
            print(f"{src:<15} | {rtype:<25} | {tgt:<25} | {ev}")
    else:
        print(" (Không tìm thấy quan hệ 1-hop trực tiếp nào trong Mini KG)")
    print("=" * 85 + "\n")

if __name__ == "__main__":
    main()
