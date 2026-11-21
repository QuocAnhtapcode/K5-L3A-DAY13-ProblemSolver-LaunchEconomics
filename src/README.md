# Source code

Code phân tích và dữ liệu giả lập của Lab 13. Các lệnh dưới đây chạy trong `src/`; code cũng hỗ trợ chạy từ root vì đường dẫn CSV được tính theo vị trí `lab13.py`.

- File bắt đầu chạy: `lab13.py` (đã hoàn thiện A, B, D1, E1; cũng là file nộp). `lab13_starter.py` được giữ nguyên so với trước lượt hoàn thiện, để đối chiếu; không sửa thêm.
- Cách chạy: `python3 lab13.py`.
- Input: `logix_runs.csv`, `logix_requests.csv` cùng thư mục, file yêu cầu đọc bằng `pd.read_csv('logix_requests.csv', keep_default_na=False)`.
- Output: in ra stdout ba phép thử A1, A2–A4, B1–B4, D1 và E1. Các báo cáo trong `report/team/` đã được điền từ kết quả tính; mọi chi phí có thời gian nhân viên ghi simulated.
- File học viên được sửa: `lab13.py`. Không sửa hai file CSV.

## Cài đặt

Cần Python 3.10 trở lên. Lab không cần khoá API và không cần mạng trong lúc làm.

macOS / Linux:

```bash
cd src
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -c "import pandas, numpy, scipy, statsmodels; print('san sang')"
python lab13.py
```

Windows PowerShell:

```powershell
cd src
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -c "import pandas, numpy, scipy, statsmodels; print('san sang')"
python lab13.py
```

Lệnh `python -c` kiểm tra thư viện phải in ra `san sang`.

## File trong thư mục

| File | Nội dung |
| --- | --- |
| `lab13.py` | Hàm A1, mô hình chi phí, phân tích A/B, cỡ mẫu D1 và chỉ số E1; `tinh_toan` trả về toàn bộ số liệu |
| `lab13_starter.py` | Bản gốc của `lab13.py`, giữ nguyên để đối chiếu. Tài liệu trong `docs/` gọi file này là "file khởi đầu" |
| `logix_runs.csv` | 1.624 lần chạy của agent |
| `logix_requests.csv` | 1.200 yêu cầu hoàn phí |
| `requirements.txt` | Thư viện cần cài |
| `kiem_tra_checkpoint.py` | Đối chiếu số, bảng báo cáo, YAML, nhãn đã cung cấp và các điều kiện tự kiểm tra; ghi rõ mục chưa có bằng chứng thực tế |

Ý nghĩa từng cột và các công thức: [docs/du_lieu_va_cong_thuc.md](../docs/du_lieu_va_cong_thuc.md).

## Đọc dữ liệu đúng cách

```python
import pandas as pd
runs = pd.read_csv('logix_runs.csv')
reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
```

Thiếu `keep_default_na=False`, ô trống trong cột `quyet_dinh_xem_lai` bị đọc thành `NaN` và các phép so sánh phía sau sai.

## Xuất bằng chứng và kiểm tra checkpoint

Windows PowerShell, sau khi cài requirements:

```powershell
.\.venv\Scripts\python.exe lab13.py --xuat-json
.\.venv\Scripts\python.exe kiem_tra_checkpoint.py
```

Lệnh đầu ghi `report/team/ket_qua_tinh_toan.json` với số chưa làm tròn. Lệnh sau ghi `report/team/kiem_tra_checkpoint.md`; mã thoát 1 nếu có lỗi kỹ thuật, 0 nếu các kiểm tra tự động đạt. Mã 0 không có nghĩa đã đủ bằng chứng CP3, duyệt chéo, thông tin thành viên hoặc nộp LMS.

Khi đổi giá, giả định hoặc cách tính, cần cập nhật các báo cáo rồi chạy đối chiếu lại. Công cụ không tự sửa nhãn người dùng hoặc tạo điểm hội đồng.
