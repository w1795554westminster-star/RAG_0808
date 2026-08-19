# BÁO CÁO ĐÁNH GIÁ VÀ TÁI SỬ DỤNG PHÂN QUYỀN RBAC TỪ `ALLOWED_ROLES` (BUỔI 17)
*(RBAC Reuse and Pre-Filtering Validation Report)*

---

## 1. Phân Tích Dữ Liệu Phân Quyền `allowed_roles`

Dữ liệu được kiểm tra trực tiếp trên tập: `../buoi_16/data/processed/chunks_secure.csv` (2,823 chunks).

### 1.1 Tính Khả Thi & Thống Nhất Định Dạng (Parsing Stability)
- **Tổng số chunks kiểm tra**: `2,823` chunks.
- **Số lỗi Parse JSON**: `0` lỗi (Đạt tỷ lệ parse ổn định **100%**).
- **Định dạng dữ liệu**: Chuỗi JSON Array hợp lệ (VD: `["Admin", "HR", "Risk_Manager", "Legal_Officer", "Bank_Staff", "Staff", "Guest"]`).

### 1.2 Danh Sách Vai Trò (Roles) & Thống Kê Phân Phối
Tập dữ liệu bao gồm 7 vai trò chính với tỷ lệ phân bổ như sau:

| Vai Trò (Role) | Số lượng Chunk được phép xem | Tỷ lệ % Corpus | Mức độ bảo mật |
| :--- | :---: | :---: | :--- |
| `Admin` | `2,823` | `100.0%` | Quyền toàn cục |
| `Risk_Manager` | `2,661` | `94.3%` | Quản lý rủi ro |
| `Legal_Officer` | `2,661` | `94.3%` | Pháp chế |
| `Bank_Staff` | `2,661` | `94.3%` | Nhân viên ngân hàng |
| `Staff` | `2,661` | `94.3%` | Nhân viên nội bộ |
| `HR` | `1,754` | `62.1%` | Nhân sự & chế độ |
| `Guest` | `1,592` | `56.4%` | Khách / Công khai |

### 1.3 Phân Tích Chunks Phân Quyền Nhiều Vai Trò & Hạn Chế Quyền
- **Chunks cho nhiều vai trò (Multi-role chunks)**: `2,823` chunks (100% chunks có từ 1 vai trò trở lên).
- **Chunks hạn chế quyền (Hạn chế với `Guest`)**: `1,231` chunks (chiếm **43.6%** tổng corpus). Đây là các quy định nội bộ nhạy cảm về kiểm soát rủi ro, vận chuyển tiền mặt, kho quỹ... chỉ dành cho nhân viên nội bộ hoặc cấp quản lý, hoàn toàn ẩn với vai trò `Guest`.

---

## 2. Kiểm Tra Xử Lý Vai Trò Khôn Xác Định (Unknown Role & Default Deny)

- **Thử nghiệm**: Đưa vào danh sách vai trò không hợp lệ / chưa định nghĩa: `['UnknownRole_XYZ']`.
- **Kết quả kiểm tra**:
  - Số lượng chunks được cấp quyền: `0` / `2,823` chunks (0.0%).
  - Số lượng chunks bị loại bỏ (Filtered out): `2,823` / `2,823` chunks (100.0%).
- **Kết luận**: Thuật toán `is_role_authorized()` áp dụng nguyên tắc **Default Deny (Từ chối mặc định)** tuyệt đối đối với tất cả vai trò nằm ngoài danh sách được ủy quyền.

---

## 3. Thử Nghiệm Thực Tế Với `SecureRetriever` Trên 5 Vai Trò Người Dùng

Thực thi cùng câu hỏi truy vấn:  
**Query:** *"Quy định bảo quản và vận chuyển tiền mặt, tài sản quý"*  
Phương thức truy vấn: `hybrid_rerank` (BM25 + Dense RRF + Reranker)

