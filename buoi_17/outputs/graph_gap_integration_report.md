# BÁO CÁO ĐÁNH GIÁ VÀ TÍCH HỢP KNOWLEDGE GRAPH CHO COMPLIANCE GAP CHECKER (BUỔI 17)

---

## 1. Giới Thiệu & Triết Lý Phân Công Vai Trò Hệ Thống

Trong hệ thống RAG nâng cao kết hợp Quản trị Tuân thủ (Compliance RAG), ba thành phần chính có sự phân công vai trò rõ ràng:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ Hybrid Search  = Tìm nội dung liên quan theo từ khóa (BM25) & Vector   │
│ Knowledge Graph = Mở rộng ứng viên theo các quan hệ đã biết (1-hop)    │
│ Gap Checker    = So sánh gói bằng chứng (Evidence) để đưa ra kết luận │
└────────────────────────────────────────────────────────────────────────┘
```

> **NGUYÊN TẮC BẮT BUỘC:**  
> Hệ thống chỉ khai thác các mối quan hệ (Relationships/Edges) **THỰC TẾ TỒN TẠI** trong cơ sở dữ liệu Neo4j hoặc tập dữ liệu đồ thị [relationships.csv](file:///d:/03.08/kb+hops/relationships.csv). **TUYỆT ĐỐI KHÔNG TỰ TẠO EDGE GIẢ**.

---

## 2. Rà Soát & Phân Loại Các Loại Quan Hệ (Relationship Types) Thực Tế

Kiểm tra tập dữ liệu quan hệ đồ thị tại `kb+hops/relationships.csv` (gồm 329 cạnh/edges thực tế):

### 2.1 Nhóm 1: Quan hệ Nối Văn bản / Điều khoản (Nội dung Pháp lý) - **CÓ GIÁ TRỊ RẤT CAO**
Các quan hệ này trực tiếp liên kết logic giữa các văn bản pháp lý và quy định:

| Loại Quan Hệ (Relationship Type) | Tần suất | Ý nghĩa và Vai trò đối với Compliance Gap Checker |
| :--- | :---: | :--- |
| **`THAM_CHIEU`** | `163` (49.5%) | **Rất quan trọng**: Cho biết văn bản/dấu hiệu điều khoản này dẫn chiếu đến văn bản/điều khoản khác. Giúp tìm văn bản nền tảng. |
| **`SUA_DOI_BO_SUNG`** | `40` (12.2%) | **Rất quan trọng**: Cho biết văn bản mới sửa đổi/bổ sung cho văn bản cũ (VD: Thông tư 43/2024 sửa đổi Thông tư 01/2014). Tránh dùng quy định đã hết hiệu lực. |
| **`THAY_THE_BOI`** | `6` (1.8%) | **Quan trọng**: Cho biết điều khoản/văn bản đã bị thay thế hoàn toàn bởi quy định mới. |

### 2.2 Nhóm 2: Quan hệ Metadata Thuộc tính & Cơ quan - **GIÁ TRỊ BỔ TRỢ**
Các quan hệ này cung cấp ngữ cảnh về cơ quan phát hành và phạm vi áp dụng:
- **`BAN_HANH_BOI`** (`30` edges): Nối văn bản với cơ quan ban hành (NHNN, Bộ Tài chính, Chính phủ).
- **`KY_BOI`** (`30` edges): Nối văn bản với người ký (Thống đốc, Bộ trưởng).
- **`AP_DUNG_CHO`** (`30` edges): Phạm vi đối tượng áp dụng (TCTD, Chi nhánh NHNNg).
- **`THUOC_LINH_VUC`** (`30` edges): Lĩnh vực quản lý (Kho quỹ, An toàn vốn, Kiểm toán).

### 2.3 Nhóm 3: Quan hệ Cấu trúc Phân cấp (Hierarchy Containment) - **KHÔNG NỐI CROSS-DOCUMENT**
- **`CONTAINS` / `HAS_SECTION` / `NEXT`**: Các quan hệ cấu trúc phân cấp cây văn bản (Chương $\rightarrow$ Mục $\rightarrow$ Điều $\rightarrow$ Chunk). Chỉ dùng để duyệt cây nội bộ của 1 văn bản, không giúp nối liên kết giữa 2 văn bản khác nhau.

---

## 3. Đánh Giá Hiệu Quả & Cơ Chế Tích Hợp Đồ Thị (Graph Candidate Expansion)

### 3.1 Cơ Chế Mở Rộng Ứng Viên (Graph Candidate Expansion Workflow)
Khi `ComplianceGapChecker` nhận được một Yêu cầu NHNN (`external_requirement`):
1. **Bước 1 (Hybrid Search)**: Lấy Top-K ứng viên có điểm tương đồng nội dung cao nhất (BM25 + Dense).
2. **Bước 2 (Graph Expansion)**: Gọi `SecureRetriever.get_secure_graph_hints()` để lấy các node liên kết 1-hop qua quan hệ `THAM_CHIEU`, `SUA_DOI_BO_SUNG`, `THAY_THE_BOI`.
3. **Bước 3 (Fusion & Filtering)**: Hợp nhất danh sách ứng viên từ Hybrid Search và Graph Expansion, lọc qua RBAC pre-filter (`auth_mask`) để đảm bảo không vi phạm phân quyền.
4. **Bước 4 (Evidence Package & Gap Analysis)**: Xây dựng gói bằng chứng hai phía và đưa vào mô hình phân loại.

### 3.2 Hiện Trạng Dữ Liệu Rút Ra
- Do tập corpus hiện tại mới có 30 văn bản pháp luật bên ngoài (khuyết thiếu `INTERNAL_POLICY`), các edge `SUA_DOI_BO_SUNG` và `THAM_CHIEU` hiện tại mở rộng rất tốt liên kết giữa các Thông tư NHNN sửa đổi với nhau (VD: Thông tư 43/2024 $\rightarrow$ Thông tư 01/2014).
- Khi bổ sung dữ liệu quy định nội bộ Agribank có chứa các liên kết dẫn chiếu `THAM_CHIEU` đến Thông tư NHNN, cơ chế Graph Expansion này sẽ ngay lập tức phát huy 100% sức mạnh tìm kiếm đối ứng hai chiều.

---

## 4. Kết Luận Báo Cáo

```text
GRAPH USED: YES
```

**Lý do**:  
Đã xác nhận 3 loại quan hệ thực tế `THAM_CHIEU` (163 edges), `SUA_DOI_BO_SUNG` (40 edges) và `THAY_THE_BOI` (6 edges) có giá trị cao trong việc mở rộng ứng viên đối ứng. Cơ chế Graph Candidate Expansion được tích hợp chính thức vào pipeline tìm kiếm ứng viên của `ComplianceGapChecker` mà không tự tạo bất kỳ edge giả nào.
