# SPEC Buổi 05

## Mục tiêu

Xây dựng chương trình demo xử lý tài liệu PDF tiếng Việt và so sánh ba
chiến lược chia nhỏ (chunking). Phạm vi chỉ ở mức đơn giản, dễ hiểu,
không phức tạp hóa.

## Đầu vào

-   Thư mục đầu vào: `datademo/`
-   Dữ liệu đầu vào:
    -   Các tệp PDF tiếng Việt.
-   Chương trình cần duyệt các tệp PDF trong thư mục trên để xử lý.

## Đầu ra

Đối với mỗi PDF sau khi xử lý OCR, tạo dữ liệu gồm:

-   `text`: Nội dung OCR chuẩn hóa Unicode **NFC**.
-   `metadata`:
    -   `source`: tên tệp PDF nguồn.
    -   `page`: số trang.
    -   `ocr_used`: cho biết có sử dụng OCR hay không.
    -   `language`: ngôn ngữ nhận dạng (ví dụ: `vi` hoặc `vi+en` tùy cấu
        hình).

Ngoài dữ liệu OCR, cần sinh **báo cáo so sánh** của ba chiến lược
chunking.

## Ba chiến lược chunking cần so sánh

### 1. Fixed-size

-   Chia theo số ký tự hoặc số token.
-   Có sử dụng overlap giữa các chunk.
-   Báo cáo:
    -   số lượng chunk,
    -   kích thước trung bình,
    -   overlap đã dùng.

### 2. Semantic

-   Ưu tiên cắt theo ranh giới tự nhiên của văn bản.
-   Thứ tự ưu tiên:
    -   ngắt đoạn,
    -   kết đoạn,
    -   dòng trống/cách dòng.
-   Chỉ sử dụng quy tắc đơn giản, không dùng LLM.

### 3. Hierarchical

-   Chia theo cấu trúc văn bản.
-   Mỗi mốc sau phải được xem là điểm bắt đầu của một chunk:
    -   Chương
    -   Mục
    -   Điều/Khoản
    -   Điểm
-   Nếu không phát hiện được cấu trúc thì có thể rơi về quy tắc đơn giản
    phù hợp.

## Báo cáo cần xuất

Báo cáo phải thể hiện tối thiểu:

-   số chunk của từng chiến lược;
-   kích thước trung bình của chunk;
-   kích thước nhỏ nhất/lớn nhất;
-   nhận xét ngắn về sự khác nhau giữa ba cách chia.

## Quy định về cấu hình

-   Phải sử dụng các key được khai báo trong tệp `.env` nằm trong thư
    mục `src`.
-   Chỉ được đọc **tên biến môi trường** để sử dụng khi chạy chương
    trình.
-   **Không được phép đọc, in, ghi log, hiển thị hoặc tiết lộ giá trị
    của bất kỳ key nào** trong `.env`.

## Các yêu cầu bắt buộc

-   Không tạo embedding.
-   Không lưu vector database.
-   Không gọi LLM dưới bất kỳ hình thức nào trong Buổi 5.
-   Chỉ thực hiện:
    -   đọc PDF,
    -   OCR,
    -   chuẩn hóa Unicode NFC,
    -   tạo metadata,
    -   thực hiện ba chiến lược chunking,
    -   sinh báo cáo so sánh.
-   Mã nguồn ở mức demo đơn giản, rõ ràng, dễ đọc.
-   Không bổ sung kiến trúc hoặc tính năng ngoài phạm vi yêu cầu.
-   Không bỏ sót bất kỳ yêu cầu nào nêu trong tài liệu đặc tả này.
