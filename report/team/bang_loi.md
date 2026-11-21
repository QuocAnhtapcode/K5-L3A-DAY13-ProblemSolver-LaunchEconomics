# Bảng lỗi và cách khắc phục · Nhiệm vụ C

20 ca lỗi nằm trong `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`. Năm loại theo Google PAIR: **Do người dùng · Hệ thống · Ngữ cảnh · Giới hạn hệ thống · Ngầm**. Gắn nhãn theo nguyên nhân gốc, không theo chỗ cần sửa.

## Hai bộ nhãn độc lập

Người gắn nhãn 1: Hùng · Người gắn nhãn 2: Bình (gắn độc lập, không trao đổi trước khi so)

| Ca | Nhãn người 1 | Nhãn người 2 | Trùng? | Nhãn thống nhất |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | Do người dùng | Có | Do người dùng |
| 2 | Hệ thống | Hệ thống | Có | Hệ thống |
| 3 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 4 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 5 | Ngầm | Ngầm | Có | Ngầm |
| 6 | Do người dùng | Do người dùng | Có | Do người dùng |
| 7 | Hệ thống | Hệ thống | Có | Hệ thống |
| 8 | Hệ thống | Hệ thống | Có | Hệ thống |
| 9 | Do người dùng | Do người dùng | Có | Do người dùng |
| 10 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 11 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 12 | Ngầm | Ngầm | Có | Ngầm |
| 13 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 14 | Do người dùng | Do người dùng | Có | Do người dùng |
| 15 | Hệ thống | Hệ thống | Có | Hệ thống |
| 16 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 17 | Ngầm | Ngầm | Có | Ngầm |
| 18 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 19 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 20 | Hệ thống | Hệ thống | Có | Hệ thống |

**Tỉ lệ đồng thuận:** 20 / 20 = 100%

Phân bố: Do người dùng 4 ca (1, 6, 9, 14) · Hệ thống 5 ca (2, 7, 8, 15, 20) · Ngữ cảnh 4 ca (3, 10, 16, 18) · Giới hạn hệ thống 4 ca (4, 11, 13, 19) · Ngầm 3 ca (5, 12, 17).

## Quy tắc phân biệt cho các ca không trùng

Không có ca không trùng. Các quy tắc nhóm đã dùng cho những ca dễ lẫn:

- Ca 6, 9: gốc lỗi là khách chọn sai mục hoặc nhập sai mã, nên là Do người dùng; việc trợ lý không gợi ý nằm ở cột khắc phục.
- Ca 8, 15: sai đã lộ ra (trích dẫn nhìn thấy được, nhân viên bắt được) nên là Hệ thống, không phải Ngầm.
- Ca 12: kết quả đúng nhưng chi phí gấp 3 lần suốt 3 tuần mà không ai thấy, nên là Ngầm; "sai" có thể là sai về chi phí.
- Ca 13: ngoài phạm vi thì là Giới hạn hệ thống, kể cả khi trợ lý xử lý giới hạn đó kém.

## Bảng khắc phục cho 5 ca, mỗi loại một ca

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --: | --- | --- | --- | --- |
| 9 | Do người dùng | Event `input_validation_failed` (reason = ma_san_tmdt), đếm theo ngày; cảnh báo khi vượt 2% số yêu cầu/ngày | Nhận diện mã sàn TMĐT bằng regex và hướng dẫn khách cách lấy mã vận đơn LogiX | PM trợ lý hoàn phí |
| 7 | Hệ thống | Đối soát mỗi giờ: tin nhắn "đã hoàn" không có bản ghi `refund_ledger_write` thành công cùng `trace_id`; ngưỡng 0 ca | Chỉ báo thành công khi sổ cái trả 200 OK; nếu 503 sau 3 lần thì báo "đang xử lý", đẩy vào hàng đợi và chuyển nhân viên | Kỹ sư trưởng agent |
| 18 | Ngữ cảnh | Event `ticket_reopened` với lý do số tiền mà kiểm tra thấy số tiền đúng, tính theo tuần; ngưỡng 1% số yêu cầu đã đóng | Mẫu tin nhắn luôn ghi công thức: phí gốc 30.000 đ × mức hoàn 50% = 15.000 đ | Trưởng nhóm CSKH |
| 4 | Giới hạn hệ thống | Event `handoff_to_staff` với reason = thieu_du_lieu, tính theo loại yêu cầu mỗi tuần | Giữ luồng chuyển nhân viên kèm tóm tắt và giải thích lý do thiếu dữ liệu; đưa quoc_te ra khỏi phạm vi pilot (1,88× theo A3 [simulated]) | PM trợ lý hoàn phí |
| 17 | Ngầm | Kiểm tra mẫu 100 đơn/tuần so với bảng giá hiện hành (event `audit_sample_checked`); ngưỡng 1% đơn lệch | Xoá bộ nhớ đệm tự động mỗi khi cập nhật bảng giá mới; ghi phiên bản bảng giá vào trace | Kế toán trưởng |
