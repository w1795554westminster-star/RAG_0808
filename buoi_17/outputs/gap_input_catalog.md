# BÁO CÁO DANH MỤC TÀI LIỆU VÀ PHÂN LOẠI ĐẦU VÀO CHO COMPLIANCE GAP CHECKER (GAP INPUT CATALOG)

---

## 1. Tổng Quan Kiểm Tra Dữ Liệu Nguồn (Corpus Assessment)

Dữ liệu nguồn kiểm tra: `../buoi_16/data/processed/chunks_secure.csv` (2,823 chunks).  
Mục tiêu: Phân loại từng văn bản theo đúng bằng chứng thực tế (Real Evidence) để phục vụ bài toán so sánh tuân thủ (Compliance Gap Analysis) giữa Quy định pháp lý bên ngoài (`EXTERNAL_REQUIREMENT`) và Quy định nội bộ (`INTERNAL_POLICY`).

### 1.1 Nguyên Tắc Phân Loại Bắt Buộc (Classification Principles)
- **`EXTERNAL_REQUIREMENT`**: Các Luật, Nghị định, Thông tư, Văn bản hợp nhất do Quốc hội, Chính phủ, Ngân hàng Nhà nước Việt Nam hoặc Bộ Tài chính ban hành.
- **`INTERNAL_POLICY`**: Chỉ phân loại khi có bằng chứng thực tế chứng minh đó là Quy định, Quyết định, Quy trình nội bộ do Ngân hàng (Agribank) ban hành.
- **Cam kết Trung thực Dữ liệu**: **KHÔNG** tự ý gán nhãn một Thông tư/Nghị định thành "quy định nội bộ" để khiên cưỡng chạy demo.

---

## 2. Danh Mục Chi Tiết 30 Văn Bản Trong Tập Dữ Liệu

| STT | Document ID | Tên Văn Bản (Title) | Số Ký Hiệu | Loại Văn Bản | Cơ Quan Ban Hành | Phân Loại (Classification) | Bằng Chứng Thực Tế (Evidence) | Chunks |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| 1 | `44209` | Thông tư 01/2014/TT-NHNN Quy định về giao nhận, bảo quản, vận chuyển tiền mặt, tài sản quý | 01/2014/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 90 |
| 2 | `166170` | Luật Các tổ chức tín dụng số 32/2024/QH15 | 32/2024/QH15 | Luật | Quốc hội | **EXTERNAL_REQUIREMENT** | Văn bản Luật do Quốc hội ban hành | 328 |
| 3 | `166269` | Luật Hợp tác xã số 17/2023/QH15 | 17/2023/QH15 | Luật | Quốc hội | **EXTERNAL_REQUIREMENT** | Văn bản Luật do Quốc hội ban hành | 172 |
| 4 | `117310` | Thông tư 41/2016/TT-NHNN Quy định tỷ lệ an toàn vốn | 41/2016/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 98 |
| 5 | `112924` | Thông tư 105/2016/TT-BTC Hướng dẫn đầu tư gián tiếp ra nước ngoài | 105/2016/TT-BTC | Thông tư | Bộ Tài chính | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do Bộ Tài chính ban hành | 58 |
| 6 | `186482` | Thông tư 69/2025/TT-NHNN Sửa đổi các Thông tư giám sát ngân hàng | 69/2025/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 52 |
| 7 | `173460` | Thông tư 57/2024/TT-NHNN Cấp phép TCTD phi ngân hàng | 57/2024/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 40 |
| 8 | `164719` | Thông tư 22/2023/TT-NHNN Sửa đổi Thông tư 41 tỷ lệ an toàn vốn | 22/2023/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 33 |
| 9 | `150974` | Thông tư 08/2021/TT-BTC Chuẩn mực kiểm toán nội bộ | 08/2021/TT-BTC | Thông tư | Bộ Tài chính | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do Bộ Tài chính ban hành | 16 |
| 10 | `30402` | Thông tư 202/2012/TT-BTC Đăng ký kiểm toán viên | 202/2012/TT-BTC | Thông tư | Bộ Tài chính | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do Bộ Tài chính ban hành | 25 |
| 11 | `6e689cd0` | VBHN 52/VBHN-NHNN Hồ sơ cấp phép NHTM, chi nhánh NHNNg | 52/VBHN-NHNN | VBHN | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản hợp nhất do NHNN ban hành | 176 |
| 12 | `185630` | Thông tư 63/2025/TT-NHNN Sửa đổi quy định Quỹ tín dụng nhân dân | 63/2025/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 30 |
| 13 | `173695` | Thông tư 56/2024/TT-NHNN Cấp phép NHTM và chi nhánh NHNNg | 56/2024/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 60 |
| 14 | `38128` | Thông tư 37/2014/TT-NHNN Thiết kế mẫu tiền và quản lý in đúc tiền | 37/2014/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 28 |
| 15 | `95652` | Nghị định 135/2015/NĐ-CP Quy định đầu tư gián tiếp ra nước ngoài | 135/2015/NĐ-CP | Nghị định | Chính phủ | **EXTERNAL_REQUIREMENT** | Nghị định do Chính phủ ban hành | 53 |
| 16 | `168859` | Thông tư 29/2024/TT-NHNN Quy định về quỹ tín dụng nhân dân | 29/2024/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 75 |
| 17 | `133858` | Nghị định 05/2019/NĐ-CP Về kiểm toán nội bộ | 05/2019/NĐ-CP | Nghị định | Chính phủ | **EXTERNAL_REQUIREMENT** | Nghị định do Chính phủ ban hành | 40 |
| 18 | `25692` | Luật Ngân hàng Nhà nước Việt Nam số 46/2010/QH12 | 46/2010/QH12 | Luật | Quốc hội | **EXTERNAL_REQUIREMENT** | Văn bản Luật do Quốc hội ban hành | 108 |
| 19 | `163441` | Nghị định 46/2023/NĐ-CP Luật Kinh doanh bảo hiểm | 46/2023/NĐ-CP | Nghị định | Chính phủ | **EXTERNAL_REQUIREMENT** | Nghị định do Chính phủ ban hành | 250 |
| 20 | `112025` | Nghị định 73/2016/NĐ-CP Hướng dẫn Luật Kinh doanh bảo hiểm | 73/2016/NĐ-CP | Nghị định | Chính phủ | **EXTERNAL_REQUIREMENT** | Nghị định do Chính phủ ban hành | 120 |
| 21 | `26750` | Luật Các TCTD số 47/2010/QH12 | 47/2010/QH12 | Luật | Quốc hội | **EXTERNAL_REQUIREMENT** | Văn bản Luật do Quốc hội ban hành | 220 |
| 22 | `143217` | Thông tư 28/2020/TT-BTC Hướng dẫn quản lý tài chính TCTD | 28/2020/TT-BTC | Thông tư | Bộ Tài chính | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do Bộ Tài chính ban hành | 45 |
| 23 | `21703` | Thông tư 01/2013/TT-NHNN Hoạt động chiết khấu giấy tờ có giá | 01/2013/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 35 |
| 24 | `110594` | Thông tư 39/2016/TT-NHNN Cho vay của TCTD | 39/2016/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 85 |
| 25 | `162799` | Thông tư 06/2023/TT-NHNN Sửa đổi Thông tư 39 cho vay | 06/2023/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 40 |
| 26 | `173458` | Thông tư 55/2024/TT-NHNN Chuyển đổi TCTD | 55/2024/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 30 |
| 27 | `173459` | Thông tư 58/2024/TT-NHNN Cấp phép TCTD phi ngân hàng | 58/2024/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 35 |
| 28 | `173461` | Thông tư 59/2024/TT-NHNN Mạng lưới TCTD | 59/2024/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 40 |
| 29 | `173462` | Thông tư 60/2024/TT-NHNN Mở chi nhánh TCTD | 60/2024/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 25 |
| 30 | `173463` | Thông tư 61/2024/TT-NHNN Phong tỏa tài khoản TCTD | 61/2024/TT-NHNN | Thông tư | Ngân hàng Nhà nước Việt Nam | **EXTERNAL_REQUIREMENT** | Văn bản quy phạm pháp luật do NHNN ban hành | 30 |

