# Báo cáo cá nhân — Đỗ Thị Thanh Bình

## 1. Thông tin thành viên

- Họ tên: Đỗ Thị Thanh Bình
- MSSV: 2A202603709
- Email: dtb1232005@gmail.com
- GitHub: ecaep7
- Vai trong nhóm: Trưởng nhóm, người viết code A–E, người gắn nhãn 2 ở C.

## 2. Phần việc phụ trách

Tôi điều phối các checkpoint. Tôi viết code mô hình chi phí, phân tích độ nhạy, tính cỡ mẫu D1 và đặc tả ba chỉ số E1.

Ở CP3, tôi gắn độc lập 20 ca lỗi và chỉ so với bộ nhãn của Hưng sau khi hai bộ nhãn đã chốt.

## 3. Đóng góp cụ thể

Phần mã nguồn tôi thực hiện gồm ba phép thử A1, mô hình A2–A4, các kịch bản B1–B4, cỡ mẫu D1 và chỉ số E1.

Tôi xác nhận bộ nhãn số 2 ở phần C và ghi lại cách xử lý bất đồng nếu có.

## 4. Bằng chứng

- [Mã nguồn](../../src/lab13.py) và [bảng chi phí](bang_chi_phi.md). Ba kết quả A1 là 1,20 · 1,25 · 1,25.
- [Bảng lỗi](bang_loi.md). [Cần bổ sung: bộ nhãn gốc của tôi, lưu trước khi so nhãn.]

## 5. Công cụ AI đã dùng

Tôi dùng Claude Code (trong VS Code) để điền các bảng `bang_chi_phi.md`, `bang_loi.md`, `pilot_plan.yaml` và `chi_so.md` từ nội dung nhóm đã soạn.

Tôi tự kiểm tra bằng cách chạy lại `src/lab13.py` và tính lại từ `logix_requests.csv`, `logix_runs.csv`: bảng A3, A4, các kịch bản B1–B3 và chi phí xem lại 100% ở B4; cỡ mẫu và tỉ lệ mở lại ở D1; tỉ lệ ở E1 (82,83%, 27,12%, 4,25%). Các số đều khớp.

Những chỗ không kiểm được từ dữ liệu, tôi giữ nguyên là giả định của nhóm: 5 phút xem lại và 9 phút làm lại ở B4, các ngưỡng trong luật dừng, ngày quyết định.

## 6. Tự đánh giá

Các con số A–E đều truy ngược được về `lab13.py` và hai file CSV.

Khi kiểm lại, tôi thấy hai chỗ cần giải thích khi bảo vệ: cỡ mẫu 1.251 trong `pilot_plan.yaml` so với 1.250 khi chạy `statsmodels` (và 859 so với 858), và nguồn của hai giả định 5 phút, 9 phút ở B4.
