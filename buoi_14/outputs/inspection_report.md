# BÁO CÁO KIỂM TRA TIỀN KHẢO SÁT (PRE-CHECK INSPECTION REPORT)
**Buổi 14: Hybrid Search + Reranking + Mini Knowledge Graph**

---

## 1. Cấu Trúc Thư Mục `buoi_14/`

- **Working Directory (Thư mục làm việc):** `d:\03.08\buoi_14`
- **Cấu trúc thư mục hiện tại:**
  ```text
  d:\03.08\buoi_14/
  └── outputs/
      └── inspection_report.md
  ```
- **Đường dẫn dữ liệu nguồn:** `../kb+hops/` (Thông qua Junction / link trực tiếp tới thư mục dữ liệu gốc `d:\03.08\ner_kb`, không sao chép, di chuyển, sửa đổi hay ghi đè dữ liệu gốc).

---

## 2. Kiểm Tra Các File Hiện Có Trong `buoi_14/`

- **File `.py`:** 0 file
- **File `.md`:** 1 file (`outputs/inspection_report.md`)
- **File `.csv`:** 0 file (Tất cả dữ liệu nguồn được đọc từ `../kb+hops/`)
- **File `.json`:** 0 file
- **File `requirements.txt`:** 0 file (Dùng chung môi trường ảo `.venv` tại thư mục gốc `d:\03.08\.venv`)
- **File `.env`:** 0 file (Dùng `.env` tại gốc `d:\03.08\.env`)

---

## 3. Báo Cáo Chi Tiết 3 File CSV Nguồn Trong `../kb+hops/`

Đã thực hiện truy cập và đọc trực tiếp đúng 3 file CSV theo đúng quy định (không sửa đổi, không tạo bản sao):

### 3.1. `../kb+hops/metadata.csv`
- **Đường dẫn đọc trực tiếp:** `../kb+hops/metadata.csv`
- **Encoding:** `utf-8`
- **Số dòng:** 30 dòng
- **Số cột:** 17 cột
- **Danh sách cột:**
  1. `id`
  2. `title`
  3. `so_ky_hieu`
  4. `ngay_ban_hanh`
  5. `loai_van_ban`
  6. `ngay_co_hieu_luc`
  7. `ngay_het_hieu_luc`
  8. `nguon_thu_thap`
  9. `ngay_dang_cong_bao`
  10. `nganh`
  11. `linh_vuc`
  12. `co_quan_ban_hanh`
  13. `chuc_danh`
  14. `nguoi_ky`
  15. `pham_vi`
  16. `thong_tin_ap_dung`
  17. `tinh_trang_hieu_luc`
- **Trùng lặp (Duplicates):**
  - Trùng lặp dòng toàn phần: 0
  - Trùng lặp khóa `id`: 0 (Khóa `id` hoàn toàn duy nhất cho cả 30 văn bản)
- **Giá trị rỗng (Null values):**
  - `id`: 0 (0.0%)
  - `title`: 0 (0.0%)
  - `so_ky_hieu`: 0 (0.0%)
  - `ngay_ban_hanh`: 0 (0.0%)
  - `loai_van_ban`: 0 (0.0%)
  - `ngay_co_hieu_luc`: 2 (6.67%)
  - `ngay_het_hieu_luc`: 28 (93.33%)
  - `nguon_thu_thap`: 10 (33.33%)
  - `ngay_dang_cong_bao`: 22 (73.33%)
  - `nganh`: 5 (16.67%)
  - `linh_vuc`: 3 (10.00%)
  - `co_quan_ban_hanh`: 0 (0.0%)
  - `chuc_danh`: 1 (3.33%)
  - `nguoi_ky`: 1 (3.33%)
  - `pham_vi`: 0 (0.0%)
  - `thong_tin_ap_dung`: 30 (100.0%)
  - `tinh_trang_hieu_luc`: 0 (0.0%)
- **Khóa có thể sử dụng (Usable Keys):**
  - Primary Key: `id` (Dạng chuỗi ID như `"166170"`, `"112025"`).
  - Kết nối 1:1 với `content.csv` qua `id`.
  - Kết nối 1:N với `relationships.csv` qua `source` và `target`.
- **Trường text phù hợp Retrieval:** `title`, `so_ky_hieu`, `linh_vuc`, `nganh`, `loai_van_ban`.
- **Metadata phù hợp Citation:** `title`, `so_ky_hieu`, `co_quan_ban_hanh`, `ngay_ban_hanh`, `loai_van_ban`, `nguoi_ky`, `chuc_danh`, `tinh_trang_hieu_luc`, `ngay_co_hieu_luc`.

---

