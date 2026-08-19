# BÁO CÁO THỬ NGHIỆM TRUY VẤN AN TOÀN (SECURE RETRIEVAL TEST REPORT) - BUỔI 17

---

## 1. Giới Thiệu & Kiến Trúc Tái Sử Dụng (Reuse Architecture)

Buổi 17 thực hiện tái sử dụng nguyên trạng thuật toán `SecureRetriever` của Buổi 16 (tại [secure_retriever.py](file:///d:/03.08/buoi_16/src/secure_retriever.py)) và bổ sung lớp Adapter chuẩn hóa interface tại [secure_retrieval_adapter.py](file:///d:/03.08/buoi_17/scripts/secure_retrieval_adapter.py).

### 1.1 Cấu Trúc Đầu Ra Chuẩn Hóa (Standardized Output Schema)
Mỗi chunk trả về qua `SecureRetrievalAdapter` bao gồm đầy đủ 10 trường thuộc tính:
- `rank`: Thứ hạng trả về (1..K).
- `chunk_id`: Định danh duy nhất đoạn trích (VD: `44209_chunk_021`).
- `document_id`: Mã hiệu văn bản pháp lý (VD: `44209`).
- `title`: Tên đầy đủ của văn bản.
- `article`: Điều khoản trích dẫn (VD: `Điều 15`).
- `citation`: Trích dẫn pháp lý chuẩn hóa `[Tên văn bản | Số hiệu | Điều | Chunk ID]`.
- `allowed_roles`: Danh sách danh hiệu vai trò được phép xem.
- `access_decision`: Quyết định truy cập (`GRANTED` cho tất cả chunk trả về).
- `retrieval_method`: Phương thức tìm kiếm (`bm25`, `dense`, `hybrid`, `hybrid_rerank`).
- `text`: Nội dung văn bản trích dẫn.

---

## 2. Kết Quả Thử Nghiệm 4 Yêu Cầu Bắt Buộc (4 Test Suites)

Tập dữ liệu thử nghiệm: `../buoi_16/data/processed/chunks_secure.csv` (2,823 chunks).  
Chunk nhạy cảm kiểm thử: `44209_chunk_021` (*Điều 15. Sắp xếp, bảo quản tài sản tại quầy giao dịch và trong kho tiền*).  
Danh sách vai trò được phép (`allowed_roles`): `["Admin", "Risk_Manager", "Legal_Officer", "Bank_Staff", "Staff"]` (Hoàn toàn ẩn đối với `Guest`).

### 2.1 Test 1: Vai Trò Được Phép Nhận Được Chunk (Authorized Role Check)
- **Role thử nghiệm**: `Staff` (Nhân viên nội bộ).
- **Query**: *"Bảo quản tài sản tại quầy giao dịch và trong kho tiền nghỉ buổi trưa"*
- **Kết quả**: Chunk `44209_chunk_021` xuất hiện tại **Rank 1** trong danh sách kết quả.
- **Trạng thái**: **PASS**

### 2.2 Test 2: Vai Trò Không Được Phép Không Nhận Được Chunk (Unauthorized Role Check)
- **Role thử nghiệm**: `Guest` (Khách / Công khai).
- **Query**: *"Bảo quản tài sản tại quầy giao dịch và trong kho tiền nghỉ buổi trưa"*
- **Kết quả**: Chunk `44209_chunk_021` **KHÔNG XUẤT HIỆN** trong Top 5 kết quả của `Guest` (Đã bị Pre-filtering loại bỏ hoàn toàn).
- **Trạng thái**: **PASS**

### 2.3 Test 3: Văn Bản Không Có Quyền Không Bao Giờ Xuất Hiện Trong Context (No Unauthorized Context Check)
- **Thử nghiệm**: Duyệt qua 4 roles khác nhau (`Guest`, `HR`, `Staff`, `Risk_Manager`) với các câu hỏi truy vấn tổng hợp.
- **Kết quả**: 
  - Số lượng chunk vi phạm quyền trong Context gửi cho LLM: `0` / 100%.
  - 100% chunks trả về đều thỏa mãn `user_role IN chunk.allowed_roles`.
- **Trạng thái**: **PASS**

### 2.4 Test 4: Bảo Toàn Định Danh & Trích Dẫn (Citation & Metadata Preservation)
- **Thử nghiệm**: Kiểm tra tính toàn vẹn thông tin của tất cả các phần tử trả về qua `SecureRetrievalAdapter`.
- **Kết quả**:
  - `chunk_id`: Bảo toàn 100%.
  - `document_id`: Bảo toàn 100%.
  - `citation`: Bảo toàn 100%.
  - `title` & `article`: Bảo toàn 100%.
  - `access_decision`: `GRANTED` (Bảo toàn 100%).
- **Trạng thái**: **PASS**

---

## 3. Mẫu Dữ Liệu Trả Về Chuẩn Hóa qua Adapter

```json
{
  "rank": 1,
  "chunk_id": "44209_chunk_021",
  "document_id": "44209",
  "title": "Thông tư số 01/2014/TT-NHNN Quy định về giao nhận, bảo quản, vận chuyển tiền mặt, tài sản quý, giấy tờ có giá",
  "article": "Điều 15",
  "citation": "[Thông tư số 01/2014/TT-NHNN Quy định về giao nhận, bảo quản, vận chuyển tiền mặt, tài sản quý, giấy tờ có giá | Số: 01/2014/TT-NHNN | Điều 15 | 44209_chunk_021]",
  "allowed_roles": [
    "Admin",
    "Risk_Manager",
    "Legal_Officer",
    "Bank_Staff",
    "Staff"
  ],
  "access_decision": "GRANTED",
  "retrieval_method": "bm25",
  "text": "Điều 15. Sắp xếp, bảo quản tài sản tại quầy giao dịch và trong kho tiền..."
}
```

---

## 4. Kết Luận Báo Cáo

```text
SECURE RETRIEVAL REUSE: PASS
NO UNAUTHORIZED CONTEXT: PASS
CITATION PRESERVED: PASS
```
