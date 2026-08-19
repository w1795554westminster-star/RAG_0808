# BÁO CÁO ĐÁNH GIÁ HỆ THỐNG RAG TỰ ĐỘNG (RAGAS EVALUATION REPORT)
**Buổi 15: Kiểm soát Truy cập RBAC, RAG Pipeline & Ragas Metrics Benchmark**

---

## 1. Bảng Tóm Tắt Điểm Trung Bình 4 Ragas Metrics (Executive Metric Summary)

| Ragas Metric | Điểm Trung Bình (Average Score) | Đánh Giá Hiệu Năng |
| :--- | :---: | :--- |
| **Context Precision** | `0.5500` | Độ chính xác thứ hạng các đoạn ngữ cảnh trích xuất |
| **Context Recall** | `0.7030` | Khả năng bao phủ toàn bộ thông tin đáp án chuẩn |
| **Faithfulness** | `1.0000` | Độ trung thực của câu trả lời so với ngữ cảnh |
| **Answer Relevancy** | `0.7000` | Độ liên quan trực tiếp của câu trả lời với câu hỏi |
| **OVERALL RAG SCORE** | `0.7382` | **Điểm Đánh Giá Tổng Thể Hệ Thống RAG** |

---

## 2. Phân Tích Chi Tiết 20 Câu Hỏi Thử Nghiệm (Detailed Evaluation Matrix)

| Q_ID | Độ Khó | Context Precision | Context Recall | Faithfulness | Answer Relevancy | Overall Score |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Q01** | easy | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q02** | medium | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q03** | hard | `1.0000` | `1.0000` | `1.0000` | `0.7000` | `0.9250` |
| **Q04** | easy | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q05** | medium | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q06** | medium | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q07** | hard | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q08** | medium | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q09** | easy | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q10** | medium | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q11** | hard | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q12** | hard | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q13** | easy | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q14** | medium | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q15** | easy | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q16** | medium | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q17** | medium | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q18** | hard | `1.0000` | `1.0000` | `1.0000` | `0.7000` | `0.9250` |
| **Q19** | easy | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |
| **Q20** | medium | `0.5000` | `0.6700` | `1.0000` | `0.7000` | `0.7175` |

---

## 3. Phân Tích Nguyên Nhân Lỗi Cho Các Câu Hỏi Có Điểm Thấp (< 0.75)

### Câu Hỏi [Q01]: "Điều 4 Thông tư 01/2014/TT-NHNN đóng gói tiền mặt quy định những gì?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q02]: "Vận chuyển tiền mặt và tài sản quý trong ngành ngân hàng cần tuân thủ nguyên tắc an toàn nào?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q04]: "Phạm vi điều chỉnh của Chế độ giao nhận bảo quản vận chuyển tiền mặt theo Thông tư 01/2014/TT-NHNN?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q05]: "Nhiệm vụ của thủ kho tiền trong công tác bảo quản và quản lý tài sản quý?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q06]: "Trách nhiệm của Giám đốc Ngân hàng Nhà nước chi nhánh trong việc quản lý kho tiền?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q07]: "Điều kiện trang bị xe chở tiền chuyên dụng ngân hàng gồm những chuẩn gì?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q08]: "Thông tư số 43/2024/TT-NHNN sửa đổi bổ sung những nội dung gì của Thông tư 01/2014/TT-NHNN?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q09]: "Quy định về lập biên bản khi giao nhận tiền mặt phát hiện thừa thiếu?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q10]: "Quy trình mở cửa kho tiền đầu ngày và đóng cửa kho tiền cuối ngày?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q11]: "Quy định kỷ luật đối với cán bộ ngân hàng vi phạm quy trình quản lý kho tiền?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q12]: "Trách nhiệm bảo vệ tiền mặt trên đường vận chuyển khi xe bị sự cố?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q13]: "Tiêu chuẩn niêm phong niêm tiền mặt của Ngân hàng Nhà nước?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q14]: "Bảo quản giấy tờ có giá và tài sản quý nhận thế chấp bảo đảm?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q15]: "Quy định về thời hạn hết hiệu lực của các văn bản cũ theo Thông tư 01/2014?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q16]: "Thủ tục bàn giao ca trực bảo vệ kho tiền ban đêm?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q17]: "Chế độ báo cáo định kỳ tình hình an toàn kho tiền ngân hàng?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q19]: "Quy định về việc mang đồ vật cá nhân vào khu vực kho tiền?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

### Câu Hỏi [Q20]: "Trách nhiệm của kiểm ngân trong việc phát hiện tiền giả khi kiểm đếm?" (Overall: `0.7175`)
- **Hiện tượng:** Điểm Context Precision / Recall đạt `0.5000` / `0.6700`.
- **Nguyên nhân chính:**
  - Từ khóa câu hỏi chứa cụm từ diễn đạt tự nhiên (SEMANTIC) làm giảm nhẹ điểm BM25 rank.
  - Đoạn văn bản chuẩn chứa nhiều điều khoản tham chiếu đéo trùng hoàn toàn 100% từ khóa bề mặt.
- **Biện pháp khắc phục:** Bổ sung bước **Query Expansion / Rephrasing** trước khi đưa vào Hybrid Search.

---

## 4. Đề Xuất Tối Ưu Hóa Hệ Thống RAG (System Optimization Recommendations)

1. **Nâng cấp Reranker Cross-Encoder:** Sử dụng mô hình Neural Cross-Encoder tiếng Việt chuyên biệt (`bge-reranker-v2-m3`) để tối ưu hóa vị trí Top-1 cho các câu hỏi phức tạp.
2. **Triển khai Parent-Child Chunking:** Áp dụng kỹ thuật Parent Document Retriever để trích xuất ngữ cảnh rộng hơn cho LLM sinh câu trả lời đầy đủ ý hơn.
3. **Thêm Query Rewriting:** Tăng cường thành phần phát sinh câu hỏi tương đương để nâng cao chỉ số Context Recall trên các câu hỏi diễn đạt gián tiếp.

---

## 5. Kết Luận
Hệ thống RAG đã được đánh giá tự động thành công với **Overall RAG Score = 0.7382**.
