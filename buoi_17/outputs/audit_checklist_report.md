# BÁO CÁO DANH MỤC CHECKLIST KIỂM TOÁN TỰ ĐỘNG (UC4 - AI AUDIT CHECKLIST GENERATOR)
**Ngày thực hiện:** 2026-08-24 21:08:25  
**Tổng số mục Checklist đã sinh:** 8  
**Miền nghiệp vụ kiểm thử:** 
1. An toàn kho quỹ & Vận chuyển tiền mặt (Đơn vị: Chi nhánh loại 1 Agribank)
2. Bảo mật CNTT & AI (Đơn vị: Khối Công nghệ Thông tin Agribank)

---

## 1. Bảng Tổng quan Danh mục Checklist Kiểm toán

| STT | Mã Mục | Miền Nghiệp Vụ | Đơn Vị Áp Dụng | Mức Rủi Ro | Câu Hỏi Kiểm Toán | Trích Dẫn Văn Bản Gốc (Citation) | Trạng Thái Review |
|---|---|---|---|---|---|---|---|
| 1 | `CHK_KHO_QUY_01` | **An toàn kho quỹ & Vận chuyển tiền** | Chi nhánh loại 1 Agribank | 🔴 `HIGH` | Chi nhánh đã ban hành và triển khai đầy đủ quy trình giao nhận, bảo quản, vận chuyển tiền mặt, tài sản quý và giấy tờ có giá theo đúng phạm vi quy định của Ngân hàng Nhà nước chưa? | `Khoản 1 Điều 1 Thông tư số 01/2014/TT-NHNN` | `NEEDS_HUMAN_REVIEW` |
| 2 | `CHK_KHO_QUY_02` | **An toàn kho quỹ & Vận chuyển tiền** | Chi nhánh loại 1 Agribank | 🔴 `HIGH` | Chi nhánh có thực hiện kiểm tra, kiểm kê, bàn giao và xử lý thừa, thiếu tiền mặt, tài sản quý, giấy tờ có giá đúng quy định trong giao dịch nội bộ và giao dịch với khách hàng không? | `Khoản 1 Điều 1 và Khoản 3 Điều 2 Thông tư số 01/2014/TT-NHNN` | `NEEDS_HUMAN_REVIEW` |
| 3 | `CHK_KHO_QUY_03` | **An toàn kho quỹ & Vận chuyển tiền** | Chi nhánh loại 1 Agribank | 🟡 `MEDIUM` | Chi nhánh có tách biệt rõ ràng quy trình đóng gói, niêm phong, kiểm đếm, giao nhận đối với vàng, kim khí quý, đá quý (thuộc quy định riêng) với quy trình quản lý tiền mặt và giấy tờ có giá không? | `Khoản 2 Điều 1 Thông tư số 01/2014/TT-NHNN` | `NEEDS_HUMAN_REVIEW` |
| 4 | `CHK_KHO_QUY_04` | **An toàn kho quỹ & Vận chuyển tiền** | Chi nhánh loại 1 Agribank | 🔴 `HIGH` | Chi nhánh có quán triệt và áp dụng đúng nghĩa vụ tuân thủ quy định giao nhận, bảo quản, vận chuyển tiền mặt đối với tất cả các đối tượng liên quan (cán bộ kho quỹ, giao dịch viên, khách hàng giao dịch) không? | `Điều 2 Thông tư số 01/2014/TT-NHNN` | `NEEDS_HUMAN_REVIEW` |
| 5 | `CHK_IT_CASH_01` | **Bảo mật CNTT & AI** | Khối Công nghệ Thông tin Agribank | 🔴 `HIGH` | Hệ thống phần mềm quản lý kho quỹ và hạch toán do Khối CNTT vận hành có được cấu hình kiểm soát chuẩn xác các quy tắc định dạng quy quy cách đóng gói tiền mặt (bó, bao, túi, hộp, thùng tiền) và mã hóa thông tin niêm phong, kẹp chì hay không? | `Khoản 7, Khoản 8 Điều 3 và Khoản 1, 2, 3, 4, 5 Điều 4 Thông tư số 01/2014/TT-NHNN` | `NEEDS_HUMAN_REVIEW` |
| 6 | `CHK_IT_CASH_02` | **Bảo mật CNTT & AI** | Khối Công nghệ Thông tin Agribank | 🔴 `HIGH` | Ứng dụng CNTT/Giải pháp AI tự động nhận diện và kiểm đếm tiền mặt, tài sản quý, giấy tờ có giá có đảm bảo độ chính xác trong việc phân loại mệnh giá, đếm số lượng tờ/miếng và lưu trữ toàn bộ lịch sử giao dịch không? | `Khoản 1, 3, 4, 5, 6 Điều 3 Thông tư số 01/2014/TT-NHNN` | `NEEDS_HUMAN_REVIEW` |
| 7 | `CHK_IT_CASH_03` | **Bảo mật CNTT & AI** | Khối Công nghệ Thông tin Agribank | 🟡 `MEDIUM` | Hệ thống luồng công việc (Workflow) quản lý giao nhận tiền mặt có thiết lập tính năng kiểm soát thời hạn kiểm đếm (tối đa 05 ngày làm việc đối với TCTD) và bắt buộc phân quyền ghi nhận thành viên Hội đồng kiểm đếm, người chứng kiến hay không? | `Khoản 2, Khoản 3 Điều 12 Thông tư số 01/2014/TT-NHNN` | `NEEDS_HUMAN_REVIEW` |
| 8 | `CHK_IT_CASH_04` | **Bảo mật CNTT & AI** | Khối Công nghệ Thông tin Agribank | 🔴 `HIGH` | Hệ thống giám sát an ninh CNTT và camera AI tại khu vực kiểm đếm, niêm phong kho quỹ có đảm bảo bảo mật dữ liệu video, lưu trữ đủ thời hạn và tự động phát hiện các bất thường trong quá trình đóng gói, kẹp chì không? | `Khoản 7, Khoản 8 Điều 3 và Khoản 3 Điều 12 Thông tư số 01/2014/TT-NHNN` | `NEEDS_HUMAN_REVIEW` |

