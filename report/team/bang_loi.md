# Bảng lỗi và cách khắc phục · Nhiệm vụ C

Nguồn: 20 ca trong `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`; bộ nhãn người dùng đã gửi trong cuộc trò chuyện, đối chiếu với hướng dẫn chi tiết của lab. Gắn theo nguyên nhân gốc.

## Hai bộ nhãn độc lập

Bộ 1: người dùng cung cấp; chưa có họ tên người gắn nhãn, chưa xác nhận điều kiện gắn độc lập trước khi xem tài liệu. Bộ 2: **Chưa có**. Vì vậy **CP3 chưa đủ bằng chứng độc lập**, dù bộ đã cung cấp khớp 20/20 nhãn tham khảo.

| Ca | Nhãn người dùng cung cấp | Nhãn người 2 | Trùng | Nhãn thống nhất | Lý do bộ đã cung cấp |
| --- | --- | --- | --- | --- | --- |
| 1 | Do người dùng | Chưa có | Chưa tính | Chưa chốt | Nhập thiếu hai chữ số tài khoản. |
| 2 | Hệ thống | Chưa có | Chưa tính | Chưa chốt | Chọn sai loại hàng, khách phát hiện hoàn thiếu. |
| 3 | Ngữ cảnh | Chưa có | Chưa tính | Chưa chốt | Hoàn ví đúng thiết kế, khách chờ ngân hàng. |
| 4 | Giới hạn hệ thống | Chưa có | Chưa tính | Chưa chốt | Không có dữ liệu chặng nước ngoài. |
| 5 | Ngầm | Chưa có | Chưa tính | Chưa chốt | Hoàn thừa do mã giảm giá, chỉ kiểm tra mẫu phát hiện. |
| 6 | Do người dùng | Chưa có | Chưa tính | Chưa chốt | Khách chọn sai mục yêu cầu. |
| 7 | Hệ thống | Chưa có | Chưa tính | Chưa chốt | Sổ cái thất bại nhưng vẫn báo thành công. |
| 8 | Hệ thống | Chưa có | Chưa tính | Chưa chốt | Trích dẫn điều khoản không tồn tại. |
| 9 | Do người dùng | Chưa có | Chưa tính | Chưa chốt | Nhập mã sàn thay mã vận đơn. |
| 10 | Ngữ cảnh | Chưa có | Chưa tính | Chưa chốt | Đúng chính sách nhưng thông điệp cam kết tạo kỳ vọng khác. |
| 11 | Giới hạn hệ thống | Chưa có | Chưa tính | Chưa chốt | Không hỗ trợ xử lý âm thanh. |
| 12 | Ngầm | Chưa có | Chưa tính | Chưa chốt | Kết quả đúng nhưng chi phí gấp ba âm thầm kéo dài. |
| 13 | Giới hạn hệ thống | Chưa có | Chưa tính | Chưa chốt | Bảo hiểm ngoài phạm vi trợ lý. |
| 14 | Do người dùng | Chưa có | Chưa tính | Chưa chốt | Bấm nhầm xác nhận đã nhận tiền. |
| 15 | Hệ thống | Chưa có | Chưa tính | Chưa chốt | Sai tỷ lệ hoàn, nhân viên bắt được. |
| 16 | Ngữ cảnh | Chưa có | Chưa tính | Chưa chốt | Gửi đúng thiết kế nhưng sai thời điểm với khách. |
| 17 | Ngầm | Chưa có | Chưa tính | Chưa chốt | Bảng giá cache cũ gây sai tiền, không ai phản ánh. |
| 18 | Ngữ cảnh | Chưa có | Chưa tính | Chưa chốt | Số tiền đúng nhưng thiếu cách tính. |
| 19 | Giới hạn hệ thống | Chưa có | Chưa tính | Chưa chốt | Vượt giới hạn truy cập dữ liệu 12 tháng. |
| 20 | Hệ thống | Chưa có | Chưa tính | Chưa chốt | Thiếu khóa chống trùng gây hoàn hai lần. |

**Tỷ lệ đồng thuận: Chưa tính**, cần hai bộ nhãn thực tế. Công thức: số ca hai người gắn cùng nhãn / 20 × 100%; yêu cầu ít nhất 16/20 = 80%, hoặc làm rõ định nghĩa theo checkpoint.

## Quy tắc phân biệt

- Ca 6 và 9: đầu vào sai là nguyên nhân gốc; gợi ý tốt hơn là khắc phục.
- Ca 13: ngoài phạm vi là giới hạn; nói rõ giới hạn là khắc phục.
- Ca 8 và 15: lỗi có thể nhận ra trực tiếp/đã bị bắt; ca 5 và 17 chỉ lộ khi kiểm tra là ngầm.
- Ca 12: chi phí tăng mà không ai biết cũng là lỗi ngầm dù câu trả lời đúng.
- Ca 18: số tiền đúng, kỳ vọng không khớp vì thiếu giải thích nên là ngữ cảnh.
- Ca 20: gửi lại yêu cầu là tình huống cần hỗ trợ; chống hoàn trùng thuộc trách nhiệm hệ thống.

Sau khi có bộ 2, giữ nguyên hai bộ gốc, ghi riêng từng ca không trùng và quy tắc thống nhất; chưa có dữ liệu để mô tả bất đồng thực tế.

## Bảng khắc phục cho 5 ca

Các ngưỡng sau là đề xuất cho pilot; chưa có event vận hành thật để xác nhận.

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --- | --- | --- | --- | --- |
| 9 | Do người dùng | input_validation_failed, trace_id, loại mã; cảnh báo >2% yêu cầu/ngày | Nhận diện mã sàn và tra sang mã vận đơn; không tra được thì hướng dẫn khách | PM trợ lý hoàn phí |
| 7 | Hệ thống | Đối soát mỗi giờ thông báo đã hoàn với sổ cái thành công cùng trace_id; ngưỡng 1 ca không khớp | Chỉ báo thành công khi sổ cái xác nhận; lỗi thì chờ xử lý và chuyển nhân viên | Kỹ sư trưởng agent |
| 18 | Ngữ cảnh | Hằng tuần đếm mở lại vì thiếu tiền nhưng audit xác nhận đúng; cảnh báo từ 3 ca/tuần | Tin nhắn ghi rõ 30.000 đ × 50% = 15.000 đ và kênh nhận | Trưởng nhóm CSKH |
| 4 | Giới hạn hệ thống | handoff_to_staff với reason=thieu_du_lieu và trace_id; tổng hợp hằng tuần theo loại | Chuyển kèm tóm tắt; loại chặng thiếu dữ liệu khỏi pilot | PM trợ lý hoàn phí |
| 17 | Ngầm | audit_sample_checked đối chiếu 100 đơn/tuần với bảng giá hiện hành; từ 1 đơn sai thì cảnh báo | Vô hiệu cache khi đổi giá, ghi policy_version vào trace và rà đơn bị ảnh hưởng | Kế toán trưởng |
