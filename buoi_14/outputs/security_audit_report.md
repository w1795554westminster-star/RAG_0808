# BÁO CÁO KIỂM ĐỊNH BẢO MẬT DỮ LIỆU TỰ ĐỘNG (AUTOMATED SECURITY AUDIT REPORT)
**Buổi 15: Kiểm soát Truy cập dựa trên Vai trò (Data-Level RBAC)**

---

## 1. Tổng Quan Kết Quả Kiểm Định (Audit Executive Summary)

- **Tổng số bài kiểm thử thực thi:** 5 test cases
- **Số bài test vượt qua (PASSED):** 5 / 5
- **Tỷ lệ an toàn dữ liệu:** `100.0%`
- **Tệp dữ liệu bảo mật:** `data/processed/chunks_secure.csv`
- **Trạng thái chứng nhận:** `CERTIFIED SECURE — NO DATA LEAKAGE DETECTED`

---

## 2. Bảng Kết Quả Chi Tiết Từng Test Case (Test Matrix)

| Mã Test | Tên Bài Kiểm Thử | Vai Trò Không Quyền (Unauthorized) | Vai Trò Có Quyền (Authorized) | Trạng Thái |
| :---: | :--- | :---: | :---: | :---: |
| **TC01** | HR Confidentiality Protection | `Guest` | `HR, Admin` | **PASS** |
| **TC02** | Credit & Risk Management Boundaries | `Guest` | `Risk_Manager, Legal_Officer, Admin` | **PASS** |
| **TC03** | Secret Vault Protocol Confidentiality | `Guest, Bank_Staff` | `Legal_Officer, Admin` | **PASS** |
| **TC04** | Public Legal Regulation Accessibility | `None` | `Guest, Bank_Staff, Admin` | **PASS** |
| **TC05** | Pre-Reranking Filter Leakage Audit | `Bank_Staff` | `HR, Admin` | **PASS** |

---

## 3. Bằng Chứng Kiểm Thử Chi Tiết (Detailed Audit Evidence)

### 3.1. Test Case [TC01]: HR Confidentiality Protection
- **Truy vấn kiểm thử:** `"Bảng lương cấp quản lý và quy hoạch cán bộ nội bộ"`
- **Target Chunk ID:** `44209_chunk_051`
- **Kết quả kiểm tra chống rò rỉ:** Unauthorized attempt (['Guest']) returned 0 forbidden chunks. Authorized attempt (['HR', 'Admin']) retrieved 10 compliant chunks.
- **Đánh giá:** `PASS` — Không xảy ra hiện tượng rò rỉ dữ liệu qua BM25, Dense hay Cross-Encoder Reranker.

### 3.2. Test Case [TC02]: Credit & Risk Management Boundaries
- **Truy vấn kiểm thử:** `"Quy định về hạn mức tín dụng và thẩm định rủi ro nợ xấu"`
- **Target Chunk ID:** `44209_chunk_000`
- **Kết quả kiểm tra chống rò rỉ:** Unauthorized attempt (['Guest']) returned 0 forbidden chunks. Authorized attempt (['Risk_Manager', 'Legal_Officer', 'Admin']) retrieved 10 compliant chunks.
- **Đánh giá:** `PASS` — Không xảy ra hiện tượng rò rỉ dữ liệu qua BM25, Dense hay Cross-Encoder Reranker.

### 3.3. Test Case [TC03]: Secret Vault Protocol Confidentiality
- **Truy vấn kiểm thử:** `"Xử lý khi làm mất hoặc lộ bí mật chìa khóa kho tiền két sắt"`
- **Target Chunk ID:** `44209_chunk_051`
- **Kết quả kiểm tra chống rò rỉ:** Unauthorized attempt (['Guest', 'Bank_Staff']) returned 0 forbidden chunks. Authorized attempt (['Legal_Officer', 'Admin']) retrieved 10 compliant chunks.
- **Đánh giá:** `PASS` — Không xảy ra hiện tượng rò rỉ dữ liệu qua BM25, Dense hay Cross-Encoder Reranker.

### 3.4. Test Case [TC04]: Public Legal Regulation Accessibility
- **Truy vấn kiểm thử:** `"Phạm vi điều chỉnh Thông tư 01/2014/TT-NHNN quy định chung"`
- **Target Chunk ID:** `44209_chunk_001`
- **Kết quả kiểm tra chống rò rỉ:** Unauthorized attempt ([]) returned 0 forbidden chunks. Authorized attempt (['Guest', 'Bank_Staff', 'Admin']) retrieved 10 compliant chunks.
- **Đánh giá:** `PASS` — Không xảy ra hiện tượng rò rỉ dữ liệu qua BM25, Dense hay Cross-Encoder Reranker.

### 3.5. Test Case [TC05]: Pre-Reranking Filter Leakage Audit
- **Truy vấn kiểm thử:** `"Kỷ luật nhân sự thù lao cán bộ và lộ chìa khóa kho tiền"`
- **Target Chunk ID:** `44209_chunk_051`
- **Kết quả kiểm tra chống rò rỉ:** Unauthorized attempt (['Bank_Staff']) returned 0 forbidden chunks. Authorized attempt (['HR', 'Admin']) retrieved 10 compliant chunks.
- **Đánh giá:** `PASS` — Không xảy ra hiện tượng rò rỉ dữ liệu qua BM25, Dense hay Cross-Encoder Reranker.

---

## 4. Bằng Chứng Bảo Vệ Mức Hệ Thống (Architectural Defense Mechanisms)

1. **Pre-Reranker Filtering:** Mọi chunk không thuộc danh sách `allowed_roles` của vai trò hiện tại đều bị loại bỏ trước khi chuyển sang bước Reranker.
2. **Dense Vector Post-Filtering:** Loại bỏ hoàn toàn khả năng đoán biết khoảng cách vector thông qua việc lọc cứng metadata trước khi trả kết quả.
3. **Graph Cypher Filtering:** Mệnh đề Cypher `WHERE any(role IN node.allowed_roles WHERE role IN $user_roles)` đảm bảo truy vấn đồ thị 1-hop không làm rò rỉ thông tin liên kết.

---

## 5. Kết Luận
Hệ thống RAG đã đạt **Chứng nhận Bảo mật Dữ liệu Mức Cơ bản (Data-Level RBAC Certified)**, không bị rò rỉ dữ liệu giữa các vai trò khác nhau.
