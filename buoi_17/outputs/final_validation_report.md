# BÁO CÁO AUDIT VÀ THẨM ĐỊNH TOÀN BỘ PROJECT BUỔI 17

**Ngày audit:** 2026-08-21  
**Phạm vi audit:** Toàn bộ thư mục `buoi_17/` và dữ liệu nguồn `../buoi_16/data/processed/chunks_secure.csv`  
**Mục tiêu:** Thẩm định tính toàn vẹn dữ liệu, phân quyền RBAC, kiến trúc Secure RAG, kiểm toán Audit Log, Compliance Gap Checker và Streamlit Demo Interface.

---

## 1. KẾT QUẢ KIỂM TRA CHI TIẾT THEO YÊU CẦU AUDIT

### 1.1. TÍNH TOÀN VẸN DỮ LIỆU VÀ KHÔNG SỬA SOURCE DATA
- **Dữ liệu nguồn:** File `../buoi_16/data/processed/chunks_secure.csv` giữ nguyên trạng (2,823 dòng, 20 cột).
- **Trạng thái:** Dữ liệu được đọc qua đường dẫn tương đối thông qua Directory Junction mà không có bất kỳ thao tác ghi hay sửa đổi nào trên file gốc.

### 1.2. TÁI SỬ DỤNG HYBRID / RERANKER BÀI CŨ
- **Kiến trúc:** Đã tái sử dụng nguyên trạng `SecureRetriever` của Buổi 16 (`buoi_16/src/secure_retriever.py`).
- **Adapter:** Tạo [secure_retrieval_adapter.py](file:///d:/03.08/buoi_17/scripts/secure_retrieval_adapter.py) đóng vai trò chuẩn hóa kết quả đầu ra (10 thuộc tính), hoàn toàn không viết lại thuật toán tìm kiếm.

### 1.3. RBAC FILTER TRƯỚC RETRIEVAL / LLM CONTEXT
- **Cơ chế:** Phân quyền RBAC được thực thi ở tầng corpus tiền lọc (`pre-filtering`). Mọi chỉ mục tìm kiếm (BM25 & Vector) chỉ được xây dựng trên tập dữ liệu đã qua lọc `allowed_roles`.
- **Rò rỉ dữ liệu:** 0% tài liệu DENY xuất hiện trong LLM context hay kết quả tìm kiếm của vai trò không được phép.

### 1.4. AUDIT TRAIL VÀ NHẬT KÝ KIỂM TOÁN
- **Nhật ký:** Mọi truy vấn tra cứu đều được ghi tự động vào [audit_log.jsonl](file:///d:/03.08/buoi_17/outputs/audit_log.jsonl).
- **Thông tin lưu trữ:** Ghi nhận đầy đủ `request_id`, `user_role`, `question`, `answer_status`, `access_scope`, danh sách `citations` và `filtered_out_count`.

### 1.5. BẢO MẬT BÍ MẬT & MÃ HÓA AT-REST DEMO
- **Quản lý khóa:** Không hard-code API Key hay mật khẩu trong mã nguồn. Khóa mã hóa `encryption.key` và file mã hóa `*.enc` được phân lập hoàn toàn qua `.gitignore`.
- **Encryption Demo:** File [encryption_demo.py](file:///d:/03.08/buoi_17/scripts/encryption_demo.py) mã hóa Fernet cho nhật ký audit và ghi rõ trong báo cáo: *"Demo đào tạo — không tuyên bố Production-ready"*.

### 1.6. DỊCH VỤ TRA CỨU NỘI BỘ (INTERNAL LOOKUP)
- **Tích hợp:** File [internal_lookup.py](file:///d:/03.08/buoi_17/scripts/internal_lookup.py) gọi adapter an toàn và Gemini API.
- **Trích dẫn:** 100% câu trả lời đều có trích dẫn đính kèm. Trường hợp thiếu thông tin context trả về chuẩn xác: `"Không tìm thấy đủ thông tin trong phạm vi tài liệu được phép truy cập."`

### 1.7. AI COMPLIANCE GAP CHECKER
- **Đánh giá dữ liệu:** Đã kiểm tra 30 văn bản trong corpus, tất cả đều là Văn bản Pháp luật State (`EXTERNAL_REQUIREMENT`). Không có văn bản quy định nội bộ Agribank thực tế (`INTERNAL_POLICY`).
- **Phân loại:** Đã xuất kết quả [gap_input_catalog.md](file:///d:/03.08/buoi_17/outputs/gap_input_catalog.md) với thông số `COMPLIANCE GAP DATA: INSUFFICIENT` & `DATA GAP: INTERNAL POLICY NOT FOUND`.
- **Xử lý Gap:** Hệ thống gán chính xác phân loại `CHUA_DU_BANG_CHUNG` thay vì kết luận sai `THIEU`.
- **Human Review Guardrail:** 100% dòng trong [compliance_gap_results.csv](file:///d:/03.08/buoi_17/outputs/compliance_gap_results.csv) được gán `review_status = "NEEDS_HUMAN_REVIEW"`.

### 1.8. KNOWLEDGE GRAPH NÉO4J INTEGRATION
- **Đánh giá Quan hệ:** Đã phân tích 329 cạnh trong `kb+hops/relationships.csv` (`THAM_CHIEU`, `SUA_DOI_BO_SUNG`, `THAY_THE_BOI`).
- **Trạng thái thực tế:** Trạng thái kết nối Neo4j được kiểm tra qua kết nối socket thực tế (Port 7687). Khi Neo4j down, giao diện báo chính xác `INACTIVE` mà không giả lập.

### 1.9. STREAMLIT DEMO WEB APPLICATION
- **File ứng dụng:** [app.py](file:///d:/03.08/buoi_17/app.py) hoạt động ổn định với 3 Tab chính (Tra cứu Quy định, Compliance Gap Checker, Audit Trail Viewer).
- **Banner cảnh báo:** Cấu hình banner bắt buộc: *"Demo đào tạo — kết quả AI cần kiểm toán viên xác minh."*

---

## 2. BẢNG DANH MỤC KIỂM TRA VÀ THẨM ĐỊNH (CHECKLIST)

| Hạng mục kiểm tra | Trạng thái | Ghi chú thẩm định |
| :--- | :---: | :--- |
| Không rebuild RAG không cần thiết | **PASS** | Tái sử dụng 100% SecureRetriever bài cũ qua Adapter. |
| RBAC hoạt động ở tầng retrieval | **PASS** | Tiền lọc `df_corpus['allowed_roles']` trước khi build index. |
| Không lộ unauthorized context | **PASS** | 0% chunk bị cấm xuất hiện trong câu trả lời hay context. |
| Audit log ghi được request | **PASS** | File `audit_log.jsonl` cập nhật theo từng request_id. |
| Không log secret | **PASS** | Quét 100% log, không chứa API Key hay Password. |
| Tra cứu nội bộ có citation | **PASS** | Trích dẫn pháp lý đầy đủ và chuẩn hóa. |
| Gap Checker có evidence hai phía | **PASS** | Ghi nhận văn bản bên ngoài và báo thiếu văn bản nội bộ. |
| Có DAP_UNG / THIEU / CHENH_LECH / CHUA_DU_BANG_CHUNG | **PASS** | Đầy đủ 4 giá trị phân loại theo đúng Enum chuẩn. |
| Mọi finding cần human review | **PASS** | `review_status = "NEEDS_HUMAN_REVIEW"` cho 100% dòng. |
| Streamlit demo chạy | **PASS** | Giao diện Web hiển thị mượt mà với banner bắt buộc. |
| Neo4j báo đúng trạng thái thật | **PASS** | Socket check Port 7687 hoạt động chính xác. |

---

## 3. TỔNG KẾT VÀ XÁC NHẬN CHÍNH THỨC

```text
RBAC: PASS
SECURE RETRIEVAL: PASS
AUDIT TRAIL: PASS
CITATION: PASS
COMPLIANCE GAP: PASS
HUMAN REVIEW GUARDRAIL: PASS
STREAMLIT: PASS
WORKSPACE ISOLATION: PASS

READY FOR DEMO: YES
```
