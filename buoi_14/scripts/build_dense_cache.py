import os
import sys
import pandas as pd

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(base_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from dense_retriever import DenseRetriever

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    corpus_csv = os.path.join(base_dir, "data", "processed", "chunks_normalized.csv")
    if not os.path.exists(corpus_csv):
        print(f"Lỗi: Không tìm thấy corpus tại {corpus_csv}")
        sys.exit(1)
        
    df = pd.read_csv(corpus_csv, dtype=str)
    print(f"Building/Resuming Dense Embeddings cache for {len(df)} chunks...")
    retriever = DenseRetriever(df)
    print(f"Cache build complete! Matrix shape: {retriever.embeddings.shape}")

if __name__ == "__main__":
    main()
