# Buổi 14: Hybrid Search + Reranking + Mini Knowledge Graph

Thư mục dự án Buổi 14 triển khai hoàn chỉnh hệ thống RAG nâng cao kết hợp Truy vấn hỗn hợp (Hybrid Search BM25 + Dense Embeddings), Đánh giá lại thứ tự (Reranking), Báo cáo Đánh giá Benchmark (Retrieval Evaluation), và Giao diện Demo tương tác Web Streamlit.

---

## 1. Cấu Trúc Thư Mục Dự Án

```text
buoi_14/
├── app.py                             # Giao diện Web Streamlit ứng dụng RAG Hybrid Search
├── requirements.txt                   # Danh sách thư viện phụ thuộc của dự án
├── cache/
│   ├── dense_embeddings.pkl           # Cache vector embedding cho 2,823 chunks
│   └── query_embeddings.pkl           # Cache vector embedding cho câu hỏi truy vấn
├── data/
│   ├── eval/
│   │   └── questions.csv              # Tập 12 câu hỏi chuẩn hóa đánh giá Benchmark
│   └── processed/
│       └── chunks_normalized.csv      # Tập dữ liệu chunk chuẩn hóa (2,823 chunks)
├── outputs/
│   ├── inspection_report.md           # Báo cáo tiền kiểm tra dữ liệu nguồn (Prompt 0)
│   ├── retrieval_examples.md          # Báo cáo kết quả thử nghiệm BM25, Dense, Hybrid & Rerank (Prompts 2-4)
│   ├── retrieval_comparison.csv       # Kết quả đánh giá chi tiết từng câu hỏi (Prompt 5)
│   └── evaluation_report.md           # Báo cáo tổng hợp chỉ số Hit@1, Hit@3, Hit@5, MRR (Prompt 5)
├── scripts/
│   ├── prepare_corpus.py              # Script chuẩn hóa dữ liệu retrieval từ CSV nguồn (Prompt 1)
│   ├── build_dense_cache.py           # Script tạo & cache vector embedding
│   ├── baseline_retrieval.py          # CLI so sánh BM25 vs Dense baseline (Prompt 2)
│   ├── hybrid_search.py               # CLI truy vấn Hybrid Search (BM25 + Dense RRF) (Prompt 3)
│   ├── rerank.py                      # CLI truy vấn Hybrid + Reranking (Prompt 4)
│   ├── compare_retrieval.py           # Script đánh giá benchmark tự động 4 cấu hình (Prompt 5)
│   └── query_demo.py                  # CLI demo truy vấn thống nhất + Graph Hints
└── src/
    ├── bm25_retriever.py              # Bộ truy vấn Lexical BM25 tiếng Việt
    ├── dense_retriever.py             # Bộ truy vấn Semantic Vector (Embedding + Cosine Sim)
    ├── hybrid_retriever.py            # Bộ truy vấn Hybrid Search Reciprocal Rank Fusion (RRF)
    ├── reranker.py                    # Bộ đánh giá lại thứ tự Reranker (Cross-Encoder / Fallback)
    └── unified_retriever.py           # API Retrieval thống nhất retrieve(question, method, top_k)
```

---

## 2. Hướng Dẫn Chạy Giao Diện Web Streamlit (`app.py`)

### 2.1 Lệnh Khởi Chạy Web App
Mở terminal tại thư mục `buoi_14/` và chạy lệnh:

```bash
streamlit run app.py
```

Ứng dụng sẽ hiển thị thông báo địa chỉ trên Terminal:
- **Local URL:** `http://localhost:8501`
- **Network URL:** `http://<YOUR_LOCAL_IP>:8501`

### 2.2 Cách Dừng Ứng Dụng Streamlit
Để dừng máy chủ Streamlit, bấm tổ hợp phím **`Ctrl + C`** trên Terminal nơi đang chạy ứng dụng.

---

## 3. Các Phương Thức Retrieval Trực Quan Trên Streamlit

Trong thanh điều khiển bên trái (Sidebar), bạn có thể lựa chọn 4 phương thức truy vấn:

1. **`BM25` (Lexical Keyword Search):** Ưu thế cao khi tìm kiếm chính xác mã hiệu văn bản, số điều (Ví dụ: `Thông tư 01/2014/TT-NHNN`, `Điều 4`).
2. **`Dense` (Semantic Vector Search):** Ưu thế cao khi người dùng hỏi bằng câu từ tự nhiên hoặc tìm kiếm khái niệm ngữ nghĩa (Ví dụ: `Bảo quản và vận chuyển tài sản quý`).
3. **`Hybrid (RRF)`:** Hợp nhất thứ hạng từ BM25 và Dense bằng công thức Reciprocal Rank Fusion ($k_{rrf}=60$), đảm bảo không bỏ sót kết quả của từng nguồn.
4. **`Hybrid + Rerank`:** Lấy Top-20 ứng viên từ Hybrid Search, sau đó chạy bộ Reranker để soi kỹ ngữ cảnh câu hỏi và xếp lại thứ hạng chính xác nhất trước khi gửi cho LLM.

---

## 4. Giải Thích Các Trường Kết Quả Trả Về

- **`rank` / `Final Rank`:** Thứ hạng kết quả cuối cùng (1..Top-K).
- **`chunk_id`:** Mã định danh duy nhất của đoạn trích (Ví dụ: `44209_chunk_007`).
- **`document_id`:** Số hiệu văn bản gốc (Ví dụ: `44209`).
- **`score`:** Điểm số tương ứng với phương thức được chọn (BM25 score / Cosine Similarity / RRF Score / Rerank Score).
- **`citation`:** Trích dẫn nguồn pháp lý chuẩn hóa `[Tên văn bản | Số hiệu | Điều | Chunk ID]`.
- **`BEFORE RERANK / AFTER RERANK`:** Bảng so sánh trực quan thứ tự thay đổi của các chunks trước và sau khi đi qua bộ Reranker.
- **`GRAPH HINTS`:** Trích xuất các liên kết 1-hop trực tiếp (mã văn bản, văn bản được tham chiếu, cơ quan ban hành, người ký) chuẩn bị dữ liệu cho bài học Graph RAG tiếp theo.

---

## 5. Bảng Tổng Hợp Chỉ Số Đánh Giá Benchmark (Evaluation Summary)

| Cấu Hình Truy Vấn | Hit@1 | Hit@3 | Hit@5 | MRR (Mean Reciprocal Rank) |
| :--- | :---: | :---: | :---: | :---: |
| **BM25-only** | `0.7500` | `0.7500` | `0.7500` | `0.7500` |
| **Dense-only** | `0.2500` | `0.4167` | `0.5833` | `0.3569` |
| **Hybrid (RRF)** | `0.3333` | `0.5000` | `0.7500` | `0.4792` |
| **Hybrid + Rerank** | `0.5000` | `0.7500` | `0.7500` | `0.6111` |
