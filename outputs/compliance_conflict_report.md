# BÁO CÁO PHÁT HIỆN MÂU THUẪN & XUNG ĐỘT TUÂN THỦ (UC3 - AI COMPLIANCE CHECKER)
**Ngày thực hiện:** 2026-08-26 21:45:02  
**LLM Engine:** `ollama`  
**Tổng số cặp quy định quét:** 3  
**Tổng số xung đột phát hiện:** 3  
**Trạng thái kiểm toán:** Tất cả các phát hiện được gán nhãn `NEEDS_HUMAN_REVIEW` bắt buộc chuyên viên thẩm định.

---

## 1. Bảng Tổng quan Danh sách Xung đột Tuân thủ

| Mã Xung Đột | Miền Nghiệp Vụ | Loại Xung Đột | Mức Độ Rủi Ro (Severity) | Trích Dẫn VB A | Trích Dẫn VB B | Trạng Thái Review |
|---|---|---|---|---|---|---|
| `CFL_8BF7074B` | **An toàn kho quỹ & Vận chuyển tiền mặt** | `QUY_TRINH` | 🔴 `HIGH` | `agr_at01` | `44209` | `NEEDS_HUMAN_REVIEW` |
| `CFL_ED68F1EC` | **CAR & Quản lý rủi ro** | `QUY_TRINH` | 🔴 `HIGH` | `agr_car02` | `117310` | `NEEDS_HUMAN_REVIEW` |
| `CFL_3E2A93B0` | **Tín dụng & Phân cấp phê duyệt** | `QUY_TRINH` | 🔴 `HIGH` | `agr_td03` | `agr_xln10` | `NEEDS_HUMAN_REVIEW` |

---

## 2. Chi tiết Phân tích So sánh Chéo (Cross-Comparison Cards)

### [1] Mã Xung Đột: `CFL_8BF7074B` — Domain: An toàn kho quỹ & Vận chuyển tiền mặt
- **Loại xung đột:** `QUY_TRINH`
- **Mức độ rủi ro (Severity):** **HIGH**
- **Trạng thái phê duyệt:** `NEEDS_HUMAN_REVIEW`

#### Đối chiếu Trực tiếp Bằng chứng:
| Đặc điểm | Văn bản A (Quy định Nội bộ) | Văn bản B (Quy định Đối chiếu) |
|---|---|---|
| **Mã Văn Bản** | `agr_at01` | `44209` |
| **Trích Dẫn Gốc (Citation)** | `[100/QĐ-NHNO-AT - Quy định nội bộ số 100/QĐ-NHNO-AT | Điều 12 | doc_agr_at01_02]` | `[01/2014/TT-NHNN - Thông tư số 01/2014/TT-NHNN Quy định về giao nhận, bảo quản, vận chuyển tiền mặt, tài sản quý, giấy tờ có giá | Điều 1. Phạm vi điều chỉnh | doc_44209_điều_1__phạm_vi_điều_chỉnh_1]` |
| **Nội Dung Trích Yếu** | Khi tiến hành vận chuyển tiền mặt có giá trị từ 3 tỷ đồng trở lên hoặc tuyến đường di chuyển liên tỉnh, Agribank bắt buộc bố trí xe ô tô bọc thép chuyên dùng và 02 bảo vệ chuyên trách trang bị công cụ hỗ trợ. Hạn mức vận chuyển không quá 50 tỷ đồng mỗi chuyến. | Văn bản: Thông tư số 01/2014/TT-NHNN Quy định về giao nhận, bảo quản, vận chuyển tiền mặt, tài sản quý, giấy tờ có giá (Số ký hiệu: 01/2014/TT-NHNN)
Điều 1. Phạm vi điều chỉnh
Điều 1. Phạm vi điều chỉnh
1. Thông tư này quy định việc giao nhận, bảo quản, vận chuyển; kiểm tra, kiểm kê, bàn giao, xử lý thừa thiếu tiền mặt, tài sản quý, giấy tờ có giá trong ngành Ngân hàng; việc thu, chi tiền mặt giữa Ngân hàng Nhà nước, tổ chức tín dụng, chi nhánh ngân hàng nước ngoài và khách hàng.
2. Việc đóng gói, niêm phong, kiểm đếm, giao nhận vàng, các loại kim khí quý, đá quý và các tài sản quý khác không thuộc phạm vi điều chỉnh của Thông tư này. |

#### 🔍 Phân tích chi tiết từ AI Compliance Engine:
> Phát hiện mâu thuẫn giữa 2 quy định.

---
### [2] Mã Xung Đột: `CFL_ED68F1EC` — Domain: CAR & Quản lý rủi ro
- **Loại xung đột:** `QUY_TRINH`
- **Mức độ rủi ro (Severity):** **HIGH**
- **Trạng thái phê duyệt:** `NEEDS_HUMAN_REVIEW`

