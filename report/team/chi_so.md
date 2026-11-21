# Đặc tả chỉ số, event và rủi ro kinh tế · Nhiệm vụ E1, E2

## E1 · Đặc tả chỉ số

| Loại | Chỉ số | Công thức | Tính thử trên 1.200 yêu cầu |
| --- | --- | --- | --- |
| Chính (kết quả) | % yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày | `dong_trong_24h` bằng 1 và `mo_lai_trong_7_ngay` bằng 0, chia tổng số yêu cầu | 82,83% (994/1.200) |
| Dùng | Tỉ lệ bỏ qua gợi ý | `quyet_dinh_xem_lai` là `sua` hoặc `bo`, chia số yêu cầu được xem lại | 27,12% (48/177) |
| An toàn | Tỉ lệ lỗi lọt đến khách | `mo_lai_trong_7_ngay` bằng 1, chia tổng số yêu cầu | 4,25% (51/1.200) |
| Dùng | Nhóm tự đề xuất: % yêu cầu của nhóm dùng trợ lý được mở bằng trợ lý | Số yêu cầu có `agent_suggestion_shown` chia số `refund_request_created` có arm = trợ lý | Không cần tính |
| An toàn | Nhóm tự đề xuất: % đơn hoàn sai tiền qua kiểm tra mẫu hằng tuần (bắt lỗi ngầm như ca 5, 17) | Số đơn trong `audit_sample_checked` có `so_tien_da_hoan` khác `so_tien_dung`, chia số đơn được kiểm tra | Không cần tính |

Chỉ số chính trong đợt chạy thử là 82,83%. Đợt chạy thử không có nhóm đối chứng, nên con số này chưa cho biết tác động của trợ lý; pilot sẽ trả lời phần đó.

## Danh sách event

| Event | Ai tạo | Thuộc tính chính | Thời điểm |
| --- | --- | --- | --- |
| `refund_request_created` | App khách | request_id, loai, so_tien, depot, staff_id, arm, trace_id | Khi khách gửi yêu cầu |
| `input_validation_failed` | Agent | request_id, reason (vd. ma_san_tmdt, sai_so_tai_khoan), trace_id | Khi đầu vào không hợp lệ |
| `agent_run_completed` | Agent | attempt, tokens_in, tokens_out, tool_calls, status, trace_id | Sau mỗi lần chạy, kể cả lần lỗi |
| `agent_suggestion_shown` | Giao diện nhân viên | staff_id, so_tien_de_xuat, trace_id | Khi gợi ý hiện cho nhân viên |
| `staff_review_decision` | Nhân viên | quyết định giu / sua / bo, phut_xem_lai (đo thật), trace_id | Khi nhân viên bấm gửi, sửa hoặc bỏ |
| `staff_rework_completed` | Nhân viên | phut_lam_lai, ly_do, trace_id | Khi nhân viên làm lại xong |
| `refund_ledger_write` | Dịch vụ sổ cái | idempotency_key, so_tien, ket_qua, trace_id | Khi ghi sổ hoàn tiền |
| `handoff_to_staff` | Agent | reason (vd. thieu_du_lieu, ngoai_pham_vi), tom_tat, trace_id | Khi chuyển cho nhân viên |
| `ticket_closed` | Hệ thống ticket | closed_at, trace_id | Khi yêu cầu được đóng |
| `ticket_reopened` | Khách | reopened_at, reason, trace_id | Khi khách mở lại |
| `audit_sample_checked` | Kế toán | so_tien_da_hoan, so_tien_dung, phien_ban_bang_gia, trace_id | Hằng tuần, kiểm tra mẫu 100 đơn |

**Kiểm tra chéo:** với mỗi chỉ số ở bảng E1, ghi event dùng để tính. Chỉ số nào không tính được từ danh sách event thì chưa đo được.

- Chính: `refund_request_created` (thời điểm tạo) + `ticket_closed` (đóng trong 24 giờ) + `ticket_reopened` (không mở lại trong 7 ngày).
- Dùng, tỉ lệ bỏ qua gợi ý: `staff_review_decision` (sua + bo chia tổng số quyết định).
- An toàn, lỗi lọt đến khách: `ticket_reopened` chia `refund_request_created`.
- Dùng, tự đề xuất: `agent_suggestion_shown` chia `refund_request_created` có arm = trợ lý.
- An toàn, tự đề xuất: `audit_sample_checked`.
- Chi phí mỗi việc thành công (luật dừng chi phí): `agent_run_completed` (token, tool) + `staff_review_decision` (phút xem lại) + `staff_rework_completed` (phút làm lại); thay số phút simulated bằng phút đo thật.

## E2 · Rủi ro kinh tế

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Người phụ trách |
| --- | --- | --- | --- | --- |
| Số ca làm lại tăng gấp đôi | +51,8%, lên 6.787 đ mỗi việc thành công [simulated] (B1) | Tỉ lệ làm lại theo tuần vượt 7% (đợt chạy thử: 4,9% trong phạm vi noi_dia + hang_nang) | Thu hẹp về noi_dia, rà 20 trace làm lại gần nhất | PM trợ lý hoàn phí |
| Phải xem lại 100% kéo dài | 11.743 đ = 0,98× hoặc 12.415 đ = 1,03× khi dùng thời gian làm lại trung bình trong dữ liệu [simulated] (B4) | % yêu cầu được xem lại còn trên 50% ở cuối bước rollout 0.25 | Giảm xem lại theo bậc khi tỉ lệ sửa + bỏ dưới 15% | Trưởng nhóm CSKH |
| Khối lượng thấp hơn dự kiến | Nếu phân bổ đủ 40 triệu đ/tháng, bước 4 người ở 10% khối lượng chỉ có khoảng 3.375 việc thành công/tháng. Chi phí cố định khoảng 11.852 đ/việc, cộng 3.414 đ biến đổi thành khoảng 15.266 đ/việc [simulated] (A4) | Số việc thành công theo tuần dưới 50% kế hoạch | Xem lại hợp đồng và hoãn mở rộng. Theo dõi chi phí toàn phần riêng. Ngưỡng dừng 8.000 đ của D3 chỉ tính chi phí biến đổi. | PM trợ lý hoàn phí |