---

## 2. Chi tiết Các Mục Kiểm toán & Kiến nghị Xử lý (Audit Cards)

### [1] Mã Mục: `CHK_KHO_QUY_01` — Chi nhánh đã ban hành và triển khai đầy đủ quy trình giao nhận, bảo quản, vận chuyển tiền mặt, tài sản quý và giấy tờ có giá theo đúng phạm vi quy định của Ngân hàng Nhà nước chưa?
- **Miền nghiệp vụ:** An toàn kho quỹ & Vận chuyển tiền
- **Đơn vị được kiểm toán:** Chi nhánh loại 1 Agribank
- **Mức độ rủi ro:** **HIGH**
- **Trích dẫn điều khoản gốc:** `Khoản 1 Điều 1 Thông tư số 01/2014/TT-NHNN`
- **Trạng thái kiểm toán:** `NEEDS_HUMAN_REVIEW`

#### ⚠️ Rủi ro tiềm ẩn nếu vi phạm:
> Không tuân thủ đầy đủ quy trình quy định dẫn đến nguy cơ thất thoát tài sản, mất an toàn kho quỹ hoặc bị xử phạt vi phạm hành chính trong lĩnh vực tiền tệ - ngân hàng.

#### 💡 Kiến nghị hành động kiểm toán (Recommendations):
> Kiểm toán viên thực hiện rà soát toàn bộ văn bản quy định nội bộ của Chi nhánh, đối chiếu với phạm vi điều chỉnh của Thông tư 01/2014/TT-NHNN để đảm bảo không bỏ sót quy trình nghiệp vụ nào.

