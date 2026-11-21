"""Kiểm tra số liệu, hồ sơ và trạng thái checkpoint; không tự cho điểm hội đồng.

Chạy: python kiem_tra_checkpoint.py
Ghi report/team/kiem_tra_checkpoint.md; mã thoát 1 khi có lỗi kỹ thuật,
0 khi phần kiểm tra tự động đạt (các mục cần người thực hiện vẫn ghi CHƯA).
"""
import hashlib
import json
import math
from pathlib import Path
import re
import sys

import pandas as pd
import yaml

import lab13

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'report' / 'team'
checks = []


def check(group, name, fn):
    try:
        fn()
        checks.append((group, name, True, 'ĐẠT'))
    except (AssertionError, KeyError, ValueError, TypeError, IndexError) as exc:
        checks.append((group, name, False, str(exc) or 'Điều kiện không đạt'))


def require(condition, message):
    assert condition, message


def close(actual, expected, tolerance=.02):
    require(abs(actual - expected) <= max(abs(expected) * tolerance, 1e-9),
            f'{actual} khác mốc {expected} quá {tolerance:.1%}')


def read(name):
    return (REPORT / name).read_text(encoding='utf-8-sig')


def rows_in(text, heading):
    section = text.split('## ' + heading, 1)[1].split('\n## ', 1)[0]
    rows = []
    for line in section.splitlines():
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if all(re.fullmatch(r'[:\- ]+', c) for c in cells):
                continue
            rows.append(cells)
    return rows[1:]


def number(value):
    return float(value.replace('.', '').replace(',', '.').replace('%', '').replace('×', '').replace('đ', '').strip())


runs = pd.read_csv(ROOT / 'src' / 'logix_runs.csv')
reqs = pd.read_csv(ROOT / 'src' / 'logix_requests.csv', keep_default_na=False)
r = lab13.tinh_toan(runs, reqs)
cost_text = read('bang_chi_phi.md')
error_text = read('bang_loi.md')
metric_text = read('chi_so.md')
launch_text = read('ho_so_launch_v0.md')
plan_text = read('pilot_plan.yaml')
plan = yaml.safe_load(plan_text)['pilot']


def integrity():
    expected = {
        'src/logix_runs.csv': '521145e65c645e7ecbdd48e3a4d91a015ddd14beaf163f2bfe439107b735231d',
        'src/logix_requests.csv': '7fcb7a23afbabe4d1b8f60980f147f87061050d4d43aa3a2cd11db1fcb71d06e',
        'src/lab13_starter.py': 'bca82257c919e1452946239d4f34ec5719eafe3c163f60d388dc4fc843b4909f',
    }
    for name, digest in expected.items():
        require(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest,
                name + ' thay đổi so với trước lượt hoàn thiện')
    require(len(reqs) == 1200 and len(runs) == 1624, 'Sai kích thước dữ liệu')
    require(reqs.request_id.is_unique and runs.run_id.is_unique, 'ID trùng')
    require(runs.request_id.isin(reqs.request_id).all(), 'Run không có request')


check('Chung', 'CSV và starter giữ nguyên byte so với trước lượt hoàn thiện; ID hợp lệ', integrity)
check('CP1', 'Ba phép thử A1', lab13.kiem_tra_dap_an_biet_truoc)


def cost_reference():
    for key, expected in dict(token=245585, tool=84000, chay_lai=93804,
                              xem_lai=1780000, lam_lai=2264000,
                              tong=4373585, thanh_cong=978, cps=4472).items():
        close(r['a2'][key], expected)
    for row in r['a3']:
        close(row['cps'], dict(noi_dia=2696, hang_nang=8221, quoc_te=22515, doi_tac=10215)[row['loai']])
    close(r['a4'][0]['cps'], 4599)
    close(r['a4'][1]['cps'], 5784)


check('CP1', 'A2, bốn loại A3, hai mức A4 trong dung sai 2% của docs', cost_reference)


