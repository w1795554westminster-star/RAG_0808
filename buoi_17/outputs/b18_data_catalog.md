# BÁO CÁO DATA CATALOGING & DỮ LIỆU ĐẦU VÀO BUỔI 18
**Ngày thực hiện:** 2026-08-24 20:58:35  
**Tệp dữ liệu phân tích:**
1. `data/agribank_internal_policies.csv` (24 chunks)
2. `data/chunks_combined_secure.csv` (811 chunks)

---

## 1. Thống kê Văn bản Nội bộ Agribank (10 Quy định cốt lõi)

| STT | Mã VB | Tên Văn Bản Nội Bộ | Số Ký Hiệu | Loại Văn Bản | Cơ Quan Ban Hành | Ngày Ban Hành | Miền Nghiệp Vụ (Domain) | Số Chunks | Quyền Truy Cập (Allowed Roles) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `agr_at01` | Quy định nội bộ số 100/QĐ-NHNO-AT về Giao nhận, bảo quản, vận chuyển tiền mặt và tài sản quý Agribank | `100/QĐ-NHNO-AT` | Quy định nội bộ | Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam (Agribank) | 15/03/2024 | **An toàn kho quỹ & Vận chuyển tiền mặt** | 4 | `["Admin", "Risk_Manager", "Staff"]` |
| 2 | `agr_bh06` | Quy định nội bộ số 180/QĐ-NHNO-BH về Mua bảo hiểm rủi ro nghiệp vụ và tài sản Agribank | `180/QĐ-NHNO-BH` | Quy định nội bộ | Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam (Agribank) | 14/02/2024 | **Bảo hiểm & Quản lý tài sản** | 2 | `["Admin", "Risk_Manager", "Staff"]` |
| 3 | `agr_car02` | Quy định nội bộ số 250/QĐ-NHNO-QLRR về Quản lý tỷ lệ an toàn vốn và định mức rủi ro Agribank | `250/QĐ-NHNO-QLRR` | Quy định nội bộ | Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam (Agribank) | 20/06/2024 | **CAR & Quản lý rủi ro** | 3 | `["Admin", "Risk_Manager"]` |
| 4 | `agr_fx04` | Quy định nội bộ số 410/QĐ-NHNO-TTNH về Quản lý trạng thái ngoại tệ và giao dịch ngoại hối Agribank | `410/QĐ-NHNO-TTNH` | Quy định nội bộ | Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam (Agribank) | 05/09/2024 | **Giao dịch Ngoại tệ & Ngoại hối** | 2 | `["Admin", "Risk_Manager"]` |
| 5 | `agr_gp05` | Quy chế số 520/QC-NHNO-MANGLUOI về Mở rộng mạng lưới chi nhánh và phòng giao dịch Agribank | `520/QC-NHNO-MANGLUOI` | Quy chế nội bộ | Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam (Agribank) | 18/11/2024 | **Quản lý Mạng lưới & Giấy phép** | 2 | `["Admin", "Risk_Manager", "Staff"]` |
| 6 | `agr_hr08` | Quy định nội bộ số 88/QĐ-NHNO-NS về Quy hoạch, bổ nhiệm và quản lý nhân sự Agribank | `88/QĐ-NHNO-NS` | Quy định nội bộ | Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam (Agribank) | 10/01/2025 | **Quản lý Nhân sự & Phân cấp** | 2 | `["Admin", "HR"]` |
| 7 | `agr_it07` | Quy chế bảo mật CNTT số 600/QC-NHNO-CNTT về An toàn thông tin và Quản trị dữ liệu AI Agribank | `600/QC-NHNO-CNTT` | Quy chế nội bộ | Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam (Agribank) | 01/03/2025 | **Bảo mật CNTT & AI** | 2 | `["Admin", "Risk_Manager"]` |
| 8 | `agr_tc09` | Quy chế tài chính số 720/QC-NHNO-TC về Chế độ chi tiêu và mua sắm tài sản nội bộ Agribank | `720/QC-NHNO-TC` | Quy chế nội bộ | Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam (Agribank) | 05/12/2024 | **Mua sắm nội bộ & Tài chính** | 2 | `["Admin", "Risk_Manager", "Staff"]` |
| 9 | `agr_td03` | Quy chế tín dụng nội bộ số 315/QC-NHNO-TD về Phán quyết và Phân cấp ủy quyền cho vay tại Agribank | `315/QC-NHNO-TD` | Quy chế nội bộ | Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam (Agribank) | 10/01/2024 | **Tín dụng & Phê duyệt cho vay** | 3 | `["Admin", "Risk_Manager", "Staff"]` |
| 10 | `agr_xln10` | Quy định nội bộ số 390/QĐ-NHNO-XLN về Phân loại nợ và Xử lý nợ xấu tại Agribank | `390/QĐ-NHNO-XLN` | Quy định nội bộ | Ngân hàng Nông nghiệp và Phát triển Nông thôn Việt Nam (Agribank) | 22/07/2024 | **Phân loại nợ & Xử lý nợ xấu** | 2 | `["Admin", "Risk_Manager"]` |

