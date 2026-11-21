# Bảng chi phí · Nhiệm vụ A và B

Nguồn số: `src/lab13.py --xuat-json`, bảng chưa làm tròn trong `ket_qua_tinh_toan.json`. Toàn bộ CSV và bảng giá đều giả lập. Mọi CPS, tổng có giờ nhân viên, tỷ trọng và thay đổi chi phí dưới đây mang nhãn **simulated**; riêng token/tool đo từ trace giả lập. CPS chưa cộng cố định, trừ A4. Mỗi câu trả lời tách thành đoạn không quá ba dòng.

## A1 · Ba phép thử đáp án biết trước

| Phép thử (p = 0,8) | Kết quả |
| --- | --- |
| Số lần chạy trung bình, tối đa 2 lần | 1,20 |
| Số lần chạy trung bình, chạy đến khi đúng | 1,25 |
| Hệ số chi phí mỗi việc thành công, tối đa 3 lần | 1,25 |

Cả 3 phép thử ĐẠT. Công thức lý thuyết giả định các lần thử độc lập với xác suất đúng không đổi; cần kiểm tra lại bằng trace khi lỗi lặp trên cùng yêu cầu.

## A2 · Mô hình chi phí từ trace

| Khoản | Số tiền (đ), trừ dòng số việc | Nguồn | Nhãn |
| --- | --- | --- | --- |
| Token | 245.585 | tokens_in/out × giá / 1.000 | đo từ trace giả lập |
| Tool | 84.000 | tool_calls × 15 | đo từ trace giả lập |
| Trong đó, lần chạy thứ 2 và 3 | 93.804 | attempt > 1; đã nằm trong token + tool | đo từ trace giả lập |
| Xem lại | 1.780.000 | 890 phút × 2.000 | simulated |
| Làm lại | 2.264.000 | 1.132 phút × 2.000 | simulated |
| Tổng | 4.373.585 | token + tool + xem lại + làm lại | simulated |
| Số việc thành công | 978 | ket_qua == thanh_cong | đếm từ mẫu giả lập |
| Chi phí mỗi việc thành công | 4.472 | tổng / 978 | simulated |
| Hóa đơn token + tool / số yêu cầu | 274,65 | (token + tool) / 1.200 | đo từ trace giả lập |

CPS gấp **16,3 lần** hóa đơn token/tool chia số yêu cầu — simulated; nhân viên xem lại/làm lại là phần chi phí chính.

Làm lại chiếm **51,8%**, tổng giờ nhân viên chiếm **92,5%** chi phí — simulated.

Tử số tính mọi run, gồm run lỗi; mẫu số chỉ tính **978** request thành công. Khoản chạy lại **93.804 đ** là phần đã có trong token/tool, không cộng lần hai.

So sánh cùng đơn vị theo quy ước B3: (4.373.585 + 222 × 12.000) / 1.200 = **5.865 đ/yêu cầu**, khoảng **0,49×** thủ công — simulated, chưa gồm cố định.

## A3 · Tách theo loại yêu cầu

Hai cột CPS và so với 12.000 đ: **simulated**. Tỷ lệ CPS/baseline là phép đối chiếu A3; chưa cộng nhân viên làm thay và cố định.

| Loại | Số yêu cầu | Tỷ lệ thành công | Lần chạy/yêu cầu | CPS (đ), simulated | CPS/12.000, simulated |
| --- | --- | --- | --- | --- | --- |
| noi_dia | 824 | 95,0% | 1,11 | 2.696 | 0,22× |
| hang_nang | 158 | 74,1% | 1,47 | 8.221 | 0,69× |
| quoc_te | 150 | 27,3% | 2,32 | 22.515 | 1,88× |
| doi_tac | 68 | 54,4% | 1,88 | 10.215 | 0,85× |

Quốc tế chưa phù hợp: **22.515 đ/việc**, thành công **27,3%** — simulated đối với chi phí. Tỷ lệ run ok lần 1/2/3 là **30,0% / 11,4% / 2,2%**: lượt thứ ba chỉ bổ sung rất ít.

Pilot chọn **nội địa + hàng nặng**; tạm loại quốc tế và đối tác. Đối tác có CPS **10.215 đ — simulated**, thành công **54,4%** và điều khoản riêng, cần rà chính sách trước.

## A4 · Chi phí cố định, nội địa + hàng nặng

Phạm vi có **982** yêu cầu, **900** thành công, CPS biến đổi **3.414 đ — simulated**. 45.000 là tổng yêu cầu toàn công ty; giữ cơ cấu loại của mẫu: thành công thuộc phạm vi/tháng = khối lượng × 900/1.200.

| Tổng yêu cầu/tháng | Việc thành công thuộc phạm vi/tháng | Cố định/việc (đ) | CPS + cố định (đ), simulated | So 12.000, simulated |
| --- | --- | --- | --- | --- |
| 45.000 | 33.750 | 1.185 | 4.599 | 0,38× |
| 22.500 | 16.875 | 2.370 | 5.784 | 0,48× |

Giảm một nửa khối lượng làm cố định/việc tăng từ **1.185 lên 2.370 đ**; CPS cộng cố định tăng **4.599 lên 5.784 đ — simulated**, vẫn dưới 12.000 đ theo phép đối chiếu A4.