---

## 3. Thống Kê & Đánh Giá Đủ Điều Kiện Cho Compliance Gap Checker

- **Tổng số văn bản kiểm tra (Total Documents)**: `30` văn bản.
- **Số lượng văn bản quy định nhà nước (`EXTERNAL_REQUIREMENT`)**: `30` văn bản (100.0%).
- **Số lượng quy định nội bộ (`INTERNAL_POLICY`)**: `0` văn bản (0.0%).

### 3.1 Nhận Xét Chuyên Môn (Expert Assessment)
Tất cả 30 văn bản trong tập dữ liệu `chunks_secure.csv` hiện tại đều là **Văn bản quy phạm pháp luật cấp Nhà nước** (Luật của Quốc hội, Nghị định của Chính phủ, Thông tư của NHNN và Bộ Tài chính). Không có bất kỳ Quy định/Quy trình nội bộ thực tế nào của Ngân hàng thương mại (Agribank) trong tập dữ liệu này.

Để thực hiện so sánh Khoảng cách Tuân thủ (Compliance Gap Analysis) một cách hợp lệ và khoa học, hệ thống bắt buộc phải có đối sánh 2 chiều:
1. **Yêu cầu quy định bên ngoài** (`EXTERNAL_REQUIREMENT` - Ví dụ: Thông tư NHNN).
2. **Quy định/Quy trình nội bộ** (`INTERNAL_POLICY` - Ví dụ: Quy trình kho quỹ Agribank).

Do tập dữ liệu hiện tại khuyết thiếu hoàn toàn tập `INTERNAL_POLICY`, hệ thống tuân thủ nghiêm ngặt nguyên tắc **Không kết luận Compliance trên tập dữ liệu chưa đủ bằng chứng**.

---

## 4. Kết Luận Báo Cáo

```text
COMPLIANCE GAP DATA: INSUFFICIENT
DATA GAP: INTERNAL POLICY NOT FOUND
```
