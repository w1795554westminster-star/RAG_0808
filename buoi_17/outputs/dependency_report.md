# BÁO CÁO ĐÁNH GIÁ PHỤ THUỘC VÀ TÁI SỬ DỤNG DỮ LIỆU/CODE BUỔI 16 CHO BUỔI 17
*(Dependency and Reuse Inspection Report)*

---

## 1. Kiểm tra Dữ liệu Nguồn (Source Data Inspection)

Dữ liệu kiểm tra theo yêu cầu đặt tại:
- `../buoi_16/data/processed/chunks_secure.csv`
- `../buoi_16/data/processed/chunks_normalized.csv`

### 1.1 Thông tin Chi tiết Tập Dữ liệu `chunks_secure.csv`
- **Số lượng dòng (Row count)**: `2,823` dòng (không kể dòng header). *(Ghi chú: Thư mục `buoi_17/data/chunks_combined_secure.csv` có sẵn phiên bản thu gọn 811 dòng).*
- **Số lượng cột (Column count)**: `20` cột.
- **Danh sách cột chi tiết**:
  1. `chunk_id`
  2. `document_id`
  3. `text`
  4. `source_file`
  5. `title`
  6. `document_type` (tương đương *loai_van_ban*)
  7. `chapter`
  8. `section`
  9. `article`
  10. `clause`
  11. `effective_date`
  12. `status`
  13. `so_ky_hieu`
  14. `co_quan_ban_hanh`
  15. `ngay_ban_hanh`
  16. `linh_vuc`
  17. `nganh`
  18. `nguoi_ky`
  19. `chuc_danh`
  20. `allowed_roles` *(Cột phân quyền RBAC)*

### 1.2 Kiểm tra sự hiện diện của các trường yêu cầu
| Trường dữ liệu | Trạng thái trong CSV | Ghi chú / Giá trị mẫu |
| :--- | :---: | :--- |
| `chunk_id` | **CÓ** | Mã định danh duy nhất (VD: `44209_chunk_001`) |
| `document_id` | **CÓ** | Số hiệu văn bản gốc (VD: `44209`) |
| `citation` | **CƠ CHẾ ĐỘNG** | Được sinh động trong retriever/citation formatter: `[Tên văn bản \| Số hiệu \| Điều \| Chunk ID]` |
| `title` | **CÓ** | Tên văn bản pháp lý |
| `loai_van_ban` | **CÓ** | Trường `document_type` chứa thông tin loại văn bản (VD: `Thông tư`, `Quyết định`) |
| `co_quan_ban_hanh` | **CÓ** | Cơ quan phát hành (VD: `Ngân hàng Nhà nước`) |
| `ngay_ban_hanh` | **CÓ** | Ngày ban hành văn bản |
| `allowed_roles` | **CÓ** | Danh sách role dạng JSON String (VD: `["Admin", "HR", "Risk_Manager", "Staff"]`) |

---

## 2. So sánh `chunks_secure.csv` vs `chunks_normalized.csv`

- **Số dòng `chunks_normalized.csv`**: `2,823` dòng.
- **Số cột `chunks_normalized.csv`**: `19` cột.
- **Kết luận so sánh**:
  $$\text{chunks\_secure.csv} = \text{chunks\_normalized.csv} + \text{allowed\_roles}$$
- **Xác nhận**: Dữ liệu giữa hai file hoàn toàn trùng khớp 100% về số dòng (2,823 dòng) và toàn bộ 19 trường dữ liệu nội dung/metadata. File `chunks_secure.csv` chỉ bổ sung duy nhất cột `allowed_roles` phục vụ lọc phân quyền RBAC.

---

## 3. Kiểm tra Code `SecureRetriever` của Buổi 16

Code `SecureRetriever` được phát hiện và kiểm tra tại:
- **File / Module**: `buoi_16/src/secure_retriever.py` (hoặc `src.secure_retriever`)

### 3.1 Cấu trúc Hàm / Class Chính
- **Class chính**: `class SecureRetriever`
- **Phương thức chính**:
  ```python
  def retrieve(self, question: str, user_roles: list, method: str = "hybrid_rerank", top_k: int = 5, candidate_k: int = 20) -> tuple
  ```
- **Hàm helper độc lập**: `retrieve_secure(...)`

### 3.2 Đặc tả I/O và Cơ chế Phân quyền (RBAC Logic)
- **Input Role**: Tham số `user_roles: list` (Danh sách các vai trò của người dùng hiện tại, ví dụ: `['Guest']`, `['HR', 'Staff']`, `['Admin']`).
- **Output**: Tuple dạng `(filtered_results_list, total_filtered_out_count)`. Mỗi phần tử trong `filtered_results_list` là một `dict` chứa đầy đủ các trường: `rank`, `chunk_id`, `document_id`, `text`, `score`, `citation`, `retrieval_method`, `allowed_roles`, v.v.
- **Cơ chế Lọc (Filter Timing)**: **PRE-FILTERING (Lọc TRƯỚC khi Retrieval)**.
  - *Duyệt qua corpus ban đầu*:
    ```python
    auth_mask = self.df_corpus['allowed_roles'].apply(lambda r: is_role_authorized(r, user_roles))
    df_auth = self.df_corpus[auth_mask].copy()
    ```
  - *Tác động*: Tất cả các search engine (BM25, Dense, Hybrid, Reranker) đều chỉ khởi tạo và tìm kiếm trên tập `df_auth` đã được loại bỏ hoàn toàn các chunk người dùng không có quyền truy cập. Các văn bản không có quyền xem sẽ không bao giờ xuất hiện trong Context gửi cho LLM.
- **Duy trì định danh & trích dẫn**: **CÓ**. Các thông tin `document_id`, `chunk_id`, `citation`, `title`, `text` được bảo toàn nguyên vẹn trong kết quả trả về.

---

## 4. Kế hoạch Tái sử dụng (Reuse Plan)

1. **Không sửa dữ liệu nguồn**: Giữ nguyên `chunks_secure.csv` và `chunks_normalized.csv`.
2. **Không tạo Policy mới & Không viết lại Retriever**: Tái sử dụng trực tiếp class `SecureRetriever` từ `buoi_16/src/secure_retriever.py`.
3. **Adapter (nếu cần)**: Trong các bước sau của Buổi 17, nếu ứng dụng Streamlit hoặc các script `internal_lookup.py` / `compliance_gap.py` yêu cầu chuẩn hóa interface đầu ra, sẽ tạo `buoi_17/scripts/secure_retrieval_adapter.py` để bọc lại `SecureRetriever` mà không nhân bản hay viết lại bộ truy vấn.

---

## 5. Kết luận Chỉ số Tổng hợp

```text
SOURCE DATA: PASS
RBAC DATA AVAILABLE: YES
SECURE RETRIEVER REUSABLE: YES
REUSE PLAN: Tái sử dụng nguyên trạng SecureRetriever từ buoi_16/src/secure_retriever.py, lọc RBAC pre-filter dựa trên cột allowed_roles của chunks_secure.csv.
```
