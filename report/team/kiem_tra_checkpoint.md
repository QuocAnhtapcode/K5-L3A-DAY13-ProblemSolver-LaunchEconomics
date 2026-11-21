# Kiểm tra checkpoint sau hoàn thiện

Kiểm tra bằng `src/kiem_tra_checkpoint.py`; số từ `src/lab13.py` và hai CSV. Đây là kiểm tra kỹ thuật, không thay điểm giảng viên hoặc hội đồng.

| Phần | Kết quả | Căn cứ |
| --- | --- | --- |
| CP1 · A | ĐẠT phần phân tích | A1, A2, 4 loại A3, 2 mức A4 và báo cáo. |
| CP2 · B | ĐẠT phần phân tích | 9 kịch bản B1, B2, 3 giới hạn B3, 2 giả định B4. |
| CP3 · C | CHƯA ĐỦ | Có bộ nhãn người dùng cung cấp và 5 cách khắc phục; thiếu bộ thứ hai, tên và bằng chứng độc lập nên chưa tính đồng thuận. |
| CP4 · D | ĐẠT hồ sơ kế hoạch | D1/D2, 20 cụm/nhánh, 5.980 thực tế và 859 hiệu dụng; MDE 6 điểm, 4 luật dừng. Lịch và roster là đề xuất, chưa triển khai. |
| CP5 · E | ĐẠT nội dung E; duyệt chéo CHƯA | 3 chỉ số, 12 event, 4 rủi ro, 7 mục launch. Chưa có phiếu hội đồng thực tế. |
| Đóng gói | CHƯA ĐỦ | Thiếu xác nhận tên nhóm/lớp, danh tính và báo cáo cá nhân, đóng góp, chạy máy thứ hai, repo/commit/push/LMS. |

## Kiểm tra tự động

| Nhóm | Phép kiểm tra | Kết quả |
| --- | --- | --- |
| Chung | CSV và starter giữ nguyên byte so với trước lượt hoàn thiện; ID hợp lệ | ĐẠT |
| CP1 | Ba phép thử A1 | ĐẠT |
| CP1 | A2, bốn loại A3, hai mức A4 trong dung sai 2% của docs | ĐẠT |
| CP1 | Báo cáo A đủ bảng và số đối chiếu với chương trình | ĐẠT |
| CP2 | 9 kịch bản, cộng tác động, B3/B4, không sửa dữ liệu và lọc đúng request | ĐẠT |
| CP2 | Báo cáo B1 đủ 9 dòng, B3 đủ 3 dòng và B4 đủ 2 giả định | ĐẠT |
| CP3 | Đủ 20 ca bộ đã cung cấp và 5 loại khắc phục | ĐẠT |
| CP4 | D1/D2, YAML hợp lệ, mẫu thực tế/hiệu dụng, luật dừng và cửa sổ theo dõi | ĐẠT |
| CP5 | Ba chỉ số, event, rủi ro và hồ sơ 7 mục có đề xuất | ĐẠT |
| Chung | Đủ file, JSON khớp, không có từ cấm hoặc chỗ giữ trống trong hồ sơ chính | ĐẠT |

## Điểm cần hiểu khi bảo vệ

- A2 CPS 4.472 đ và A4/B4 chi phí đều simulated; không suy ra mức tiết kiệm toàn công ty từ CPS/baseline.
- B3 theo quy ước chi phí của đề; 2 lượt rẻ nhất toàn mẫu. Phạm vi pilot 2 lượt được tính riêng 892/982 thành công, CPS 3.252 đ — simulated.
- B4 tính 15,3 phút cho CPS 12.414,7925 đ, làm tròn 12.415 đ — simulated; hướng dẫn ghi 12.414, sai khác nhỏ hơn dung sai 2%.
- Dùng 5.980 request thực tế mỗi nhánh và DE 6,96 để đạt 859 hiệu dụng; không lấy 859 làm số request cần thu.
- Tác động thật 5 điểm chỉ có power khoảng 0,642; pilot đề xuất chấp nhận mục tiêu 6 điểm.
- Bộ nhãn người dùng đã gửi khớp 20/20 tham khảo không đồng nghĩa hai người độc lập đồng thuận 100%.
- CSV và starter giữ nguyên byte so với lúc bắt đầu lượt này. Git đã báo starter có thay đổi trước lượt này; không tự hoàn nguyên phần người dùng.

## Chạy lại

Từ src: `.\.venv\Scripts\python.exe lab13.py --xuat-json` rồi `.\.venv\Scripts\python.exe kiem_tra_checkpoint.py`.
JSON được cập nhật theo code; nếu đổi giả định, phải cập nhật các báo cáo và chạy đối chiếu lại.
