# Đặc tả chỉ số, event và rủi ro kinh tế · Nhiệm vụ E

Nguồn số: `src/lab13.py --xuat-json` và `ket_qua_tinh_toan.json`. Toàn bộ dữ liệu là mẫu giả lập; các event dưới đây là đặc tả đề xuất, chưa được triển khai trong repo phân tích.

## E1 · Chỉ số

| Loại | Chỉ số | Công thức | Tính thử |
| --- | --- | --- | --- |
| Chính | Đóng trong 24 giờ, không mở lại 7 ngày | Số request thỏa hai điều kiện / tổng request | 994/1.200 = 82,83% |
| Dùng | Sửa hoặc bỏ gợi ý | Số request được xem lại có quyết định sua/bo / số request được xem lại | 48/177 = 27,12% |
| An toàn | Mở lại trong 7 ngày; chỉ số đại diện lỗi lọt theo lab | Số request mở lại / tổng request | 51/1.200 = 4,25% |
| Dùng bổ sung | Tỷ lệ mở trợ lý trên yêu cầu đủ điều kiện | Số request đủ điều kiện ở nhánh AI có suggestion_shown / tổng request đủ điều kiện nhánh AI | Chưa tính: CSV chưa có event hiển thị và arm |
| An toàn bổ sung | Tỷ lệ hoàn sai tiền qua audit | Số đơn sai tiền / số đơn được lấy mẫu kiểm tra | Chưa tính: cần audit và số tiền chuẩn |

Chỉ số trong mẫu chạy thử là **82,83%**; không kết luận trợ lý tạo ra cải thiện vì chưa có đối chứng đồng thời. Chỉ số chính có **994** ca, còn ket_qua thành công có **978** ca: định nghĩa thành công còn yêu cầu không sai tiền.

Tỷ lệ mở lại chỉ đại diện cho an toàn, không chứng minh mọi ca mở lại đều do AI sai và không bắt được hết lỗi ngầm. Chỉ số 7 ngày chỉ chốt khi cohort đã đủ thời gian theo dõi.

## Danh sách event

Mỗi event có `event_id`, `occurred_at`, `request_id`, `trace_id`; event trùng được loại theo event_id. Liên kết mọi run của một request bằng request_id; không đếm số run thành số request.

| Event | Ai tạo | Thuộc tính chính, ngoài các trường chung | Thời điểm |
| --- | --- | --- | --- |
| refund_request_created | Hệ thống ticket | trace_id, created_at, loai, staff_id, depot, arm, eligible, policy_version | Khi tiếp nhận |
| agent_run_completed | Agent | trace_id, run_id, attempt, tokens_in, tokens_out, tool_calls, status | Sau mỗi run, cả lỗi |
| agent_suggestion_shown | Giao diện nhân viên | trace_id, staff_id, arm, suggestion_id | Khi hiển thị |
| staff_review_decision | Giao diện nhân viên | trace_id, suggestion_id, decision=giu/sua/bo, review_minutes | Khi chốt xem lại |
| staff_rework_completed | Giao diện nhân viên | trace_id, rework_minutes, reason | Khi hoàn tất làm lại |
| refund_ledger_write | Sổ cái | trace_id, idempotency_key, amount, currency, result | Khi ghi giao dịch |
| customer_refund_notified | Dịch vụ thông báo | trace_id, message_status, ledger_transaction_id | Khi báo khách kết quả |
| handoff_to_staff | Agent | trace_id, reason, staff_id, summary | Khi chuyển nhân viên |
| input_validation_failed | Giao diện tiếp nhận | trace_id, field, error_type, input_code_type | Khi kiểm tra đầu vào lỗi |
| ticket_closed | Hệ thống ticket | trace_id, closed_at, reason | Khi đóng yêu cầu |
| ticket_reopened | Hệ thống ticket | trace_id, reopened_at, reason | Khi mở lại |
| audit_sample_checked | Kế toán | trace_id, sampled_at, paid_amount, correct_amount, policy_version, discrepancy | Khi kiểm tra mẫu |

## Kiểm tra chỉ số với event

- Chính: refund_request_created + ticket_closed + ticket_reopened; 24 giờ tính từ created_at, theo dõi mở lại trong 7 ngày kể từ đóng. Kiểm tra audit sai tiền riêng, không tự đổi định nghĩa chỉ số chính.
- Sửa/bỏ: staff_review_decision; một quyết định cuối mỗi request được xem lại. Mẫu số không phải toàn bộ request.
- Mở lại: refund_request_created + ticket_closed + ticket_reopened, chỉ tính các request đã đủ cửa sổ 7 ngày.
- Tỷ lệ mở trợ lý: eligible và arm của refund_request_created nối agent_suggestion_shown; mỗi request tính một lần.
- Hoàn sai tiền: audit_sample_checked; tách số đơn có discrepancy khỏi số đơn được lấy mẫu.
- CPS và lỗi C: agent_run_completed + review/rework + handoff + ledger + notification + audit, nối request_id/trace_id; review_minutes và rework_minutes thay cột simulated khi đo thật.

## E2 · Rủi ro kinh tế

Mọi tác động chi phí bên dưới có nhãn **simulated**; ngưỡng hành động là đề xuất viết trước.

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Người phụ trách |
| --- | --- | --- | --- | --- |
| Làm lại tăng gấp đôi | CPS 4.472 → 6.787 đ, +51,8% — simulated | Làm lại >7% request/tuần trong phạm vi; mẫu hiện tại 4,89% | Rà 20 trace làm lại, thu hẹp về nội địa trước khi tăng rollout | PM trợ lý hoàn phí |
| Xem lại gấp đôi | CPS 4.472 → 6.292 đ, +40,7% — simulated | Giờ xem lại/100 request và tỷ lệ được xem lại tăng liên tiếp 2 tuần | Đo thời gian thật, sửa giao diện và huấn luyện nhân viên; không bỏ kiểm soát an toàn | Trưởng nhóm CSKH |
| Xem lại 100% kéo dài | B4: 11.743 hoặc 12.415 đ/việc — simulated | Cuối bước 25% còn >50% request được xem lại hoặc phút xem lại >5 | Chỉ giảm xem lại 100% → 50% → 25% khi audit 100 đơn/tuần không sai tiền và an toàn không vượt ngưỡng | Giám đốc vận hành |
| Khối lượng giảm một nửa | Cố định/việc 1.185 → 2.370 đ theo A4 — simulated | Số thành công/tuần <50% kế hoạch trong 2 tuần | Đánh giá lại quy mô và 40 triệu/tháng chi phí cố định | PM trợ lý hoàn phí |
