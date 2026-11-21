"""Lab 13: tính A, B, D1, E từ CSV giả lập; chạy offline.

Chạy: python lab13.py
Xuất bằng chứng: python lab13.py --xuat-json
Giá là giả định của lab. Mọi chi phí có thời gian nhân viên mang nhãn simulated.
"""
import argparse
import json
import math
from pathlib import Path
from statistics import NormalDist

import pandas as pd
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

GIA_VAO = 26
GIA_RA = 130
GIA_TOOL = 15
LUONG_PHUT = 2000
BASELINE = 12000
CO_DINH_THANG = 40000000
SRC = Path(__file__).resolve().parent
REPORT = SRC.parent / 'report' / 'team'


def so_lan_chay_ky_vong(p, k=None):
    """Mô hình lý thuyết: các lần thử độc lập, 0 < p <= 1."""
    return 1 / p if k is None else (1 - (1 - p) ** k) / p


def ti_le_thanh_cong(p, k=None):
    return 1.0 if k is None else 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    return so_lan_chay_ky_vong(p, k) / ti_le_thanh_cong(p, k)


def kiem_tra_dap_an_biet_truoc():
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9
    print('Ba phép thử đáp án biết trước: ĐẠT (1,20; 1,25; 1,25)')


def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Cộng mọi run; mẫu số chỉ là request thành công.

    Cắt lượt chạy theo quy ước B1/B3 của đề; không thay đổi bảng đầu vào.
    chay_lai là phần nằm trong token + tool, không cộng thêm vào tong.
    xem_lai, lam_lai, tong, cps đều có thành phần simulated.
    """
    reqs = reqs.copy()
    runs = runs[runs['request_id'].isin(reqs['request_id'])]
    if max_lan_chay is not None:
        runs = runs[runs['attempt'] <= max_lan_chay]
        vuot = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0
    tien_token = runs.tokens_in / 1000 * gia_vao + runs.tokens_out / 1000 * gia_ra
    tien_tool = runs.tool_calls * gia_tool
    xem_lai = reqs.phut_xem_lai_simulated.sum() * luong_phut * he_so_xem_lai
    lam_lai = reqs.phut_lam_lai_simulated.sum() * luong_phut * he_so_lam_lai
    tong = float(tien_token.sum() + tien_tool.sum() + xem_lai + lam_lai)
    thanh_cong = int(reqs.ket_qua.eq('thanh_cong').sum())
    return dict(
        token=float(tien_token.sum()), tool=float(tien_tool.sum()),
        chay_lai=float((tien_token + tien_tool)[runs.attempt > 1].sum()),
        xem_lai=float(xem_lai), lam_lai=float(lam_lai), tong=tong,
        thanh_cong=thanh_cong, cps=tong / thanh_cong if thanh_cong else None,
        hoa_don_moi_yc=float((tien_token.sum() + tien_tool.sum()) / len(reqs))
        if len(reqs) else None,
    )


def co_mau(p1, p2, alpha=0.05, power=0.8):
    """Công thức so hai tỷ lệ trong docs, làm tròn lên mỗi nhóm."""
    za = NormalDist().inv_cdf(1 - alpha / 2)
    zb = NormalDist().inv_cdf(power)
    pb = (p1 + p2) / 2
    return math.ceil((za * math.sqrt(2 * pb * (1 - pb))
                      + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
                     / (p2 - p1) ** 2)


def tinh_toan(runs, reqs):
    """Một nguồn số duy nhất cho màn hình, JSON và các bảng báo cáo."""
    goc = mo_hinh(runs, reqs)
    pham_vi = reqs[reqs.loai.isin(['noi_dia', 'hang_nang'])]
    cp_pv = mo_hinh(runs, pham_vi)
    a3 = []
    for loai, nhom in reqs.groupby('loai', sort=True):
        kq = mo_hinh(runs, nhom)
        a3.append(dict(loai=loai, so_yc=len(nhom),
                       thanh_cong=kq['thanh_cong'],
                       ti_le=kq['thanh_cong'] / len(nhom),
                       lan_chay_tb=float(nhom.so_lan_chay.mean()),
                       cps=kq['cps'], so_baseline=kq['cps'] / BASELINE))
    # Nối một lần ngoài vòng lặp theo loại.
    theo_lan = runs.merge(reqs[['request_id', 'loai']], on='request_id',
                          validate='many_to_one')
    theo_lan['ok'] = theo_lan.status.eq('ok')
    ok_theo_lan = [dict(loai=loai, attempt=int(attempt), ti_le=float(ti_le))
                   for (loai, attempt), ti_le in
                   theo_lan.groupby(['loai', 'attempt']).ok.mean().items()]
    a4 = []
    for volume in [45000, 22500]:
        successes = volume * cp_pv['thanh_cong'] / len(reqs)
        fixed = CO_DINH_THANG / successes
        a4.append(dict(khoi_luong=volume, thanh_cong_thang=successes,
                       co_dinh_moi_viec=fixed, cps=cp_pv['cps'] + fixed,
                       so_baseline=(cp_pv['cps'] + fixed) / BASELINE))
    scenarios = [
        ('Giá token gấp đôi', dict(gia_vao=52, gia_ra=260)),
        ('Giá token giảm nửa', dict(gia_vao=13, gia_ra=65)),
        ('Xem lại gấp đôi', dict(he_so_xem_lai=2)),
        ('Xem lại giảm nửa', dict(he_so_xem_lai=0.5)),
        ('Làm lại gấp đôi', dict(he_so_lam_lai=2)),
        ('Làm lại giảm nửa', dict(he_so_lam_lai=0.5)),
        ('Lương tăng 25%', dict(luong_phut=2500)),
        ('Tối đa 2 lần', dict(max_lan_chay=2)),
        ('Tối đa 1 lần', dict(max_lan_chay=1)),
    ]
    b1 = []
    for ten, kwargs in scenarios:
        cost = mo_hinh(runs, reqs, **kwargs)
        b1.append(dict(kich_ban=ten, tham_so=kwargs, cps=cost['cps'],
                       thay_doi=(cost['cps'] / goc['cps'] - 1) * 100))
    pair = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2)
    b2 = dict(cps=pair['cps'], thay_doi=(pair['cps'] / goc['cps'] - 1) * 100)
    b3 = []
    for cap in [1, 2, 3]:
        cost = mo_hinh(runs, reqs, max_lan_chay=cap)
        failed = len(reqs) - cost['thanh_cong']
        b3.append(dict(gioi_han=cap, tong_tro_ly=cost['tong'],
                       khong_thanh_cong=failed,
                       ca_he_thong=cost['tong'] + failed * BASELINE,
                       cps=cost['cps']))
    rr = runs[runs.request_id.isin(pham_vi.request_id)]
    ok = int(rr.loc[rr.status.eq('ok'), 'request_id'].nunique())
    wrong = int(pham_vi.ket_qua.eq('lam_lai').sum())
    mins_mean = float(reqs.loc[reqs.ket_qua.eq('lam_lai'),
                               'phut_lam_lai_simulated'].mean())
    b4 = []
    for mins in [9.0, 15.3]:
        review = ok * 5 * LUONG_PHUT
        rework = wrong * mins * LUONG_PHUT
        total = cp_pv['token'] + cp_pv['tool'] + review + rework
        b4.append(dict(phut_lam_lai=mins, yc_ok=ok, ca_lam_lai=wrong,
                       token_tool=cp_pv['token'] + cp_pv['tool'],
                       xem_lai=review, lam_lai=rework, tong=total,
                       thanh_cong=cp_pv['thanh_cong'], cps=total / cp_pv['thanh_cong'],
                       phut_xem_lai_hoa_von=(BASELINE * cp_pv['thanh_cong']
                           - cp_pv['token'] - cp_pv['tool'] - rework) / (ok * LUONG_PHUT)))
    n5, n6, icc = co_mau(.70, .75), co_mau(.70, .76), .02
    de75 = 1 + 74 * icc
    raw75 = math.ceil(n5 * de75)
    m6 = math.ceil(n6 * (1 - icc) / (20 - n6 * icc))
    de6 = 1 + (m6 - 1) * icc
    power5 = float(NormalIndPower().power(
        effect_size=abs(proportion_effectsize(.70, .75)),
        nobs1=n6, alpha=.05, ratio=1, alternative='two-sided'))
    d1 = dict(n5=n5, de75=de75, n75=raw75,
              nguoi_moi_nhom=math.ceil(raw75 / 75),
              tran20=20 / icc, tran6=6 / icc, n6=n6, m6=m6, de6=de6,
              raw6=20 * m6, effective6=20 * m6 / de6, power5=power5)
    reviewed = reqs[reqs.duoc_xem_lai.eq(1)]
    primary = int((reqs.dong_trong_24h.eq(1) & reqs.mo_lai_trong_7_ngay.eq(0)).sum())
    overrides = int(reviewed.quyet_dinh_xem_lai.isin(['sua', 'bo']).sum())
    reopened = int(reqs.mo_lai_trong_7_ngay.eq(1).sum())
    e = dict(primary_count=primary, primary=primary / len(reqs),
             reviewed=len(reviewed), overrides=overrides,
             override_rate=overrides / len(reviewed), reopened=reopened,
             reopen_rate=reopened / len(reqs),
             scope_reopened=int(pham_vi.mo_lai_trong_7_ngay.eq(1).sum()),
             scope_reopen_rate=float(pham_vi.mo_lai_trong_7_ngay.mean()),
             scope_rework_rate=wrong / len(pham_vi))
    scope_cap2 = mo_hinh(runs, pham_vi, max_lan_chay=2)
    return dict(
        meta=dict(requests=len(reqs), runs=len(runs), depots=int(reqs.depot.nunique()),
                  staff=int(reqs.staff_id.nunique()), scope_requests=len(pham_vi),
                  all_data='giả lập', cost_label='simulated',
                  sources=['logix_runs.csv', 'logix_requests.csv']),
        a1=[so_lan_chay_ky_vong(.8, 2), so_lan_chay_ky_vong(.8),
            he_so_chi_phi_moi_viec_thanh_cong(.8, 3)],
        a2=goc, a3=a3, ok_theo_lan=ok_theo_lan, scope=cp_pv, a4=a4,
        b1=b1, b2=b2, b3=b3, b4=b4, phut_lam_lai_tb=mins_mean,
        d1=d1, e=e, scope_cap2=scope_cap2,
        system_cost_per_request=b3[2]['ca_he_thong'] / len(reqs),
        ratio_invoice=goc['cps'] / goc['hoa_don_moi_yc'],
        rework_share=goc['lam_lai'] / goc['tong'],
        human_share=(goc['xem_lai'] + goc['lam_lai']) / goc['tong'],
    )


def in_bang(title, rows):
    print('\n' + title)
    print(pd.DataFrame(rows).to_string(index=False, float_format=lambda x: f'{x:,.4f}'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--xuat-json', action='store_true',
                        help='Lưu số chưa làm tròn vào report/team/ket_qua_tinh_toan.json')
    args = parser.parse_args()
    runs = pd.read_csv(SRC / 'logix_runs.csv')
    reqs = pd.read_csv(SRC / 'logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    result = tinh_toan(runs, reqs)
    print('Toàn bộ dữ liệu giả lập; mọi chi phí chứa thời gian nhân viên: simulated.')
    print('CPS chưa gồm chi phí cố định, trừ bảng A4; B3 theo quy ước chi phí của lab.')
    in_bang('A2 — Chi phí', [result['a2']])
    in_bang('A3 — Theo loại (chi phí simulated)', result['a3'])
    in_bang('A3 — Tỷ lệ run ok theo lần thử', result['ok_theo_lan'])
    in_bang('A4 — Có chi phí cố định (simulated)', result['a4'])
    in_bang('B1 — Độ nhạy (simulated)', result['b1'])
    in_bang('B2 — Thay một cặp (simulated)', [result['b2']])
    print('Xếp hạng: 1. làm lại; 2. xem lại; 3. lương nhân viên.')
    in_bang('B3 — Chi phí cả hệ thống (simulated)', result['b3'])
    in_bang('B4 — Xem lại 100% (simulated)', result['b4'])
    in_bang('D1 — Cỡ mẫu mỗi nhóm', [result['d1']])
    in_bang('E1 — Chỉ số trong mẫu giả lập, chưa có đối chứng', [result['e']])
    in_bang('Pilot nội địa + hàng nặng, tối đa 2 lần (simulated)', [result['scope_cap2']])
    if args.xuat_json:
        REPORT.mkdir(parents=True, exist_ok=True)
        path = REPORT / 'ket_qua_tinh_toan.json'
        path.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n',
                        encoding='utf-8')
        print('\nĐã xuất:', path)


if __name__ == '__main__':
    main()
