# SPEC Buổi 06

Tài liệu hướng dẫn AI Agent phục vụ phát triển project Buổi 06.

---

## 1. Workspace Rules

### Chỉ được phép đọc:
- `RAG/rag_foundation/buoi_05/output/chunks/`
- `RAG/rag_foundation/buoi_05/.venv/`
- `RAG/rag_foundation/buoi_06/`

### Tuyệt đối KHÔNG đọc:
- Source code của Buổi 05
- README của các buổi trước
- Notebook
- Git history
- Các thư mục khác trong workspace

> **Nguyên tắc:** Buổi 5 được xem là black box. Không reverse engineering, không phân tích cách Buổi 5 hoạt động.

---

## 2. Python Environment

- Sử dụng đúng Python interpreter trong: `RAG/rag_foundation/buoi_05/.venv/`
- **Không** tạo virtual environment (venv) mới.

---

## 3. Package Requirements

Chỉ cài đặt và sử dụng các package sau:
- `streamlit`
- `google-genai`
- `chromadb`
- `psycopg`
- `python-dotenv`

> **Lưu ý:** Không cài đặt thêm bất kỳ framework hay thư viện nào khác.

---

## 4. Coding Style & Architecture

- **Ưu tiên:** Ít file, ít class, ít function, code dễ đọc và đơn giản nhất có thể.
- **Tối kỵ (Không tạo):** 
  - Repository pattern
  - Service layer
  - Dependency injection
  - Factory pattern
  - Plugin architecture

---

## 5. Scope & Features

Chỉ tập trung vào 4 chức năng cốt lõi:
1. **Index**
2. **Retrieval**
3. **Answer**
4. **Streamlit UI**

> Không phát triển bất kỳ tính năng nào vượt ngoài phạm vi yêu cầu trên.

---

## 6. Error Handling

- Chỉ sử dụng `try/except` tối thiểu tại các điểm cần thiết.
- **Không cần:** retry mechanism, logging system, monitoring.

---

## 7. Security

- **Tuyệt đối không in (print/log/display):** API Key, password, secret hay các thông tin nhạy cảm.

---

## 8. Code Size Limit

- **Mục tiêu:** Tổng kích thước code khoảng **300 – 500 dòng** Python.
- **Giới hạn:** Nếu tổng số dòng vượt quá 700 dòng, bắt buộc phải tái cấu trúc và đơn giản hóa thiết kế.
