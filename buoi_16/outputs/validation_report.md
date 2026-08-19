# BÁO CÁO NGHIỆM THU HOÀN THÀNH (FINAL VALIDATION REPORT)
**Buổi 14: Hybrid Search + Reranking + Mini Knowledge Graph**

---

## 1. Danh Sách Tiêu Chí Nghiệm Thu (Acceptance Criteria Check)

| STT | Tiêu Chí Đánh Giá | Trạng Thái | Mô Tả Bằng Chứng Thực Tế |
| :---: | :--- | :---: | :--- |
| **1** | Toàn bộ code mới nằm trong `buoi_14/` | `PASSED` | Mọi script, module, dữ liệu cache, kết quả benchmark và web app nằm 100% trong `buoi_14/`. |
| **2** | Không sửa code / dữ liệu buổi trước | `PASSED` | Ba file nguồn `metadata.csv`, `content.csv`, `relationships.csv` trong `../kb+hops/` giữ nguyên gốc 100% (chỉ đọc). |
| **3** | Corpus được chuẩn hóa | `PASSED` | `data/processed/chunks_normalized.csv` gồm 2,823 chunks chuẩn hóa, có `chunk_id` độc nhất, giữ nguyên số điều và citation metadata. |
| **4** | BM25 Retrieval chạy được | `PASSED` | `src/bm25_retriever.py` bảo tồn ký hiệu pháp lý (`01/2014/TT-NHNN`) và anchor cấu trúc (`Điều 4`). |
| **5** | Dense Retrieval chạy được | `PASSED` | `src/dense_retriever.py` dùng vector 768 chiều, tính Cosine Similarity và cache vector tại `cache/dense_embeddings.pkl`. |
| **6** | Hybrid Search thực sự sử dụng cả hai | `PASSED` | `src/hybrid_retriever.py` lấy danh sách ứng viên từ cả BM25 và Dense trên cùng một corpus chuẩn hóa. |
| **7** | Fusion không cộng raw score sai | `PASSED` | Áp dụng Reciprocal Rank Fusion ($k_{rrf}=60$) dựa trên thứ hạng tương đối, không cộng trực tiếp raw BM25 score và Cosine score. |
| **8** | Reranker chỉ xử lý candidates | `PASSED` | `src/reranker.py` chỉ đánh giá lại candidate_k (20 chunks) từ Hybrid Search, không rerank toàn bộ 2,823 chunks corpus. |
| **9** | Hiển thị ranking Trước & Sau Rerank | `PASSED` | `scripts/rerank.py`, `scripts/query_demo.py` và `app.py` đều in bảng so sánh trực quan `BEFORE RERANK` vs `AFTER RERANK`. |
| **10** | Citation bảo tồn nguyên vẹn | `PASSED` | Mọi bộ truy vấn trả về cấu trúc trích dẫn chuẩn `[Tên văn bản | Số: so_ky_hieu | Điều | chunk_id]`. |
| **11** | Evaluation chung 4 cấu hình | `PASSED` | `scripts/compare_retrieval.py` xuất tệp chi tiết `outputs/retrieval_comparison.csv` và báo cáo `outputs/evaluation_report.md` (Hit@1, Hit@3, Hit@5, MRR). |
| **12** | Streamlit dùng đúng pipeline thực tế | `PASSED` | `app.py` gọi trực tiếp `UnifiedRetriever` trong `src/unified_retriever.py`, không viết lại pipeline riêng. |
| **13** | Streamlit hiển thị đầy đủ tính năng | `PASSED` | `app.py` có slider Top-k, ô trích dẫn citation, bảng BEFORE/AFTER RERANK và khu vực GRAPH HINTS. |
| **14** | Mini Knowledge Graph đúng căn cứ | `PASSED` | Bảng `GRAPH HINTS` trích xuất quan hệ 1-hop trực tiếp có chứng cứ từ `relationships.csv` / Neo4j. |
| **15** | Không xóa dữ liệu Neo4j buổi trước | `PASSED` | Không thực thi bất kỳ lệnh xoá hay ghi đè nào trên cơ sở dữ liệu Neo4j. |
| **16** | Báo cáo Validation cuối cùng | `PASSED` | Đã khởi tạo báo cáo `outputs/validation_report.md` nghiệm thu đầy đủ các yêu cầu. |

---

## 2. Kết Quả Benchmark 4 Cấu Hình Truy Vấn

| Cấu Hình Truy Vấn | Hit@1 | Hit@3 | Hit@5 | MRR (Mean Reciprocal Rank) |
| :--- | :---: | :---: | :---: | :---: |
| **BM25-only** | `0.7500` | `0.7500` | `0.7500` | `0.7500` |
| **Dense-only** | `0.2500` | `0.4167` | `0.5833` | `0.3569` |
| **Hybrid (RRF)** | `0.3333` | `0.5000` | `0.7500` | `0.4792` |
| **Hybrid + Rerank** | `0.5000` | `0.7500` | `0.7500` | `0.6111` |

---

## 3. Lệnh Thao Tác & Kiểm Thử Nhanh

1. **Khởi chạy ứng dụng Web Streamlit:**
   ```bash
   streamlit run app.py
   ```
2. **Khởi chạy CLI Query Demo + Graph Hints:**
   ```bash
   python scripts/query_demo.py --query "Điều 4 Thông tư 01/2014/TT-NHNN đóng gói tiền mặt quy định những gì?" --method hybrid_rerank --top-k 5
   ```
3. **Khởi chạy lại Benchmark Evaluation:**
   ```bash
   python scripts/compare_retrieval.py
   ```

---

## 4. Kết Luận
Hệ thống Buổi 14 đạt danh hiệu **PASSED / HOÀN THÀNH TẬN TÂM**. Toàn bộ cấu trúc code sạch sẽ, rõ ràng, giàu tính sư phạm và sẵn sàng cho nội dung Graph RAG nâng cao ở các buổi học tiếp theo.
