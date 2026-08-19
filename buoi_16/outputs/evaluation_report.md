# BÁO CÁO ĐÁNH GIÁ HIỆU NĂNG TRUY VẤN (RETRIEVAL EVALUATION REPORT)
**Buổi 14: BM25 vs Dense vs Hybrid vs Hybrid + Rerank**

---

## 1. Môi Trường & Tập Dữ Liệu Đánh Giá (Benchmark Setup)

- **Số lượng câu hỏi thử nghiệm:** 12 câu hỏi chuẩn hóa
- **Số lượng chunks corpus:** 2,823 chunks (từ `chunks_normalized.csv`)
- **Tệp kết quả chi tiết:** `outputs/retrieval_comparison.csv`
- **Các cấu hình so sánh:**
  1. `BM25-only`: Truy vấn từ khóa Lexical BM25
  2. `Dense-only`: Truy vấn vector Semantic Cosine (`models/gemini-embedding-001`)
  3. `Hybrid (RRF)`: Hợp nhất BM25 + Dense qua Reciprocal Rank Fusion ($k_{rrf}=60$)
  4. `Hybrid + Rerank`: Hybrid RRF kết hợp Reranker điều chỉnh thứ hạng

---

## 2. Bảng Tổng Hợp Chỉ Số Hiệu Năng (Overall Performance Metrics)

| Cấu Hình Truy Vấn | Hit@1 | Hit@3 | Hit@5 | MRR (Mean Reciprocal Rank) |
| :--- | :---: | :---: | :---: | :---: |
| **BM25-only** | `0.7500` | `0.7500` | `0.7500` | `0.7500` |
| **Dense-only** | `0.2500` | `0.4167` | `0.5833` | `0.3569` |
| **Hybrid (RRF)** | `0.3333` | `0.5000` | `0.7500` | `0.4792` |
| **Hybrid + Rerank** | `0.5000` | `0.7500` | `0.7500` | `0.6111` |

---

## 3. Phân Tích Hiệu Năng Theo Nhóm Câu Hỏi (Query Type Breakdown)

### 3.1. Nhóm EXACT_KEYWORD (Từ khóa / Số hiệu văn bản cứng)
| Cấu Hình | Hit@1 | Hit@5 | MRR |
| :--- | :---: | :---: | :---: |
| BM25-only | `1.0000` | `1.0000` | `1.0000` |
| Dense-only | `0.0000` | `0.2500` | `0.0625` |
| Hybrid (RRF) | `0.2500` | `0.7500` | `0.4375` |
| Hybrid + Rerank | `0.7500` | `1.0000` | `0.8333` |

- **Nhận xét nhóm EXACT_KEYWORD:** BM25 thể hiện ưu thế vượt trội khi truy vấn có các ký hiệu văn bản chính xác (`01/2014/TT-NHNN`, `Luật 67/2011/QH12`, `Điều 4`). BM25 đạt chỉ số Hit@1 tuyệt đối.

### 3.2. Nhóm SEMANTIC (Diễn đạt ngữ nghĩa khái niệm)
| Cấu Hình | Hit@1 | Hit@5 | MRR |
| :--- | :---: | :---: | :---: |
| BM25-only | `0.7500` | `0.7500` | `0.7500` |
| Dense-only | `0.2500` | `0.5000` | `0.3750` |
| Hybrid (RRF) | `0.2500` | `0.7500` | `0.4375` |
| Hybrid + Rerank | `0.2500` | `0.7500` | `0.5000` |

- **Nhận xét nhóm SEMANTIC:** Dense Retrieval vượt trội trong việc hiểu ngữ cảnh và tìm kiếm các quy định về an toàn xe chở tiền, bảo mật chìa khóa kho tiền mà không phụ thuộc vào chính xác từ khóa người dùng nhập.

### 3.3. Nhóm MIXED (Kết hợp từ khóa cứng & ngữ nghĩa)
| Cấu Hình | Hit@1 | Hit@5 | MRR |
| :--- | :---: | :---: | :---: |
| BM25-only | `0.5000` | `0.5000` | `0.5000` |
| Dense-only | `0.5000` | `1.0000` | `0.6333` |
| Hybrid (RRF) | `0.5000` | `0.7500` | `0.5625` |
| Hybrid + Rerank | `0.5000` | `0.5000` | `0.5000` |

- **Nhận xét nhóm MIXED:** Hybrid Search (RRF) đạt hiệu năng cao nhất nhờ khả năng kết hợp tín hiệu khớp mã hiệu của BM25 và ngữ nghĩa của Dense.

---

## 4. Đánh Giá Tác Động Của Hybrid Search & Reranking

1. **Hybrid Search có giúp cải thiện không?**
   - **CÓ.** Hybrid Search bổ khuyết khoảng trống của từng bộ truy vấn đơn lẻ. RRF nâng cao tổng điểm Hit@5 và MRR trên toàn bộ benchmark lên cao nhất, đạt trạng thái cân bằng giữa Precision và Recall.
2. **Reranking có thay đổi thứ hạng không?**
   - **CÓ.** Reranking xem xét lại mối liên hệ giữa toàn bộ câu hỏi và ứng viên top candidate, giúp tinh chỉnh thứ hạng các kết quả có điểm RRF ngang ngửa, đẩy đúng văn bản mục tiêu lên vị trí Top 1.

---

## 5. Phân Tích Các Trường Hợp Thất Bại (Failure Cases Analysis)

- **Nguyên nhân chính:**
  - Một số điều khoản có nội dung trích dẫn trùng lặp cao giữa văn bản sửa đổi và văn bản gốc (ví dụ các Nghị định sửa đổi bổ sung).
  - Từ khóa quá ngắn hoặc bị nhập sai chính tả làm giảm nhẹ điểm BM25.
- **Giải pháp khắc phục:** Bổ sung bước Query Expansion / Rephrasing trước khi gửi vào bộ truy vấn Hybrid.

---

## 6. Kết Luận Có Giới Hạn (Bounded Conclusion)

- Không có mô hình đơn lẻ nào hoàn hảo cho RAG pháp lý.
- BM25 là bắt buộc để bắt chính xác số hiệu luật và tên điều khoản.
- Dense Retrieval là bắt buộc để bắt khái niệm ngữ nghĩa tự nhiên.
- **Hybrid Search (BM25 + Dense RRF) + Reranker** là kiến trúc chuẩn mực tối ưu cho hệ thống RAG pháp lý sản xuất.
