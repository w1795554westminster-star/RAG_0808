# BÁO CÁO MÔ PHỎNG MÃ HÓA DỮ LIỆU Ở TRẠNG THÁI NGHỈ (DATA-AT-REST ENCRYPTION DEMO)

---

## 1. Mục Tiêu & Phạm Vi (Objective & Scope)

Báo cáo này minh họa giải pháp mã hóa dữ liệu ở trạng thái nghỉ (Data-at-Rest Encryption) cho các file dữ liệu nhạy cảm (như file audit log) trong Buổi 17.

> **CẢNH BÁO KIẾN TRÚC (ARCHITECTURAL NOTICE):**  
> Đây là kịch bản demo minh họa khái niệm cơ bản về symmetric encryption trên file cục bộ. Demo này **KHÔNG TUYÊN BỐ PRODUCTION-READY**.

---

## 2. Thiết Kế & Thuật Toán Mã Hóa (Design & Encryption Standard)

- **Thuật toán mã hóa**: `cryptography.fernet.Fernet` (Sử dụng chuẩn AES-128 ở chế độ CBC với PKCS7 padding và mã xác thực thông điệp HMAC-SHA256).
- **Quản lý Khóa (Key Management)**:
  - Khóa mã hóa **KHÔNG HARD-CODE** trong mã nguồn Python.
  - Khóa được khởi tạo động (Base64 URL-safe 32-byte key) và lưu trữ riêng tại: `buoi_17/config/secret.key`.
- **Cấu hình Kiểm soát Phiên bản (.gitignore)**:
  - Tất cả các file khóa `*.key` và file mã hóa `*.enc` đều được thêm vào `buoi_17/.gitignore` để ngăn ngừa tuyệt đối việc lộ khóa lên Git repository.

---

## 3. Quy Trình & Kết Quả Thực Thi Demo (`encryption_demo.py`)

Kịch bản thử nghiệm đã mã hóa và giải mã file audit log minh họa (`demo_audit_raw.jsonl`):

### 3.1 Bảng Thống Kê Hash & Dung Lượng Dữ Liệu

| Giai đoạn | Đường dẫn File | Dung lượng | SHA256 Checksum | Trạng thái |
| :--- | :--- | :---: | :--- | :---: |
| **Dữ liệu Gốc (Raw)** | `outputs/demo_audit_raw.jsonl` | 539 bytes | `05079bee7f22ca4d20026db0326195dc1deb14389ed403c5b589e9ef2ae49663` | Nguyên bản |
| **Dữ liệu Mã hóa (Encrypted)** | `outputs/demo_audit_encrypted.enc` | 804 bytes | `7fd462969e94a68d4e3d0c949806f3649126a3ef8815d2bbbb0664008a525f2e` | Đã mã hóa |
| **Dữ liệu Giải mã (Decrypted)** | `outputs/demo_audit_decrypted.jsonl` | 539 bytes | `05079bee7f22ca4d20026db0326195dc1deb14389ed403c5b589e9ef2ae49663` | **Khớp 100%** |

### 3.2 Đánh Giá Kết Quả Kiểm Tra
1. **Quá trình mã hóa (Encryption Process)**: Dữ liệu gốc 539 bytes được chuyển đổi thành chuỗi ciphertext 804 bytes không thể đọc được bằng văn bản thuần (`ENCRYPT: PASS`).
2. **Quá trình giải mã & So khớp (Decryption & Hash Match)**: Dữ liệu sau giải mã hoàn toàn trùng khớp từng byte và trùng khớp 100% mã hash SHA256 với file gốc (`DECRYPT MATCH: PASS`).
3. **Bảo toàn dữ liệu nguồn**: Toàn bộ dữ liệu gốc `chunks_secure.csv` và `chunks_normalized.csv` giữ nguyên trạng, không bị chỉnh sửa hay ảnh hưởng.

---

## 4. Giải Thích Cho Học Viên: Sự Khác Biệt Giữa Demo và Hệ Thống Production

Trong môi trường doanh nghiệp và ngân hàng thực tế, việc mã hóa dữ liệu đòi hỏi các tiêu chuẩn an ninh thông tin khắt khe vượt xa phạm vi bài học demo. Một hệ thống Production hoàn chỉnh bắt buộc phải bổ sung các lớp bảo mật sau:

```text
[Người dùng / Client]
       │
       ▼  (1) TLS / HTTPS (Data-in-Transit)
[Hệ thống AI / API Gateway]
       │
       ▼  (2) IAM & Role Policies (Xác thực & Phân quyền)
[Enterprise KMS (AWS KMS / HashiCorp Vault / Cloud KMS)] ◄─── (3) Key Rotation & Envelope Encryption
       │
       ▼  (4) Hardware Security Module (HSM) / Encrypted Storage
[Data-at-Rest Storage + Encrypted Backups]
```

1. **Bảo vệ dữ liệu khi truyền tải (Data-in-Transit)**:
   - Phải sử dụng mã hóa TLS 1.3 / HTTPS cho mọi kết nối mạng giữa client, server và cơ sở dữ liệu để chống bắt lén gói tin (Man-in-the-Middle).
2. **Dịch vụ quản lý khóa chuyên nghiệp (KMS - Key Management Service)**:
   - Không lưu file khóa `secret.key` trên cùng máy chủ ứng dụng.
   - Sử dụng các dịch vụ KMS chuyên dụng như AWS KMS, Google Cloud KMS, Azure Key Vault, hoặc HashiCorp Vault có tích hợp phần cứng bảo mật HSM (Hardware Security Module).
3. **Cơ chế xoay vòng khóa (Key Rotation)**:
   - Định kỳ xoay vòng khóa tự động (VD: 90 ngày/lần) và áp dụng cơ chế Envelope Encryption (Mã hóa bao thư: Data Encryption Key được mã hóa bởi Key Encryption Key).
4. **Sao lưu & Phục hồi thảm họa (Backup & Disaster Recovery)**:
   - Các bản sao lưu (Backup snapshot/cold storage) phải được mã hóa độc lập và có quy trình khôi phục được kiểm thử định kỳ.
5. **Kiểm soát truy cập khóa (IAM & Audit Trail)**:
   - Áp dụng nguyên tắc quyền tối thiểu (Least Privilege) với IAM để quy định chặt chẽ ai/dịch vụ nào có quyền gọi hàm `kms:Decrypt`.

---

## 5. Kết Luận Báo Cáo

```text
ENCRYPT: PASS
DECRYPT MATCH: PASS
PRODUCTION READY: NO
```