def report_cost():
    require(len(rows_in(cost_text, 'A1')) == 3, 'A1 thiếu dòng')
    a2 = rows_in(cost_text, 'A2')
    require(len(a2) == 9, 'A2 không đủ 9 dòng')
    for row, key in zip(a2, ['token','tool','chay_lai','xem_lai','lam_lai','tong','thanh_cong','cps','hoa_don_moi_yc']):
        close(number(row[1]), r['a2'][key], .005)
    a3 = rows_in(cost_text, 'A3')
    require(len(a3) == 4, 'A3 không đủ 4 loại')
    for row in a3:
        actual = next(x for x in r['a3'] if x['loai'] == row[0])
        close(number(row[4]), actual['cps'], .005)
    a4 = rows_in(cost_text, 'A4')
    require(len(a4) == 2, 'A4 thiếu mức khối lượng')
    for row, expected in zip(a4, r['a4']):
        close(number(row[1]), expected['thanh_cong_thang'], .005)
        close(number(row[2]), expected['co_dinh_moi_viec'], .005)
        close(number(row[3]), expected['cps'], .005)
    require('simulated' in cost_text, 'Thiếu nhãn simulated')


check('CP1', 'Báo cáo A đủ bảng và số đối chiếu với chương trình', report_cost)


def scenario_checks():
    expected = [4723,4346,6292,3562,6787,3315,5506,4237,4111]
    for actual, ref in zip(r['b1'], expected):
        close(actual['cps'], ref)
    for doubled, halved in [(0,1),(2,3),(4,5)]:
        require(math.isclose(r['b1'][doubled]['thay_doi'], -2*r['b1'][halved]['thay_doi'], abs_tol=1e-9), 'Độ nhạy nửa/gấp đôi sai')
    require(math.isclose(r['b2']['thay_doi'], r['b1'][0]['thay_doi']+r['b1'][2]['thay_doi'], abs_tol=1e-9), 'Cặp tác động không cộng đúng')
    require(min(r['b3'],key=lambda x:x['ca_he_thong'])['gioi_han']==2, 'B3 chọn sai')
    require([x['khong_thanh_cong'] for x in r['b3']]==[319,234,222], 'B3 đếm sai')
    close(r['b4'][0]['cps'],11743)
    close(r['b4'][1]['cps'],12414)
    before = reqs.copy(deep=True)
    lab13.mo_hinh(runs, reqs, max_lan_chay=1)
    pd.testing.assert_frame_equal(before, reqs)
    subset = reqs[reqs.loai.eq('noi_dia')]
    filtered = runs[runs.request_id.isin(subset.request_id)]
    require(lab13.mo_hinh(runs, subset)==lab13.mo_hinh(filtered, subset), 'Chi phí lọt từ loại khác')


check('CP2', '9 kịch bản, cộng tác động, B3/B4, không sửa dữ liệu và lọc đúng request', scenario_checks)


def report_scenarios():
    b1 = rows_in(cost_text, 'B1')
    require(len(b1)==9, 'B1 thiếu dòng')
    for row, expected in zip(b1,r['b1']):
        close(number(row[2]), expected['cps'], .005)
        require(abs(number(row[3])-expected['thay_doi'])<.06, 'B1 sai phần trăm làm tròn')
    b3 = rows_in(cost_text, 'B3')
    require(len(b3)==3,'B3 thiếu giới hạn')
    for row, expected in zip(b3, r['b3']):
        close(number(row[1]), expected['tong_tro_ly'], .005)
        require(number(row[2])==expected['khong_thanh_cong'], 'B3 sai số việc để lại')
        close(number(row[3]), expected['ca_he_thong'], .005)
        close(number(row[4]), expected['cps'], .005)
    b4 = rows_in(cost_text, 'B4')
    require(len(b4)==2,'B4 thiếu giả định phút làm lại')
    for row, expected in zip(b4, r['b4']):
        close(number(row[3]), expected['tong'], .005)
        close(number(row[4]), expected['cps'], .005)


check('CP2', 'Báo cáo B1 đủ 9 dòng, B3 đủ 3 dòng và B4 đủ 2 giả định', report_scenarios)


def labels_and_repairs():
    submitted = rows_in(error_text, 'Hai bộ nhãn độc lập')
    require(len(submitted)==20,'Bảng nhãn thiếu ca')
    reference = {
        'Do người dùng': {1, 6, 9, 14}, 'Hệ thống': {2, 7, 8, 15, 20},
        'Ngữ cảnh': {3, 10, 16, 18}, 'Giới hạn hệ thống': {4, 11, 13, 19},
        'Ngầm': {5, 12, 17},
    }
    require(all(int(row[0]) in reference.get(row[1], set()) for row in submitted),
            'Bộ đã cung cấp khác nhãn tham khảo trong docs')
    repairs = rows_in(error_text,'Bảng khắc phục cho 5 ca')
    require(len(repairs)==5,'Bảng khắc phục thiếu ca')
    require({x[1] for x in repairs}=={'Do người dùng','Hệ thống','Ngữ cảnh','Giới hạn hệ thống','Ngầm'},'Thiếu loại lỗi')
    require(all(len(x)==5 and all(x) for x in repairs),'Thiếu phát hiện, khắc phục hoặc vai trò')


