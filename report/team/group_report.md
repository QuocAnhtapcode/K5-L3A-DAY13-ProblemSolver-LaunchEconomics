# Báo cáo nhóm ProblemSolver

## 1. Thông tin nhóm

- Tên nhóm: ProblemSolver
- Lớp: L3A · Khóa K5
- Thành viên và phân công: [TEAM.md](../../TEAM.md)

## 2. Mục tiêu và cách tiếp cận

Đánh giá liệu trợ lý hoàn phí LogiX-VN có đáng thử trong pilot Gate 2a. Hồ sơ dùng 1.200 yêu cầu và 1.624 lần chạy để tính chi phí, phân loại lỗi, xác định chỉ số và thiết kế nhóm đối chứng.

## 3. Giải pháp

- **A** Cộng tiền máy của mọi lần chạy và giờ nhân viên, rồi chia cho số việc thành công. Đối chiếu với 12.000 đ khi nhân viên tự làm. [Bảng chi phí](bang_chi_phi.md)
- **B** Chạy 9 kịch bản đổi từng yếu tố. So giới hạn 1–3 lần chạy theo chi phí cả hệ thống và kiểm tra kịch bản xem lại 100%. [Bảng độ nhạy](bang_chi_phi.md)
- **C** Phân loại 20 ca theo năm nguyên nhân gốc. Bảng có 5 cách khắc phục, kèm tín hiệu phát hiện và người phụ trách. [Bảng lỗi](bang_loi.md)
- **D** Chia ngẫu nhiên theo nhân viên, phân tầng theo depot. Ghi trước chỉ số chính và các luật dừng. Ngưỡng chênh lệch mở lại 2 điểm áp dụng từ bước 10 người. Ngưỡng chi phí 8.000 đ chỉ tính phần biến đổi. [Kế hoạch pilot](pilot_plan.yaml)
- **E** Tính thử 3 chỉ số, đặc tả 11 event có `trace_id` và tổng hợp rủi ro kinh tế. [Chỉ số](chi_so.md) · [Hồ sơ launch v0](ho_so_launch_v0.md)

## 4. Kết quả

- **Chi phí** 4.472 đ/việc thành công trên toàn mẫu [simulated]. Trong phạm vi pilot, chi phí cộng khoản cố định là 4.599 đ/việc thành công ở quy mô 45.000 yêu cầu/tháng [simulated]. Xem lại 100% đưa chi phí lên 0,98–1,03 lần mức nhân viên tự làm [simulated].
- **Chỉ số chạy thử** 82,83% yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày. Tỉ lệ bỏ qua hoặc sửa gợi ý là 27,12%, tỉ lệ mở lại trong 7 ngày là 4,25%.
- **Đề xuất** Go có điều kiện cho `noi_dia` và `hang_nang`. Pilot chia 20 nhân viên mỗi nhóm, với ít nhất 299 yêu cầu mỗi nhân viên để phát hiện chênh lệch 6 điểm phần trăm theo các giả định của D1.
- **Duyệt chéo** Chưa có kết quả hội đồng trong repo. Phiếu [ProblemSolver chấm nhóm khác](phieu_cham.md) điền theo buổi duyệt chéo.

## 5. Khó khăn và cách xử lý

- Lần chạy đầu trên máy hiện tại dừng ở D1 với lỗi `ModuleNotFoundError: No module named 'statsmodels'`. Sau khi bổ sung thư viện vào thư mục tạm, chạy lại `python -B lab13.py` trong `src/` thành công đến E1 và A1 báo ĐẠT. Vinh bổ sung log chạy trên máy thứ hai.
- Hồ sơ B4 đã đồng bộ theo đầu ra 12.415 đ/việc thành công [simulated] khi dùng số phút làm lại trung bình chưa làm tròn.
- Bảng C hiện ghi 20/20 ca trùng. Hưng và Bình cần đối chiếu hai cột với bộ nhãn gốc trước khi chốt CP3.

## 6. Tổng hợp đóng góp

| Thành viên | Phần việc phụ trách |
| --- | --- |
| Đỗ Thị Thanh Bình | Trưởng nhóm, code A–E và bộ nhãn 2 ở C |
| Hoàng Quốc Anh | Kiểm tra và trình bày phần D |
| Lê Gia Hưng | Bộ nhãn 1 ở C, điều kiện “Xong khi” và checklist nộp |
| Hà Quang Vinh | Chạy kiểm tra trên máy thứ hai, kiểm số, giữ hồ sơ và tổng hợp báo cáo |

Các phần việc và báo cáo cá nhân được liên kết trong [TEAM.md](../../TEAM.md).

## 7. Hạn chế và hướng cải thiện

Chi phí nhân công dựa trên số phút `simulated` và cần được thay bằng số đo trong pilot. Đợt chạy thử chưa có nhóm đối chứng để ước lượng tác động. Nếu tác động thật là 5 điểm phần trăm, kế hoạch hiện có power khoảng 0,64.

## 8. Tài liệu tham khảo

- [Dữ liệu và công thức Lab 13](../../docs/du_lieu_va_cong_thuc.md)
- [Hướng dẫn chi tiết buổi chiều](../../docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md)
- [Đề bài học viên và 20 ca lỗi](../../docs/Ngay13_Lab13_De_bai_hoc_vien.docx)
- [Slide D1 về cách chia nhóm, luật dừng và chi phí cố định](../../slide-d1-ba-cach-chia.html)
