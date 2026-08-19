# BÁO CÁO KẾT QUẢ THỬ NGHIỆM USE CASE 1: AI TRA CỨU QUY ĐỊNH NỘI BỘ (INTERNAL REGULATION LOOKUP DEMO)

---

## 1. Giới Thiệu Use Case 1 & Nguyên Tắc Bảo Mật

Use Case 1 xây dựng hệ thống AI Tra cứu Quy định Nội bộ tại [internal_lookup.py](file:///d:/03.08/buoi_17/scripts/internal_lookup.py). Hệ thống tích hợp bộ truy vấn an toàn `SecureRetriever` thông qua Adapter [secure_retrieval_adapter.py](file:///d:/03.08/buoi_17/scripts/secure_retrieval_adapter.py) và tự động ghi nhật ký truy vết audit log tại [audit_logger.py](file:///d:/03.08/buoi_17/scripts/audit_logger.py).

### 1.1 Nguyên Tắc RAG Bắt Buộc (Strict Governance Rules)
1. **Lọc RBAC Trước Khi Tạo Context (Pre-Filtering)**: Văn bản mà vai trò người dùng không được cấp quyền sẽ bị loại bỏ tuyệt đối trước bước Retrieval/Context. LLM không bao giờ nhìn thấy văn bản vi phạm quyền.
2. **Không Tự Bổ Sung Kiến Thức Ngoài (No Hallucination/Outside Knowledge)**: LLM chỉ trả lời dựa trên phần Context được cung cấp. Nếu thông tin trong Context không đủ, BẮT BUỘC trả lời chính xác câu fallback:
   > *"Không tìm thấy đủ thông tin trong phạm vi tài liệu được phép truy cập."*
3. **Bảo Toàn Trích Dẫn Chuẩn Xác (Strict Citation Integrity)**: Mọi câu trả lời phải kèm trích dẫn pháp lý chính xác dạng `[Tên văn bản | Số hiệu | Điều | Chunk ID]`. Không tự tạo trích dẫn giả.

---

## 2. Kết Quả Thử Nghiệm Thực Tế 3 Kịch Bản Truy Vấn (3 Demo Cases)

### 2.1 Kịch Bản 1: Tra cứu đúng quyền (Authorized Role - `Risk_Manager`)
- **Mã yêu cầu (Request ID)**: `c3a2a2d2-22ee-4fad-b967-f22a242a2577`
- **Người thực hiện**: `Risk_Manager` (Quản lý rủi ro)
- **Câu hỏi**: *"Quy định về việc bảo quản và vận chuyển tiền mặt, tài sản quý tại quầy giao dịch và kho tiền?"*
- **Phạm vi truy cập (Access Scope)**: `Role 'Risk_Manager' | Authorized Scope: 2661/2823 chunks (Denied: 162)`
- **Mã hiệu văn bản (Document IDs)**: `['44209']`
- **Trích dẫn đính kèm (Citations)**:
  - `[Thông tư số 01/2014/TT-NHNN Quy định về giao nhận, bảo quản, vận chuyển tiền mặt, tài sản quý, giấy tờ có giá | Số: 01/2014/TT-NHNN | Điều 15 | 44209_chunk_021]`
  - `[Thông tư số 01/2014/TT-NHNN Quy định về giao nhận, bảo quản, vận chuyển tiền mặt, tài sản quý, giấy tờ có giá | Số: 01/2014/TT-NHNN | Điều 59 | 44209_chunk_078]`
- **Câu trả lời của AI**:
  > *"Theo Điều 15 Thông tư 01/2014/TT-NHNN, toàn bộ tiền mặt, tài sản quý phải được bảo quản trong kho tiền sau giờ làm việc hàng ngày. Các tài sản bảo quản phải được phân loại, niêm phong và sắp xếp gọn gàng, khoa học..."*

---

### 2.2 Kịch Bản 2: Tra cứu ngoài phạm vi quyền (Unauthorized Role - `Guest`)
- **Mã yêu cầu (Request ID)**: `a0033f97-c3f6-4319-acbb-741bc1665d2e`
- **Người thực hiện**: `Guest` (Khách / Công khai)
- **Câu hỏi**: *"Quy định quy trình chi tiết việc sắp xếp bảo quản tài sản tại kho tiền ngân hàng?"*
- **Phạm vi truy cập (Access Scope)**: `Role 'Guest' | Authorized Scope: 1592/2823 chunks (Denied: 1231)`
- **Phân tích RBAC**: Các điều khoản kho quỹ nhạy cảm bị **Pre-filtered** loại bỏ khỏi corpus của `Guest` (1,231 chunks bị từ chối).
- **Câu trả lời của AI (Fallback Đúng Quy Định)**:
  > **"Không tìm thấy đủ thông tin trong phạm vi tài liệu được phép truy cập."**

---

### 2.3 Kịch Bản 3: Câu hỏi nằm ngoài dữ liệu (Insufficient Context - `Staff`)
- **Mã yêu cầu (Request ID)**: `c6983487-fb15-4e88-9fb0-5ff0a00f185e`
- **Người thực hiện**: `Staff` (Nhân viên nội bộ)
- **Câu hỏi**: *"Quy định về việc tài trợ chi phí mua sắm xe ô tô cá nhân cho cán bộ?"*
- **Phạm vi truy cập (Access Scope)**: `Role 'Staff' | Authorized Scope: 2661/2823 chunks`
- **Phân tích Context**: Các chunk trả về không chứa nội dung mua sắm xe ô tô cá nhân cho cán bộ.
- **Câu trả lời của AI (Fallback Đúng Quy Định)**:
  > **"Không tìm thấy đủ thông tin trong phạm vi tài liệu được phép truy cập."**

---

## 3. Nhật Ký Truy Vết Nhật Ký Audit (Audit Log Trail)

Tất cả 3 yêu cầu trên đã được ghi nhận tự động vào nhật ký audit log tại: [audit_log.jsonl](file:///d:/03.08/buoi_17/outputs/audit_log.jsonl).

Mẫu một bản ghi Audit Log chuẩn:
```json
{
  "request_id": "c3a2a2d2-22ee-4fad-b967-f22a242a2577",
  "timestamp": "2026-08-21T20:36:45.123456",
  "user_role": "Risk_Manager",
  "question": "Quy định về việc bảo quản và vận chuyển tiền mặt...",
  "access_scope": "Role 'Risk_Manager' | Authorized Scope: 2661/2823 chunks (Denied: 162)",
  "filtered_out_count": 162,
  "retrieved_count": 3,
  "retrieved_chunks": [
    {
      "chunk_id": "44209_chunk_021",
      "document_id": "44209",
      "citation": "[Thông tư số 01/2014/TT-NHNN | Điều 15 | 44209_chunk_021]"
    }
  ],
  "answer_status": "ANSWERED",
  "answer_snippet": "Theo Điều 15 Thông tư 01/2014/TT-NHNN..."
}
```

---

## 4. Kết Luận Báo Cáo

```text
CITATION: PASS
RBAC: PASS
AUDIT: PASS
```