#### Đối chiếu Trực tiếp Bằng chứng:
| Đặc điểm | Văn bản A (Quy định Nội bộ) | Văn bản B (Quy định Đối chiếu) |
|---|---|---|
| **Mã Văn Bản** | `agr_car02` | `117310` |
| **Trích Dẫn Gốc (Citation)** | `[250/QĐ-NHNO-QLRR - Quy định nội bộ số 250/QĐ-NHNO-QLRR | Điều 18 | doc_agr_car02_02]` | `[41/2016/TT-NHNN - Thông tư số 41/2016/TT-NHNN Quy định tỷ lệ an toàn vốn đối với ngân hàng, chi nhánh ngân hàng nước ngoài | Điều 1. Phạm vi điều chỉnh và đối tượng áp dụng | doc_117310_điều_1__phạm_vi_điều_chỉnh_và_đối_tượng_áp_dụng_1]` |
| **Nội Dung Trích Yếu** | Trọng số rủi ro đối với tài sản có là khoản vay bất động sản kinh doanh áp dụng mức 150% đến 200% tùy theo tỷ lệ LTV. Các khoản vay nông nghiệp nông thôn được ưu đãi hệ số rủi ro 50% theo định hướng phát triển của Agribank. | Văn bản: Thông tư số 41/2016/TT-NHNN Quy định tỷ lệ an toàn vốn đối với ngân hàng, chi nhánh ngân hàng nước ngoài (Số ký hiệu: 41/2016/TT-NHNN)
Điều 1. Phạm vi điều chỉnh và đối tượng áp dụng
Điều 1. Phạm vi điều chỉnh và đối tượng áp dụng
1. Thông tư này quy định tỷ lệ an toàn vốn đối với ngân hàng, chi nhánh ngân hàng nước ngoài tại Việt Nam.
2. Đối tượng áp dụng gồm:
a) Ngân hàng: Ngân hàng thương mại nhà nước, ngân hàng thương mại cổ phần, ngân hàng liên doanh, ngân hàng 100% vốn nước ngoài;
b) Chi nhánh ngân hàng nước ngoài.
3. Thông tư này không áp dụng đối với các ngân hàng được đặt vào kiểm soát đặc biệt. |

#### 🔍 Phân tích chi tiết từ AI Compliance Engine:
> Phát hiện mâu thuẫn giữa 2 quy định.

---
### [3] Mã Xung Đột: `CFL_3E2A93B0` — Domain: Tín dụng & Phân cấp phê duyệt
- **Loại xung đột:** `QUY_TRINH`
- **Mức độ rủi ro (Severity):** **HIGH**
- **Trạng thái phê duyệt:** `NEEDS_HUMAN_REVIEW`

#### Đối chiếu Trực tiếp Bằng chứng:
| Đặc điểm | Văn bản A (Quy định Nội bộ) | Văn bản B (Quy định Đối chiếu) |
|---|---|---|
| **Mã Văn Bản** | `agr_td03` | `agr_xln10` |
| **Trích Dẫn Gốc (Citation)** | `[315/QC-NHNO-TD - Quy chế tín dụng nội bộ số 315/QC-NHNO-TD | Điều 22 | doc_agr_td03_02]` | `[390/QĐ-NHNO-XLN - Quy định nội bộ số 390/QĐ-NHNO-XLN | Điều 23 | doc_agr_xln10_02]` |
| **Nội Dung Trích Yếu** | Tất cả các khoản vay ngắn hạn phục vụ sản xuất nông nghiệp không có tài sản bảo đảm theo Nghị định 55/2015/NĐ-CP được Agribank giải ngân lên tới 100 triệu đồng đối với cá nhân, hộ gia đình nông dân trên cơ sở xác nhận của Ủy ban nhân dân xã. | Việc cơ cấu lại thời hạn trả nợ và giữ nguyên nhóm nợ cho khách hàng gặp khó khăn do thiên tai, dịch bệnh được thực hiện theo đúng hướng dẫn của Ngân hàng Nhà nước và phải được Hội đồng Rủi ro Agribank thông qua. |

#### 🔍 Phân tích chi tiết từ AI Compliance Engine:
> Phát hiện mâu thuẫn giữa 2 quy định.

---

## 3. Nhật ký Ghi vết Kiểm toán (Audit Trail Summary)

Tất cả các truy vấn so sánh chéo đã được lưu trữ không thể sửa xóa tại `outputs/audit_log.jsonl`.
- **Tổng số Request IDs:** 3
- **Guardrail Chống Bịa Thông Tin:** 100% Trích dẫn sử dụng Citation thật từ tập dữ liệu.
- **Guardrail Phê Duyệt Con Người:** 100% kết quả có `review_status = "NEEDS_HUMAN_REVIEW"`.

---

```plaintext
COMPLIANCE CHECKER ENGINE: PASS
LLM_PROVIDER: ollama
CONFLICTS DETECTED: 3
HUMAN REVIEW GUARDRAIL: PASS
```
