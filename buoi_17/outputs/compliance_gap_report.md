# BÁO CÁO BẢO ĐẢM NGUYÊN TẮC VÀ THIẾT KẾ AI COMPLIANCE GAP CHECKER (BUỔI 17)

---

## 1. Kết Quả Đánh Giá Dữ Liệu Đầu Vào (Data Readiness Assessment)

Theo kết quả rà soát từ Prompt 6 (file [gap_input_catalog.md](file:///d:/03.08/buoi_17/outputs/gap_input_catalog.md)):

```text
COMPLIANCE GAP DATA: INSUFFICIENT
DATA GAP: INTERNAL POLICY NOT FOUND
```

- **Thống kê corpus hiện tại**: `30` / 30 văn bản đều là **Văn bản quy phạm pháp luật bên ngoài** (`EXTERNAL_REQUIREMENT` - bao gồm các Luật, Nghị định, Thông tư của NHNN, Quốc hội, Chính phủ và Bộ Tài chính).
- **Trạng thái quy định nội bộ (`INTERNAL_POLICY`)**: `0` / 30 văn bản.

### 1.1 Nguyên Tắc Tuân Thủ Tuyệt Đối (Strict Compliance Rule)
Theo đúng chỉ thị tại Prompt 7:
> *Khi Prompt 6 báo dữ liệu chưa đủ, hệ thống **KHÔNG TUYỆT ĐỐI KHÔNG TỰ TẠO VĂN BẢN VÀ KHÔNG SINH KẾT LUẬN GIẢ**; thay vào đó tạo báo cáo DATA GAP và chuẩn hóa kiến trúc dữ liệu.*

---

## 2. Kiến Trúc và Luồng Thực Thi Của `ComplianceGapChecker` (`compliance_gap.py`)

Module `ComplianceGapChecker` đã được cài đặt hoàn chỉnh tại file [compliance_gap.py](file:///d:/03.08/buoi_17/scripts/compliance_gap.py) đáp ứng đầy đủ các tiêu chí quản trị nâng cao:

```text
[Input: NHNN Requirement Chunk]
              │
              ▼
  [Data Readiness Check] ─── (Missing INTERNAL_POLICY) ───► Output: CHUA_DU_BANG_CHUNG (DATA GAP)
              │
      (If Data Ready)
              │
              ▼
 [Hybrid + Rerank Secure Search] ◄─── [Graph Hints (Neo4j / Local Rel CSV)]
              │
              ▼
    [Evidence Package Builder]
   - External Req & Citation
   - Internal Evidence & Citation
              │
              ▼
   [Strict Classification Engine]
  - DAP_UNG / THIEU / CHENH_LECH / CHUA_DU_BANG_CHUNG
              │
              ▼
 [Human Review Enforcement: NEEDS_HUMAN_REVIEW] ───► [compliance_gap_results.csv]
```

### 2.1 Các Tiêu Chí Phân Loại Chặt Chẽ (Classification Logic)
1. **`DAP_UNG` (Compliant)**: Chỉ gán khi có bằng chứng quy định nội bộ đối ứng rõ ràng và đầy đủ. **Không gán nếu không có internal evidence**.
2. **`THIEU` (Missing/Non-compliant)**: Chỉ gán khi đã khẳng định quy định nội bộ có tồn tại nhưng bỏ sót yêu cầu bắt buộc của NHNN. **Không gán chỉ vì retriever chưa tìm thấy**.
3. **`CHENH_LECH` (Partial/Deviated)**: Gán khi quy định nội bộ có đề cập nhưng có sự sai lệch về chỉ số, hạn mức hoặc quy trình.
4. **`CHUA_DU_BANG_CHUNG` (Insufficient Evidence / Data Gap)**: Gán khi chưa tìm thấy trích dẫn nội bộ hoặc khi tập dữ liệu bị khuyết thiếu `INTERNAL_POLICY`.

### 2.2 Quy Tắc Quản Trị Đánh Giá (Governance Rules)
- **Không kết luận dựa trên Similarity Score**: Điểm tương đồng BM25/Vector Similarity chỉ dùng để xếp hạng ứng viên, không dùng làm kết luận tuân thủ.
- **Bắt buộc Human Review**: Tất cả bản ghi đầu ra bắt buộc có trường `review_status = "NEEDS_HUMAN_REVIEW"`. AI chỉ đóng vai trò hỗ trợ tập hợp bằng chứng (Evidence Package), quyết định cuối cùng thuộc về Chuyên viên Kiểm toán/Pháp chế.

---

## 3. Cấu Trúc File Xuất Kết Quả CSV (`compliance_gap_results.csv`)

File kết quả đã được khởi tạo chuẩn hóa tại [compliance_gap_results.csv](file:///d:/03.08/buoi_17/outputs/compliance_gap_results.csv) theo đúng 14 trường schema tối thiểu:

| Tên Trường (Field Name) | Định Dạng | Mô Tả |
| :--- | :--- | :--- |
| `gap_id` | `String` | Mã định danh phân tích gap duy nhất (VD: `GAP_DATA_INSUFFICIENT`) |
| `external_document_id` | `String` | Document ID của quy định NHNN bên ngoài |
| `external_chunk_id` | `String` | Chunk ID của yêu cầu NHNN |
| `external_requirement` | `Text` | Trích đoạn yêu cầu quy định NHNN |
| `external_citation` | `String` | Trích dẫn pháp lý nguồn NHNN |
| `internal_document_id` | `String` | Document ID của văn bản nội bộ đối ứng |
| `internal_chunk_id` | `String` | Chunk ID của quy định nội bộ đối ứng |
| `internal_evidence` | `Text` | Bằng chứng trích dẫn nội bộ tìm thấy |
| `internal_citation` | `String` | Trích dẫn pháp lý nội bộ |
| `classification` | `Enum` | `DAP_UNG` \| `THIEU` \| `CHENH_LECH` \| `CHUA_DU_BANG_CHUNG` |
| `reason` | `Text` | Giải thích lý do phân loại ngắn gọn |
| `confidence` | `Float` | Độ tin cậy của mô hình (0.0 - 1.0) |
| `review_status` | `Enum` | **Cố định**: `NEEDS_HUMAN_REVIEW` |
| `request_id` | `UUID` | Mã truy vết Audit Trail request |

---

## 4. Kết Luận Báo Cáo

```text
GAP CHECKER: PASS
HUMAN REVIEW REQUIRED: YES
```