check('CP3', 'Đủ 20 ca bộ đã cung cấp và 5 loại khắc phục', labels_and_repairs)


def pilot_check():
    for key in ['owner','scope','assignment','rollout','primary_metric','identifiability',
                'stop_rules','interim_looks','rollback','decision_date','simulated_inputs']:
        require(key in plan,'Thiếu trường '+key)
    require(not any('?' in line for line in plan_text.splitlines() if not line.lstrip().startswith('#')), 'Còn dấu hỏi trong dữ liệu YAML')
    require(r['d1']['n5']==1251 and r['d1']['n6']==859 and r['d1']['m6']==299,'D1 sai cỡ mẫu')
    pm=plan['primary_metric']
    require(pm['n_per_arm']==pm['min_requests_per_staff']*pm['clusters_per_arm'],'Mẫu thực tế không khớp số người')
    require(pm['n_per_arm']/pm['design_effect']>=pm['effective_n_per_arm'],'Mẫu hiệu dụng không đạt')
    require(pm['clusters_per_arm']>=20 and pm['mde']==.06,'Sai đánh đổi')
    require(plan['assignment']['randomized'] is True,'Thiếu ngẫu nhiên')
    require(len(plan['stop_rules'])>=3,'Thiếu luật dừng')
    for rule in plan['stop_rules']:
        require(all(word in rule for word in ['NẾU','TRONG','THÌ','KHÔNG THÌ']),'Luật dừng thiếu vế')
    from datetime import date
    end=date.fromisoformat(plan['enrollment_end_date'])
    follow=date.fromisoformat(plan['followup_end_date'])
    decision=date.fromisoformat(plan['decision_date'])
    require((follow-end).days>=8 and decision>follow,'Thiếu 24h đóng +7 ngày theo dõi')
    require(all(k in plan['identifiability'] for k in ['concurrent_control','spillover_risk','predeclared']),'Thiếu D2')
    require(len(plan['simulated_inputs'])>=6,'Chưa liệt kê đầu vào giả lập')


check('CP4','D1/D2, YAML hợp lệ, mẫu thực tế/hiệu dụng, luật dừng và cửa sổ theo dõi',pilot_check)


def metric_check():
    require(r['e']['primary_count']==994 and r['e']['overrides']==48 and r['e']['reviewed']==177 and r['e']['reopened']==51,'E1 sai số đếm')
    ev=rows_in(metric_text,'Danh sách event')
    require(len(ev)>=6 and all('trace_id' in ' '.join(row) for row in ev),'Event thiếu trace_id')
    require(len(rows_in(metric_text,'E2'))>=2,'Thiếu rủi ro')
    launch_rows=[line for line in launch_text.splitlines() if re.match(r'^\| [1-7] ·',line)]
    require(len(launch_rows)==7,'Hồ sơ chưa đủ 7 mục')
    require(launch_text.strip().splitlines()[-1].startswith('**Đề xuất: Go có điều kiện**'),'Dòng cuối chưa là đề xuất')
    require('0,642' in launch_text,'Bỏ qua power bất lợi')
    require('simulated' in metric_text and 'simulated' in launch_text,'Thiếu nhãn')


check('CP5','Ba chỉ số, event, rủi ro và hồ sơ 7 mục có đề xuất',metric_check)


def general_reports():
    for path in REPORT.glob('*'):
        if path.suffix in ['.md','.yaml']:
            text=path.read_text(encoding='utf-8-sig')
            require(not re.search('production',text,re.I), 'Có từ cấm trong '+path.name)
    saved=json.loads(read('ket_qua_tinh_toan.json'))
    require(saved==r,'JSON chưa đồng bộ với code/CSV')
    for name in ['bang_chi_phi.md','bang_loi.md','pilot_plan.yaml','chi_so.md','ho_so_launch_v0.md','phieu_cham.md','group_report.md']:
        require('...' not in read(name),'Còn chỗ giữ trống trong '+name)


check('Chung','Đủ file, JSON khớp, không có từ cấm hoặc chỗ giữ trống trong hồ sơ chính',general_reports)