A4 dùng trace tối đa 3 lần và chưa cộng xử lý thủ công phần còn lại; không dùng riêng tỷ lệ **0,38×** để khẳng định mức tiết kiệm toàn công ty.

## B1 · Đổi từng yếu tố

Mọi CPS và thay đổi dưới đây: **simulated**; baseline CPS chưa làm tròn **4.471,9684 đ**. Hệ số xem lại/làm lại chỉ thay khoản chi phí, chưa mô phỏng thay đổi chất lượng.

| Kịch bản | Tham số của mo_hinh | CPS (đ), simulated | Thay đổi, simulated |
| --- | --- | --- | --- |
| Giá token gấp đôi | gia_vao=52, gia_ra=260 | 4.723 | +5,6% |
| Giá token giảm nửa | gia_vao=13, gia_ra=65 | 4.346 | -2,8% |
| Xem lại gấp đôi | he_so_xem_lai=2 | 6.292 | +40,7% |
| Xem lại giảm nửa | he_so_xem_lai=0.5 | 3.562 | -20,3% |
| Làm lại gấp đôi | he_so_lam_lai=2 | 6.787 | +51,8% |
| Làm lại giảm nửa | he_so_lam_lai=0.5 | 3.315 | -25,9% |
| Lương tăng 25% | luong_phut=2500 | 5.506 | +23,1% |
| Tối đa 2 lần | max_lan_chay=2 | 4.237 | -5,2% |
| Tối đa 1 lần | max_lan_chay=1 | 4.111 | -8,1% |

Giới hạn lượt chạy theo quy ước đề: bỏ run vượt giới hạn; yêu cầu cần thêm lượt chuyển nhân viên, phút xem lại/làm lại của các yêu cầu đó về 0.

## B2 · Đổi một cặp và xếp hạng

Token và xem lại cùng gấp đôi: **6.543 đ**, tăng **46,3% — simulated**. Mẫu số giữ nguyên nên hai phần tăng cộng lại: **5,6% + 40,7% = 46,3%**.

Với biên độ kịch bản B1, xếp hạng **1. làm lại (+51,8%); 2. xem lại (+40,7%); 3. lương (+23,1%) — simulated**. Đây là xếp hạng các kịch bản đã cho, không phải độ co giãn chuẩn hóa.

## B3 · Giới hạn chạy lại có thật sự rẻ hơn

Các cột chi phí: **simulated**. Theo quy ước B3: cả hệ thống = tổng trợ lý + 12.000 × số không thành công; đây là giả định so sánh của lab, chưa gồm cố định.

| Giới hạn | Tổng trợ lý (đ), simulated | Không thành công | Cả hệ thống (đ), simulated | CPS (đ), simulated |
| --- | --- | --- | --- | --- |
| 1 | 3.621.781 | 319 | 7.449.781 | 4.111 |
| 2 | 4.093.220 | 234 | 6.901.220 | 4.237 |
| 3 | 4.373.585 | 222 | 7.037.585 | 4.472 |

**2 lần** rẻ nhất cho công ty (**6.901.220 đ — simulated**); **1 lần** có CPS thấp nhất (**4.111 đ — simulated**) nhưng đẩy thêm **85** yêu cầu sang nhân viên so với 2 lần.

## B4 · Nếu phải xem lại tất cả

Chỉ lấy nội địa + hàng nặng: **948** request có ít nhất một run ok, xem lại **5 phút/request**; **48** ca làm lại; **900** thành công. Token/tool **224.513 đ**; thay toàn bộ hai khoản giờ nhân viên, không cộng vào tổng cũ.

| Phút làm lại/ca, simulated | Request ok | Ca làm lại | Tổng (đ), simulated | CPS (đ), simulated | CPS/12.000, simulated | Phút xem lại hòa vốn, simulated |
| --- | --- | --- | --- | --- | --- | --- |
| 9,0 | 948 | 48 | 10.568.513 | 11.743 | 0,98× | 5,12 |
| 15,3 | 948 | 48 | 11.173.313 | 12.415 | 1,03× | 4,80 |

Với 9 phút làm lại, CPS **11.743 đ ≈ 0,98×** thủ công; với **15,3 phút**, CPS **12.415 đ ≈ 1,03× — simulated**. Trung bình cột làm lại trên toàn bộ ca sai là **15,2973 phút — simulated**.

Pilot phải đo phút thật và tỷ lệ xem lại an toàn; thời gian xem lại hòa vốn khoảng **5,12** hoặc **4,80 phút — simulated**, tùy giả định phút làm lại.

Số 12.415 đ là làm tròn từ **12.414,7925**; hướng dẫn ghi 12.414 đ, chênh dưới 0,01%, trong dung sai 2%.

## Phạm vi pilot và tối đa hai lượt chạy

Không suy kết quả toàn mẫu B3 sang phạm vi mới: tính lại nội địa + hàng nặng, tối đa 2 lượt được **892/982** thành công, CPS **3.252 đ — simulated**, chưa gồm cố định hay xử lý thủ công.

Đây là số mô phỏng cắt trace theo quy ước lab; chất lượng và phút nhân viên phải đo lại trong pilot.
