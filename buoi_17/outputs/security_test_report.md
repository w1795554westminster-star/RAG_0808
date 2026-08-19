# BÁO CÁO KIỂM THỬ BẢO MẬT HỆ THỐNG - BUỔI 17

**Ngày kiểm thử:** 2026-08-21  
**Người thực hiện:** Security Tester AI  
**Môi trường:** Workspace `d:\03.08\buoi_17`  
**Dữ liệu kiểm thử:** `../buoi_16/data/processed/chunks_secure.csv` (2,823 chunks)

---

## 1. MỤC TIÊU VÀ PHẠM VI KIỂM THỬ BẢO MẬT
Kiểm thử toàn diện 10 yêu cầu an toàn thông tin và phân quyền của hệ thống Tra cứu Quy định Nội bộ & Compliance Gap Checker (Buổi 17):
1. Role được phép truy cập nội dung được cấp quyền (`Authorized Role -> PASS`).
2. Role không được phép tuyệt đối không lộ thông tin hoặc trích dẫn (`Unauthorized Role -> DENY`).
3. Tài liệu bị cấm tuyệt đối không được đưa vào LLM Context.
4. Role không xác định (`Unknown Role`) mặc định bị từ chối 100% (`Default Deny`).
5. Nhật ký truy vết (`Audit Log`) ghi nhận đầy đủ cả yêu cầu thành công (`ANSWERED`) và bị từ chối (`DENIED_RBAC` / `INSUFFICIENT_CONTEXT`).
6. Nhật ký kiểm toán và dữ liệu xuất ra không chứa thông tin nhạy cảm (API Key, Secret, Password).
7. Trích dẫn pháp lý (`Citation`) tồn tại và chuẩn hóa.
8. Báo cáo Gap Compliance phải chứa bằng chứng thực tế hoặc gắn nhãn `CHUA_DU_BANG_CHUNG`.
9. 100% kết quả Gap được đánh dấu `NEEDS_HUMAN_REVIEW` trước khi ban hành.
10. Trạng thái kết nối Knowledge Graph Neo4j báo thực tế, không giả lập.

---

## 2. KẾT QUẢ KIỂM THỬ CHI TIẾT (10/10 TEST CASES)

| STT | Tên bài test bảo mật | Trạng thái | Chi tiết thực thi |
| :--- | :--- | :---: | :--- |
| **TEST 1** | Role được phép $\rightarrow$ PASS | **PASS** | Role `Staff` thực hiện tra cứu câu hỏi về bảo quản tài sản tại kho tiền. Hệ thống cho phép truy cập các chunk phù hợp và tổng hợp câu trả lời đầy đủ (431 ký tự). |
| **TEST 2** | Role không được phép $\rightarrow$ Không lộ text/citation | **PASS** | Role `Guest` truy vấn quy trình bảo quản tiền mặt chi tiết tại kho tiền. Chunk bảo mật `44209_chunk_021` bị lọc 100%. Trả về thông báo chuẩn: `"Không tìm thấy đủ thông tin trong phạm vi tài liệu được phép truy cập."` |
| **TEST 3** | Tài liệu bị cấm không vào LLM context | **PASS** | Kiểm tra 100% context được truyền vào LLM cho vai trò `Guest`. Không xuất hiện bất kỳ chunk nào thiếu quyền `Guest` trong danh sách `allowed_roles` (0 unauthorized chunks). |
| **TEST 4** | Unknown role $\rightarrow$ Default DENY | **PASS** | Truy vấn với role không tồn tại `UnknownRole_12345`. Hệ thống tự động lọc bỏ toàn bộ 2,823/2,823 chunks (Default Deny) và trả về 0 kết quả context. |
| **TEST 5** | Audit ghi SUCCESS và DENIED | **PASS** | File [audit_log.jsonl](file:///d:/03.08/buoi_17/outputs/audit_log.jsonl) ghi lại chính xác các trạng thái `ANSWERED` (cho Staff) và `DENIED_RBAC` / `INSUFFICIENT_CONTEXT` (cho Guest/UnknownRole). |
| **TEST 6** | Log không chứa password/API key | **PASS** | Quét toàn bộ nội dung file audit log và output. Không phát hiện bất kỳ chuỗi API Key (`AQ.Ab8RN6J...`), Secret Key hay Password nào. |
| **TEST 7** | Citation tồn tại & chuẩn hóa | **PASS** | Tất cả các kết quả trích xuất cho các role được phép đều bảo toàn đầy đủ các trường `citation`, `document_id`, `chunk_id`. |
| **TEST 8** | Gap có evidence hoặc CHUA_DU_BANG_CHUNG | **PASS** | Thuật toán Gap Checker trả về bằng chứng đối soát thực tế hoặc gắn nhãn `CHUA_DU_BANG_CHUNG` do thiếu văn bản nội bộ thực tế trong corpus. |
| **TEST 9** | Mọi gap result NEEDS_HUMAN_REVIEW | **PASS** | 100% kết quả Gap Compliance xuất ra đều tự động gán trường `review_status = "NEEDS_HUMAN_REVIEW"`. |
| **TEST 10** | Neo4j down thì báo thật, không giả | **PASS** | Thực hiện kiểm tra socket thực tế tới Port 7687 (`127.0.0.1`). Báo cáo chính xác trạng thái `INACTIVE (Connection Refused)` thay vì giả lập kết nối thành công. |

---

## 3. TỔNG KẾT VÀ XÁC NHẬN BẢO MẬT

Hệ thống Buổi 17 đã vượt qua toàn bộ 10/10 bài kiểm thử an ninh thông tin, đáp ứng đầy đủ các tiêu chuẩn bảo mật RBAC, kiểm toán audit trail, và an toàn context LLM.

```text
SECURITY TESTS: PASS
```