lines=['# Kiểm tra checkpoint sau hoàn thiện','',
       'Kiểm tra bằng `src/kiem_tra_checkpoint.py`; số từ `src/lab13.py` và hai CSV. Đây là kiểm tra kỹ thuật, không thay điểm giảng viên hoặc hội đồng.','',
       '| Phần | Kết quả | Căn cứ |','| --- | --- | --- |']
summary=[
('CP1 · A','ĐẠT phần phân tích','A1, A2, 4 loại A3, 2 mức A4 và báo cáo.'),
('CP2 · B','ĐẠT phần phân tích','9 kịch bản B1, B2, 3 giới hạn B3, 2 giả định B4.'),
('CP3 · C','CHƯA ĐỦ','Có bộ nhãn người dùng cung cấp và 5 cách khắc phục; thiếu bộ thứ hai, tên và bằng chứng độc lập nên chưa tính đồng thuận.'),
('CP4 · D','ĐẠT hồ sơ kế hoạch','D1/D2, 20 cụm/nhánh, 5.980 thực tế và 859 hiệu dụng; MDE 6 điểm, 4 luật dừng. Lịch và roster là đề xuất, chưa triển khai.'),
('CP5 · E','ĐẠT nội dung E; duyệt chéo CHƯA','3 chỉ số, 12 event, 4 rủi ro, 7 mục launch. Chưa có phiếu hội đồng thực tế.'),
('Đóng gói','CHƯA ĐỦ','Thiếu xác nhận tên nhóm/lớp, danh tính và báo cáo cá nhân, đóng góp, chạy máy thứ hai, repo/commit/push/LMS.')]
for group,status,why in summary:
    groupkey=group.split(' · ')[0]
    if any(not ok for g,_,ok,_ in checks if g==groupkey): status='CÓ LỖI KỸ THUẬT'
    lines.append(f'| {group} | {status} | {why} |')
lines+=['','## Kiểm tra tự động','', '| Nhóm | Phép kiểm tra | Kết quả |','| --- | --- | --- |']
for group,name,ok,detail in checks:
    lines.append(f'| {group} | {name} | {"ĐẠT" if ok else "LỖI: "+detail} |')
lines += ['', '## Điểm cần hiểu khi bảo vệ', '',
          '- A2 CPS 4.472 đ và A4/B4 chi phí đều simulated; không suy ra mức tiết kiệm toàn công ty từ CPS/baseline.',
          '- B3 theo quy ước chi phí của đề; 2 lượt rẻ nhất toàn mẫu. Phạm vi pilot 2 lượt được tính riêng 892/982 thành công, CPS 3.252 đ — simulated.',
          '- B4 tính 15,3 phút cho CPS 12.414,7925 đ, làm tròn 12.415 đ — simulated; hướng dẫn ghi 12.414, sai khác nhỏ hơn dung sai 2%.',
          '- Dùng 5.980 request thực tế mỗi nhánh và DE 6,96 để đạt 859 hiệu dụng; không lấy 859 làm số request cần thu.',
          '- Tác động thật 5 điểm chỉ có power khoảng 0,642; pilot đề xuất chấp nhận mục tiêu 6 điểm.',
          '- Bộ nhãn người dùng đã gửi khớp 20/20 tham khảo không đồng nghĩa hai người độc lập đồng thuận 100%.',
          '- CSV và starter giữ nguyên byte so với lúc bắt đầu lượt này. Git đã báo starter có thay đổi trước lượt này; không tự hoàn nguyên phần người dùng.',
          '', '## Chạy lại', '', 'Từ src: `.\\.venv\\Scripts\\python.exe lab13.py --xuat-json` rồi `.\\.venv\\Scripts\\python.exe kiem_tra_checkpoint.py`.',
          'JSON được cập nhật theo code; nếu đổi giả định, phải cập nhật các báo cáo và chạy đối chiếu lại.']
(REPORT/'kiem_tra_checkpoint.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
for group,name,ok,detail in checks:
    print(('ĐẠT' if ok else 'LỖI')+' | '+group+' | '+name+(' | '+detail if not ok else ''))
print('\nCP3 và duyệt chéo/thông tin thành viên vẫn CHƯA đủ bằng chứng.')
print('Báo cáo:',REPORT/'kiem_tra_checkpoint.md')
sys.exit(1 if any(not ok for _,_,ok,_ in checks) else 0)