---

## 2. Thống kê Tổng quan Tập Dữ liệu Kết hợp (`chunks_combined_secure.csv`)

- **Tổng số văn bản (Unique Documents):** 25 văn bản
  - **Văn bản Nội bộ Agribank:** 10 văn bản (24 chunks)
  - **Văn bản Pháp luật / NHNN (External Legal Docs):** 15 văn bản (787 chunks)
- **Tổng số Chunks trong Hệ thống:** 811 chunks

### Danh sách các Văn bản Pháp luật / NHNN tiêu biểu trong Dataset:
| STT | Mã VB | Tên Văn Bản Pháp Lý / NHNN | Số Ký Hiệu | Cơ Quan Ban Hành | Số Chunks |
|---|---|---|---|---|---|
| 1 | `112025` | Nghị định số 73/2016/NĐ-CP Quy định chi tiết thi hành Luật kinh doanh bảo hiểm và Luật sửa đổi, bổ sung một số điều của Luật kinh doanh bảo hiểm | `73/2016/NĐ-CP` | Chính phủ | 117 |
| 2 | `112924` | Thông tư số 105/2016/TT-BTC Hướng dẫn hoạt động đầu tư gián tiếp ra nước ngoài của tổ chức kinh doanh chứng khoán, quỹ đầu tư chứng khoán, công ty đầu tư chứng khoán và doanh nghỉệp kinh doanh bảo hỉểm | `105/2016/TT-BTC` | Bộ Tài chính | 22 |
| 3 | `117310` | Thông tư số 41/2016/TT-NHNN Quy định tỷ lệ an toàn vốn đối với ngân hàng, chi nhánh ngân hàng nước ngoài | `41/2016/TT-NHNN` | Ngân hàng Nhà nước Việt Nam | 25 |
| 4 | `163441` | Nghị định số 46/2023/NĐ-CP Quy định chi tiết thi hành một số điều của Luật Kinh doanh bảo hiểm | `46/2023/NĐ-CP` | Chính phủ | 143 |
| 5 | `166269` | Luật Hợp tác xã số 17/2023/QH15 | `17/2023/QH15` | Quốc hội | 116 |
| 6 | `168220` | Thông tư số 27/2024/TT-NHNN Quy định về việc ngân hàng hợp tác xã, việc trích nộp, quản lý và sử dụng Quỹ bảo đảm an toàn hệ thống quỹ tín dụng nhân dân | `27/2024/TT-NHNN` | Ngân hàng Nhà nước Việt Nam | 35 |
| 7 | `169221` | Thông tư số 43/2024/TT-NHNN sửa đổi, bổ sung một số điều của Thông tư số 01/2014/TT-NHNN ngày 10 tháng 12 năm 2014 của Thống đốc Ngân hàng Nhà nước Việt Nam hướng dẫn việc tổ chức thực hiện hoạt đọng quản lý dự trữ ngoại hối nhà nước. | `43/2024/TT-NHNN` | Ngân hàng Nhà nước Việt Nam | 5 |
| 8 | `173695` | Thông tư số 56/2024/TT-NHNN Quy định hồ sơ, thủ tục cấp Giấy phép lần đầu của ngân hàng thương mại, chi nhánh ngân hàng nước ngoài, văn phòng đại diện nước ngoài | `56/2024/TT-NHNN` | Ngân hàng Nhà nước Việt Nam | 26 |
| 9 | `174218` | Thông tư số 62/2024/TT-NHNN Quy định điều kiện, hồ sơ, thủ tục chấp thuận việc tổ chức lại ngân hàng thương mại, tổ chức tín dụng phi ngân hàng | `62/2024/TT-NHNN` | Ngân hàng Nhà nước Việt Nam | 31 |
| 10 | `177271` | Thông tư số 01/2025/TT-NHNN Quy định về cấp Giấy phép lần đầu, cấp đổi Giấy phép của quỹ tín dụng nhân dân | `01/2025/TT-NHNN` | Ngân hàng Nhà nước Việt Nam | 22 |
| 11 | `185630` | Thông tư số 63/2025/TT-NHNN Sửa đổi, bổ sung một số điều của một số Thông tư về quỹ tín dụng nhân dân | `63/2025/TT-NHNN` | Ngân hàng Nhà nước Việt Nam | 17 |
| 12 | `25692` | Ngân hàng Nhà nước Việt Nam | `46/2010/QH12` | Quốc hội | 68 |
| 13 | `44209` | Thông tư số 01/2014/TT-NHNN Quy định về giao nhận, bảo quản, vận chuyển tiền mặt, tài sản quý, giấy tờ có giá | `01/2014/TT-NHNN` | Ngân hàng Nhà nước Việt Nam | 74 |
| 14 | `6e689cd0-6f81-11f1-94d6-fd5d6d5ff793` | Quy định hồ sơ, thủ tục cấp Giấy phép lần đầu của ngân hàng thương mại, chi nhánh ngân hàng nước ngoài, văn phòng đại diện nước ngoài | `52/VBHN-NHNN` | Ngân hàng Nhà nước Việt Nam | 46 |
| 15 | `95652` | Nghị định số 135/2015/NĐ-CP Quy định về đầu tư gián tiếp ra nước ngoài | `135/2015/NĐ-CP` | Chính phủ | 40 |

