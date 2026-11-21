# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

Nhóm: ProblemSolver; lớp L3A (suy từ tên thư mục, chờ xác nhận). Toàn bộ số liệu mẫu giả lập. Đề xuất chỉ áp dụng kế hoạch pilot nội địa + hàng nặng tại 12 depot khi có đủ 40 nhân viên trong danh sách vận hành.

| Mục | Con số chính | Trạng thái | Người phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí mỗi việc thành công | Toàn mẫu 4.472 đ; phạm vi 2 lượt 3.252 đ, 892/982 thành công; chưa gồm cố định — simulated | Giả lập | PM trợ lý hoàn phí |
| 2 · Ba yếu tố nhạy nhất | Làm lại +51,8%; xem lại +40,7%; lương +23,1% — simulated | Giả lập | PM trợ lý hoàn phí |
| 3 · So với nhân viên | Toàn mẫu 3 lượt: 5.865 đ/request theo B3 so 12.000 đ; A4 phạm vi 3 lượt + cố định 4.599/5.784 đ/việc ở hai khối lượng — simulated | Giả lập | Giám đốc vận hành |
| 4 · Chỉ số chính, dùng, an toàn | 82,83%; sửa/bỏ 27,12%; mở lại 4,25%; chưa có đối chứng nên chưa suy tác động | Xong, có bằng chứng | Trưởng nhóm CSKH |
| 5 · Bảng lỗi và khắc phục | 1 bộ người dùng cung cấp khớp 20/20 tham khảo; đủ 5 loại khắc phục; thiếu bộ nhãn thứ hai và bằng chứng độc lập | Chưa | Trưởng nhóm CSKH |
| 6 · Pilot plan | 20 + 20 nhân viên; 299 request/người = 5.980 thực tế/nhánh ≈859 hiệu dụng; MDE 6 điểm, power tại 5 điểm chỉ 0,642; 4 luật dừng | Xong, có bằng chứng | Giám đốc vận hành |
| 7 · Rủi ro kinh tế | Xem lại 100%: 11.743–12.415 đ/việc; giá trị thực phụ thuộc phút nhân viên và khối lượng — simulated | Giả lập | PM trợ lý hoàn phí |

Các điều kiện mở và tiếp tục pilot (lịch đề xuất, chưa xác nhận đã thực hiện):

- Kỹ sư trưởng agent sửa khóa chống trùng, đối soát sổ cái và bật 12 event; kiểm chứng ngày **2026-11-27**.
- Trưởng nhóm CSKH thu bộ nhãn thứ hai, xác nhận quy trình độc lập; nếu không chứng minh độc lập vì đã xem nhãn thì xin coach cách bổ sung; kiểm tra **2026-11-27**.
- Giám đốc vận hành xác nhận roster 40 người ở 12 depot và ký chấp nhận MDE 6 điểm cùng power 0,642 ở tác động 5 điểm; chốt **2026-11-27**.
- PM đo phút thật từ tuần đầu, theo dõi rủi ro B4; chỉ giảm xem lại khi qua ngưỡng an toàn; kiểm tra **2026-12-06**. Chưa đủ điều kiện thì giữ luồng thủ công.

**Đề xuất: Go có điều kiện** cho kế hoạch pilot nói trên; không tăng rollout hoặc kết luận có hiệu quả khi chưa đủ mẫu, chưa hết 7 ngày theo dõi hoặc chưa đáp ứng điều kiện.