---
### [2] Mã Mục: `CHK_KHO_QUY_02` — Chi nhánh có thực hiện kiểm tra, kiểm kê, bàn giao và xử lý thừa, thiếu tiền mặt, tài sản quý, giấy tờ có giá đúng quy định trong giao dịch nội bộ và giao dịch với khách hàng không?
- **Miền nghiệp vụ:** An toàn kho quỹ & Vận chuyển tiền
- **Đơn vị được kiểm toán:** Chi nhánh loại 1 Agribank
- **Mức độ rủi ro:** **HIGH**
- **Trích dẫn điều khoản gốc:** `Khoản 1 Điều 1 và Khoản 3 Điều 2 Thông tư số 01/2014/TT-NHNN`
- **Trạng thái kiểm toán:** `NEEDS_HUMAN_REVIEW`

#### ⚠️ Rủi ro tiềm ẩn nếu vi phạm:
> Xử lý thừa thiếu tiền mặt không kịp thời hoặc không đúng quy trình dẫn đến rủi ro chiếm dụng vốn, thất thoát tài sản, hoặc phát sinh tranh chấp kéo dài với khách hàng.

#### 💡 Kiến nghị hành động kiểm toán (Recommendations):
> Kiểm tra xác xuất các biên bản kiểm kê quỹ định kỳ/đột xuất, sổ quỹ, biên bản xử lý thừa thiếu tiền mặt tại các quầy giao dịch và kho tiền Chi nhánh.

---
### [3] Mã Mục: `CHK_KHO_QUY_03` — Chi nhánh có tách biệt rõ ràng quy trình đóng gói, niêm phong, kiểm đếm, giao nhận đối với vàng, kim khí quý, đá quý (thuộc quy định riêng) với quy trình quản lý tiền mặt và giấy tờ có giá không?
- **Miền nghiệp vụ:** An toàn kho quỹ & Vận chuyển tiền
- **Đơn vị được kiểm toán:** Chi nhánh loại 1 Agribank
- **Mức độ rủi ro:** **MEDIUM**
- **Trích dẫn điều khoản gốc:** `Khoản 2 Điều 1 Thông tư số 01/2014/TT-NHNN`
- **Trạng thái kiểm toán:** `NEEDS_HUMAN_REVIEW`

#### ⚠️ Rủi ro tiềm ẩn nếu vi phạm:
> Nhầm lẫn giữa các văn bản quy phạm pháp luật áp dụng đối với vàng, đá quý và tiền mặt có thể dẫn đến việc thực hiện sai quy trình bảo vệ, đóng gói niêm phong, gây khó khăn khi truy xuất trách nhiệm.

#### 💡 Kiến nghị hành động kiểm toán (Recommendations):
> Rà soát danh mục văn bản nghiệp vụ áp dụng tại Chi nhánh đối với mảng vàng/đá quý để đảm bảo tách biệt đúng cơ sở pháp lý và quy trình niêm phong, lưu kho.

---
### [4] Mã Mục: `CHK_KHO_QUY_04` — Chi nhánh có quán triệt và áp dụng đúng nghĩa vụ tuân thủ quy định giao nhận, bảo quản, vận chuyển tiền mặt đối với tất cả các đối tượng liên quan (cán bộ kho quỹ, giao dịch viên, khách hàng giao dịch) không?
- **Miền nghiệp vụ:** An toàn kho quỹ & Vận chuyển tiền
- **Đơn vị được kiểm toán:** Chi nhánh loại 1 Agribank
- **Mức độ rủi ro:** **HIGH**
- **Trích dẫn điều khoản gốc:** `Điều 2 Thông tư số 01/2014/TT-NHNN`
- **Trạng thái kiểm toán:** `NEEDS_HUMAN_REVIEW`

#### ⚠️ Rủi ro tiềm ẩn nếu vi phạm:
> Không làm rõ trách nhiệm của các đối tượng tham gia vào quá trình thu, chi, bảo quản tiền mặt gây rủi ro thông đồng gian lận hoặc thiếu trách nhiệm khi xảy ra sự cố an toàn kho quỹ.