---

## 3. Phân loại theo Domain / Nhiệm vụ (Domains Classification)

Hệ thống đã phát hiện và phân loại **10 miền nghiệp vụ trọng yếu** cho toàn bộ quy định Agribank:

- **Domain 1: An toàn kho quỹ & Vận chuyển tiền mặt** — 1 văn bản nội bộ (4 chunks)
- **Domain 2: Bảo hiểm & Quản lý tài sản** — 1 văn bản nội bộ (2 chunks)
- **Domain 3: Bảo mật CNTT & AI** — 1 văn bản nội bộ (2 chunks)
- **Domain 4: CAR & Quản lý rủi ro** — 1 văn bản nội bộ (3 chunks)
- **Domain 5: Giao dịch Ngoại tệ & Ngoại hối** — 1 văn bản nội bộ (2 chunks)
- **Domain 6: Mua sắm nội bộ & Tài chính** — 1 văn bản nội bộ (2 chunks)
- **Domain 7: Phân loại nợ & Xử lý nợ xấu** — 1 văn bản nội bộ (2 chunks)
- **Domain 8: Quản lý Mạng lưới & Giấy phép** — 1 văn bản nội bộ (2 chunks)
- **Domain 9: Quản lý Nhân sự & Phân cấp** — 1 văn bản nội bộ (2 chunks)
- **Domain 10: Tín dụng & Phê duyệt cho vay** — 1 văn bản nội bộ (3 chunks)

---

## 4. Kiểm tra Tính Đầy đủ của 14 Trường Metadata

Kiểm tra toàn bộ 14 trường metadata quy chuẩn: `chunk_id`, `document_id`, `text`, `source_file`, `title`, `so_ky_hieu`, `loai_van_ban`, `co_quan_ban_hanh`, `ngay_ban_hanh`, `chapter`, `section`, `article`, `citation`, `allowed_roles`.

| Trường Metadata | Số Lượng Rỗng (Internal Policies) | Số Lượng Rỗng (Combined CSV) | Trạng Thái Đầy Đủ | Ghi Chú |
|---|---|---|---|---|
| `chunk_id` | 0 | 0 | ✅ PASS | Bắt buộc 100% đầy đủ |
| `document_id` | 0 | 0 | ✅ PASS | Tùy thuộc cấu trúc chương mục |
| `text` | 0 | 0 | ✅ PASS | Bắt buộc 100% đầy đủ |
| `source_file` | 0 | 0 | ✅ PASS | Tùy thuộc cấu trúc chương mục |
| `title` | 0 | 0 | ✅ PASS | Tùy thuộc cấu trúc chương mục |
| `so_ky_hieu` | 0 | 0 | ✅ PASS | Tùy thuộc cấu trúc chương mục |
| `loai_van_ban` | 0 | 0 | ✅ PASS | Tùy thuộc cấu trúc chương mục |
| `co_quan_ban_hanh` | 0 | 0 | ✅ PASS | Tùy thuộc cấu trúc chương mục |
| `ngay_ban_hanh` | 0 | 0 | ✅ PASS | Tùy thuộc cấu trúc chương mục |
| `chapter` | 0 | 5 | ✅ PASS | Tùy thuộc cấu trúc chương mục |
| `section` | 0 | 219 | ✅ PASS | Tùy thuộc cấu trúc chương mục |
| `article` | 0 | 0 | ✅ PASS | Bắt buộc 100% đầy đủ |
| `citation` | 0 | 0 | ✅ PASS | Bắt buộc 100% đầy đủ |
| `allowed_roles` | 0 | 0 | ✅ PASS | Bắt buộc 100% đầy đủ |

- **Trường `article` (Điều/Khoản):** 100% đầy đủ (24/ 24 chunks)
- **Trường `citation` (Trích dẫn chuẩn):** 100% đầy đủ (24/ 24 chunks)
- **Trường `allowed_roles` (Phân quyền RBAC):** 100% đầy đủ (24/ 24 chunks)

---

## 5. Kết luận & Sẵn sàng cho UC3 & UC4

Tập dữ liệu đã được cataloging đầy đủ, chính xác, đảm bảo 14 trường metadata và sẵn sàng 100% cho việc phát triển **UC3 (AI Compliance Checker)** và **UC4 (AI Audit Checklist Generator)**.

```plaintext
DATA CATALOGING: PASS
DOMAINS DETECTED: 10
READY FOR UC3 & UC4: YES
```
