# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

Một trang. Cột trạng thái chỉ nhận: **Xong, có bằng chứng · Chưa · Giả lập**. Mục nào dựa trên cột `_simulated` ghi Giả lập. Người phụ trách là một vai trò, không ghi "cả đội". Gate 2a chỉ duyệt kế hoạch pilot: không viết như thể trợ lý đã được duyệt chạy chính thức (xem quy tắc 5 trong `README.md`).

Nhóm: ProblemSolver · Lớp: L3A

| Mục | Con số chính | Trạng thái | Người phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí mỗi việc thành công | 4.472 đ trên toàn mẫu, gấp 16,3 lần hoá đơn token chia số yêu cầu (274,7 đ); trong phạm vi noi_dia + hang_nang 3.414 đ, cộng cố định 40 triệu/tháng thành 4.599 đ [simulated] | Giả lập | PM trợ lý hoàn phí |
| 2 · Ba yếu tố nhạy nhất | Số ca làm lại +51,8% · tỉ lệ xem lại +40,7% · lương nhân viên +23,1%; giá token gấp đôi chỉ +5,6% [simulated] | Giả lập | PM trợ lý hoàn phí |
| 3 · So với nhân viên tự làm (12.000 đ) | noi_dia 0,22× · hang_nang 0,69× · doi_tac 0,85× · quoc_te 1,88×. Phạm vi pilot cộng cố định 0,38× và khi xem lại 100% là 0,98–1,03×. Toàn mẫu tính cả ca nhân viên làm thay là 0,49× [simulated]. | Giả lập | Giám đốc vận hành LogiX-VN |
| 4 · Chỉ số chính, chỉ số dùng, chỉ số an toàn | Chính 82,83% trong đợt chạy thử (chưa có đối chứng) · bỏ qua gợi ý 27,12% · mở lại 7 ngày 4,25%; 11 event có trace_id | Xong, có bằng chứng | PM trợ lý hoàn phí |
| 5 · Bảng lỗi và cách khắc phục | Bảng hiện có ghi 20/20 ca trùng, chờ xác nhận 2 bộ nhãn gốc. Có 5 cách khắc phục với tín hiệu phát hiện và người phụ trách. Ca 7 và 20 phải xử lý trước pilot. | Chưa | Kỹ sư trưởng agent |
| 6 · Pilot plan | Chia ngẫu nhiên theo nhân viên và phân tầng theo depot (20 + 20). MDE 6 điểm cần ≥ 299 yêu cầu mỗi người. Thu khoảng 10 ngày trong phạm vi pilot và chờ đủ 7 ngày theo dõi từng ca. Power 0,64 nếu tác động thật 5 điểm. Dự kiến quyết định 2027-01-05 khi đủ dữ liệu. | Xong, có bằng chứng | Giám đốc vận hành LogiX-VN |
| 7 · Rủi ro kinh tế | Làm lại gấp đôi → 6.787 đ (+51,8%); xem lại 100% kéo dài → 0,98–1,03×; khối lượng còn một nửa → cố định +2.370 đ/việc [simulated] | Giả lập | PM trợ lý hoàn phí |

Điều kiện trước và trong pilot dự kiến bắt đầu 2026-12-01:

- Xác nhận 2 bộ nhãn độc lập CP3 với Hưng và Bình trước khi chốt hồ sơ nhóm.
- Sửa khoá chống trùng và đối soát sổ cái (ca 7, 20) trước ngày bắt đầu · Kỹ sư trưởng agent · kiểm tra 2026-11-30.
- Ký chấp nhận mức chênh phát hiện được 6 điểm (power 0,64 nếu tác động thật chỉ 5 điểm) · Giám đốc vận hành LogiX-VN · kiểm tra 2026-11-30.
- Bật đủ 11 event có trace_id; thay số phút simulated bằng phút đo thật sau tuần 1 · PM trợ lý hoàn phí · kiểm tra 2026-12-08.
- Giảm xem lại theo bậc khi tỉ lệ sửa + bỏ dưới 15%, vì xem lại 100% không tiết kiệm (0,98–1,03× [simulated]) · Trưởng nhóm CSKH · kiểm tra 2026-12-14, cuối bước rollout 0.25.

**Đề xuất: Go có điều kiện** cho pilot chỉ gồm noi_dia và hang_nang (loại quoc_te 1,88× và doi_tac 0,85× [simulated]).
