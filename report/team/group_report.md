# Báo cáo nhóm

## 1. Thông tin nhóm

ProblemSolver, L3A: suy từ tên thư mục, chờ xác nhận. Họ tên, MSSV và đóng góp cá nhân chưa được cung cấp; xem `TEAM.md`.

## 2. Mục tiêu và cách tiếp cận

Đánh giá chi phí, lỗi, mức sử dụng và thiết kế pilot trợ lý hoàn phí LogiX-VN. Dùng **1.200 request, 1.624 run**, tính lại bằng `src/lab13.py`, giữ nguyên CSV trong lượt hoàn thiện này; mọi chi phí có thời gian nhân viên ghi simulated.

## 3. Giải pháp

A: cộng mọi run và giờ nhân viên, chia số thành công; phân loại và cộng cố định. B: 9 kịch bản, một cặp, giới hạn retry và xem lại 100%; xem `bang_chi_phi.md`. C: ghi bộ nhãn người dùng cung cấp, đối chiếu và đề xuất 5 cách khắc phục trong `bang_loi.md`; còn thiếu bộ thứ hai. D: công thức so hai tỷ lệ, DE và cỡ mẫu hiệu dụng; xem `pilot_plan.yaml`. E: 3 chỉ số và 12 event, rủi ro trong `chi_so.md`; kết luận trong `ho_so_launch_v0.md`.

## 4. Kết quả

CPS **4.472 đ — simulated**, nhân viên chiếm **92,5% — simulated**. B3 chọn tối đa **2** lượt, cả hệ thống **6.901.220 đ — simulated**. B4 xem lại 100% lên **11.743–12.415 đ — simulated**. Chỉ số trong mẫu: **82,83% / 27,12% / 4,25%**, chưa suy ra tác động AI. Pilot 20 nhân viên mỗi nhánh, 5.980 request thực tế/nhánh, MDE 6 điểm; power chỉ **0,642** nếu tác động 5 điểm. Đề xuất **Go có điều kiện**. Kết quả duyệt chéo: **Chưa có**, chưa tự cho điểm hội đồng.

## 5. Khó khăn và cách xử lý

Lỗi đã xuất hiện trong cuộc trò chuyện: `NotImplementedError: VIẾT Ở ĐÂY` khi gọi so_lan_chay_ky_vong; xử lý bằng công thức A1/A2. Sắp lại A4 trước B, đưa phép nối bảng ra ngoài vòng loại và bổ sung D/E. Phân biệt 859 hiệu dụng với 5.980 thực tế; làm tròn B4 từ 12.414,7925 thành 12.415 đ — simulated, lệch nhỏ so tài liệu. Thiếu bằng chứng nhãn độc lập, roster, danh tính và duyệt chéo được ghi Chưa.

## 6. Tổng hợp đóng góp

Người dùng cung cấp một bộ nhãn 20 ca trong cuộc trò chuyện. Codex hỗ trợ code, tính toán, đối chiếu và soạn báo cáo; chưa xác nhận đóng góp từng thành viên. Thành viên cần tự rà và bổ sung bằng chứng thực tế trong `TEAM.md` và báo cáo cá nhân.

## 7. Hạn chế và hướng cải thiện

CSV là giả lập, chỉ có **6 depot và 20 staff** trong mẫu, không phải roster 12 depot/40 staff toàn công ty. Hai nhóm chưa tồn tại trong dữ liệu chạy thử nên chưa chứng minh nhân quả. ICC **0,02** và baseline **0,70** là giả định D1, cần đo lại trong pilot. Giữ đủ mẫu và cửa sổ 7 ngày; chưa đủ thì kết luận chưa đủ bằng chứng.

## 8. Tài liệu tham khảo

`docs/du_lieu_va_cong_thuc.md`; `docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md`; đề bài Word trong docs; `CHECKPOINTS.md`, `RUBRIC.md`, `RULES.md`, `SUBMISSION.md`. AI đã dùng: Codex để sửa code và soạn thảo; tự kiểm tra bằng ba phép thử A1, đối chiếu CSV, YAML và `kiem_tra_checkpoint.py`.