### 3.2. `../kb+hops/content.csv`
- **Đường dẫn đọc trực tiếp:** `../kb+hops/content.csv`
- **Encoding:** `utf-8`
- **Số dòng:** 30 dòng
- **Số cột:** 2 cột
- **Danh sách cột:**
  1. `id`
  2. `content_html`
- **Trùng lặp (Duplicates):**
  - Trùng lặp dòng toàn phần: 0
  - Trùng lặp khóa `id`: 0 (Duy nhất 30 ID)
- **Giá trị rỗng (Null values):**
  - `id`: 0 (0.0%)
  - `content_html`: 0 (0.0%)
- **Khóa có thể sử dụng (Usable Keys):**
  - Primary Key: `id` (Khớp 100% tập ID của `metadata.csv`).
- **Trường text phù hợp Retrieval:** `content_html` (Văn bản thô/HTML chứa toàn bộ nội dung điều khoản luật, dùng để trích xuất text/chunking phục vụ BM25, Embedding & Hybrid Retrieval).
- **Metadata phù hợp Citation:** Không chứa trực tiếp metadata trích dẫn; sử dụng khóa `id` liên kết sang `metadata.csv` để hiển thị trích dẫn chi tiết.

---

### 3.3. `../kb+hops/relationships.csv`
- **Đường dẫn đọc trực tiếp:** `../kb+hops/relationships.csv`
- **Encoding:** `utf-8`
- **Số dòng:** 329 dòng
- **Số cột:** 6 cột
- **Danh sách cột:**
  1. `source`
  2. `target`
  3. `relationship_type`
  4. `method`
  5. `confidence`
  6. `evidence`
- **Trùng lặp (Duplicates):**
  - Trùng lặp dòng toàn phần: 0
  - Trùng lặp Bộ 3 (`source`, `target`, `relationship_type`): 0
- **Giá trị rỗng (Null values):**
  - Không có cột nào bị rỗng (0 nulls across all 6 columns).
- **Khóa có thể sử dụng (Usable Keys):**
  - Composite Key: (`source`, `target`, `relationship_type`).
  - `source`: Mã văn bản nguồn (kết nối tới `id` trong `metadata.csv` / `content.csv`).
  - `target`: Mã văn bản / Thực thể đích (`doc_...`, `ent_...`, tên cơ quan, người ký, lĩnh vực).
- **Phân loại quan hệ (`relationship_type`):**
  - `THAM_CHIEU`: 163 quan hệ
  - `SUA_DOI_BO_SUNG`: 40 quan hệ
  - `BAN_HANH_BOI`: 30 quan hệ
  - `KY_BOI`: 30 quan hệ
  - `AP_DUNG_CHO`: 30 quan hệ
  - `THUOC_LINH_VUC`: 30 quan hệ
  - `THAY_THE_BOI`: 6 quan hệ
- **Trường text phù hợp Retrieval:** `evidence` (Đoạn văn bằng chứng trích dẫn lý do liên kết), `relationship_type` (Loại liên kết giữa văn bản và thực thể).
- **Metadata phù hợp Citation:** `relationship_type`, `method`, `confidence`, `evidence` (Phục vụ truy vết quan hệ Graph RAG & trích dẫn đa chặng Multi-hop).

---

## 4. Kiểm Tra Code Hiện Có & Rủi Ro An Toàn Dữ Liệu

- **File code hiện có trong `buoi_14/`:** Chưa có file script `.py` nào.
- **Rà soát lệnh nguy hiểm:**
  - `os.remove`: Không phát hiện
  - `shutil.rmtree`: Không phát hiện
  - `open(..., "w")`: Không phát hiện
  - `DELETE`: Không phát hiện
  - `DROP`: Không phát hiện
  - `DETACH DELETE`: Không phát hiện
- **Đánh giá rủi ro phá hủy dữ liệu:** Hoàn toàn an toàn. Không có thao tác ghi đè hay xóa dữ liệu nào được thực thi.

---

## 5. Kiểm Tra Môi Trường Lập Trình (Environment Check)

- **Python Version:** Python `3.14.2`
- **Môi trường ảo (`.venv`):** Đã kích hoạt môi trường ảo `d:\03.08\.venv`
- **Thư viện Pandas:** `import pandas` thành công (Version `3.0.5`)

---

## 6. PROJECT PRE-CHECK SUMMARY

```text
PROJECT PRE-CHECK

Working root: d:\03.08\buoi_14
Data: Validated 3 CSV source files (metadata.csv, content.csv, relationships.csv) in ../kb+hops/
Existing code: Clean (0 code files, no destructive commands)
Environment: Python 3.14.2 (.venv active) with pandas 3.0.5 verified
Potential risks: None
Safe to continue: YES
```