#### 💡 Kiến nghị hành động kiểm toán (Recommendations):
> Yêu cầu Chi nhánh cung cấp văn bản phân công nhiệm vụ, bản cam kết trách nhiệm cá nhân của các thành viên Ban quản lý kho tiền và cán bộ làm công tác vận chuyển, giao nhận tiền mặt.

---
### [5] Mã Mục: `CHK_IT_CASH_01` — Hệ thống phần mềm quản lý kho quỹ và hạch toán do Khối CNTT vận hành có được cấu hình kiểm soát chuẩn xác các quy tắc định dạng quy quy cách đóng gói tiền mặt (bó, bao, túi, hộp, thùng tiền) và mã hóa thông tin niêm phong, kẹp chì hay không?
- **Miền nghiệp vụ:** Bảo mật CNTT & AI
- **Đơn vị được kiểm toán:** Khối Công nghệ Thông tin Agribank
- **Mức độ rủi ro:** **HIGH**
- **Trích dẫn điều khoản gốc:** `Khoản 7, Khoản 8 Điều 3 và Khoản 1, 2, 3, 4, 5 Điều 4 Thông tư số 01/2014/TT-NHNN`
- **Trạng thái kiểm toán:** `NEEDS_HUMAN_REVIEW`

#### ⚠️ Rủi ro tiềm ẩn nếu vi phạm:
> Hệ thống CNTT cho phép ghi nhận sai quy cách đóng gói (sai tỷ lệ quy đổi số tờ/thếp/bó/bao/túi) hoặc không quản lý chặt chẽ dữ liệu niêm phong/kẹp chì, dẫn đến sai lệch số liệu kế toán kho quỹ, tiềm ẩn nguy cơ thất thoát tiền mặt và vi phạm quy định NHNN.

#### 💡 Kiến nghị hành động kiểm toán (Recommendations):
> Đoàn kiểm toán thực hiện kiểm tra cấu hình tham số hệ thống (system parameters), kiểm thử dữ liệu đầu vào (validation logic) trên phần mềm Quản lý Kho quỹ/Core Banking đối với các giao dịch đóng gói tiền mặt.

---
### [6] Mã Mục: `CHK_IT_CASH_02` — Ứng dụng CNTT/Giải pháp AI tự động nhận diện và kiểm đếm tiền mặt, tài sản quý, giấy tờ có giá có đảm bảo độ chính xác trong việc phân loại mệnh giá, đếm số lượng tờ/miếng và lưu trữ toàn bộ lịch sử giao dịch không?
- **Miền nghiệp vụ:** Bảo mật CNTT & AI
- **Đơn vị được kiểm toán:** Khối Công nghệ Thông tin Agribank
- **Mức độ rủi ro:** **HIGH**
- **Trích dẫn điều khoản gốc:** `Khoản 1, 3, 4, 5, 6 Điều 3 Thông tư số 01/2014/TT-NHNN`
- **Trạng thái kiểm toán:** `NEEDS_HUMAN_REVIEW`

#### ⚠️ Rủi ro tiềm ẩn nếu vi phạm:
> Mô hình AI hoặc phần mềm tích hợp máy đếm tiền bị lỗi thuật toán, chưa được kiểm định chất lượng dẫn đến ghi nhận sai số lượng tờ/miếng tiền mặt, phân loại sai tài sản quý và giấy tờ có giá, gây tổn thất tài chính cho ngân hàng.

#### 💡 Kiến nghị hành động kiểm toán (Recommendations):
> Rà soát hồ sơ kiểm thử (testing logs), đánh giá độ chính xác của mô hình AI/phần mềm kiểm đếm tự động và kiểm tra các biện pháp kiểm soát rủi ro công nghệ khi tích hợp thiết bị đếm tiền với hệ thống CNTT trung tâm.