### 3.1 Bảng Kết Quả Thử Nghiệm Trên Tập Dữ Liệu `buoi_16` (2,823 chunks)

| Vai trò thử nghiệm (User Role) | Quy mô Corpus được phép | Số Chunk bị lọc bỏ | Chunk Rank 1 Trả về | `allowed_roles` của Top 1 Chunk |
| :--- | :---: | :---: | :--- | :--- |
| **`Admin`** | 2,823 / 2,823 | 0 | `44209_chunk_023` | `['Admin', 'HR', 'Risk_Manager', 'Legal_Officer', 'Bank_Staff', 'Staff', 'Guest']` |
| **`Risk_Manager`** | 2,661 / 2,823 | 162 | `44209_chunk_023` | `['Admin', 'HR', 'Risk_Manager', 'Legal_Officer', 'Bank_Staff', 'Staff', 'Guest']` |
| **`Staff`** | 2,661 / 2,823 | 162 | `44209_chunk_023` | `['Admin', 'HR', 'Risk_Manager', 'Legal_Officer', 'Bank_Staff', 'Staff', 'Guest']` |
| **`HR`** | 1,754 / 2,823 | 1,069 | `44209_chunk_023` | `['Admin', 'HR', 'Risk_Manager', 'Legal_Officer', 'Bank_Staff', 'Staff', 'Guest']` |
| **`Guest`** | 1,592 / 2,823 | 1,231 | `44209_chunk_023` | `['Admin', 'HR', 'Risk_Manager', 'Legal_Officer', 'Bank_Staff', 'Staff', 'Guest']` |
| **`UnknownRole`** | 0 / 2,823 | 2,823 | *(Rỗng)* | N/A |

### 3.2 Bảng Kết Quả Thử Nghiệm Trên Tập Dữ Liệu `buoi_17` (811 chunks)

| Vai trò (User Role) | Quy mô Corpus được phép | Số Chunk bị lọc bỏ | Chunk Rank 1 Trả về | Đánh giá thay đổi Context |
| :--- | :---: | :---: | :--- | :--- |
| **`Admin`** | 811 / 811 | 0 | `doc_44209_điều_47__quy_trình_vận_chuyển_47` | Truy cập đầy đủ |
| **`HR`** | 544 / 811 | 267 | `doc_44209_điều_68__quyền_lợi_đối_với_cán_bộ_kho_quỹ_68` | Chuyển sang chunk HR kho quỹ |
| **`Risk_Manager`** | 429 / 811 | 382 | `doc_44209_điều_47__quy_trình_vận_chuyển_47` | Truy cập đúng điều vận chuyển |
| **`Staff`** | 418 / 811 | 393 | `doc_44209_điều_47__quy_trình_vận_chuyển_47` | Truy cập đúng điều vận chuyển |
| **`Guest`** | 162 / 811 | 649 | `doc_166269_điều_88__quản_lý__sử_dụng_tài_sản_88` | **Bị ẩn Điều 47**, tự động chuyển sang tài sản công khai |

### 3.3 Xác Nhận Cơ Chế Pre-Filtering
- `SecureRetriever` thực hiện lọc phân quyền **TRƯỚC** khi chạy bất kỳ thuật toán tìm kiếm nào:
  ```python
  auth_mask = self.df_corpus['allowed_roles'].apply(lambda r: is_role_authorized(r, user_roles))
  df_auth = self.df_corpus[auth_mask].copy()
  ```
- **Kết quả**: Tất cả chỉ số BM25, Dense Cosine, RRF Ranks và Cross-Encoder Rerank đều khởi tạo duy nhất trên tập `df_auth`. Văn bản không đủ quyền **hoàn toàn không thể lọt vào Context của LLM**.

---

## 4. Kết Luận Báo Cáo

```text
RBAC REUSED: YES
FILTER BEFORE RETRIEVAL: PASS
UNKNOWN ROLE DEFAULT DENY: PASS
```