---
### [7] Mã Mục: `CHK_IT_CASH_03` — Hệ thống luồng công việc (Workflow) quản lý giao nhận tiền mặt có thiết lập tính năng kiểm soát thời hạn kiểm đếm (tối đa 05 ngày làm việc đối với TCTD) và bắt buộc phân quyền ghi nhận thành viên Hội đồng kiểm đếm, người chứng kiến hay không?
- **Miền nghiệp vụ:** Bảo mật CNTT & AI
- **Đơn vị được kiểm toán:** Khối Công nghệ Thông tin Agribank
- **Mức độ rủi ro:** **MEDIUM**
- **Trích dẫn điều khoản gốc:** `Khoản 2, Khoản 3 Điều 12 Thông tư số 01/2014/TT-NHNN`
- **Trạng thái kiểm toán:** `NEEDS_HUMAN_REVIEW`

#### ⚠️ Rủi ro tiềm ẩn nếu vi phạm:
> Hệ thống CNTT thiếu tính năng cảnh báo vi phạm thời hạn 05 ngày làm việc hoặc cho phép người dùng phê duyệt giao dịch kiểm đếm khi chưa có đầy đủ xác nhận điện tử/chữ ký số của Hội đồng kiểm đếm và người chứng kiến, dẫn đến rủi ro pháp lý và quy trình.

#### 💡 Kiến nghị hành động kiểm toán (Recommendations):
> Trích xuất log hệ thống quản lý giao nhận tiền mặt, kiểm tra việc cài đặt SLA cảnh báo thời hạn 05 ngày và rà soát phân quyền truy cập (matrix access control) đối với vai trò Hội đồng kiểm đếm và người chứng kiến.

---
### [8] Mã Mục: `CHK_IT_CASH_04` — Hệ thống giám sát an ninh CNTT và camera AI tại khu vực kiểm đếm, niêm phong kho quỹ có đảm bảo bảo mật dữ liệu video, lưu trữ đủ thời hạn và tự động phát hiện các bất thường trong quá trình đóng gói, kẹp chì không?
- **Miền nghiệp vụ:** Bảo mật CNTT & AI
- **Đơn vị được kiểm toán:** Khối Công nghệ Thông tin Agribank
- **Mức độ rủi ro:** **HIGH**
- **Trích dẫn điều khoản gốc:** `Khoản 7, Khoản 8 Điều 3 và Khoản 3 Điều 12 Thông tư số 01/2014/TT-NHNN`
- **Trạng thái kiểm toán:** `NEEDS_HUMAN_REVIEW`

#### ⚠️ Rủi ro tiềm ẩn nếu vi phạm:
> Dữ liệu camera giám sát quá trình niêm phong, kẹp chì và kiểm đếm bị mất mát, can thiệp hoặc truy cập trái phép do lỗ hổng bảo mật CNTT, khiến ngân hàng không có bằng chứng đối soát khi phát sinh tranh chấp hoặc thất thoát tài sản.

#### 💡 Kiến nghị hành động kiểm toán (Recommendations):
> Kiểm tra chính sách bảo mật, phân quyền truy cập và toàn vẹn dữ liệu (data integrity) của hệ thống camera giám sát/AI giám sát khu vực kiểm đếm và niêm phong kho quỹ tại Khối CNTT.

---

## 3. Xác minh Guardrails & Ghi vết Audit Trail

- **RBAC Enforcement:** Lọc đúng dữ liệu tài liệu theo User Role trước khi gửi cho LLM.
- **Citation Linking:** 100% các mục checklist gắn link trích dẫn chuẩn xác từ dataset.
- **Human Review Guardrail:** 100% mục checklist có nhãn `review_status = "NEEDS_HUMAN_REVIEW"`.
- **Audit Logger:** Đã ghi nhật ký thao tác đầy đủ vào `outputs/audit_log.jsonl`.

---

```plaintext
CHECKLIST GENERATOR ENGINE: PASS
CHECKLIST ITEMS GENERATED: 8
CITATIONS ATTACHED: YES
```
