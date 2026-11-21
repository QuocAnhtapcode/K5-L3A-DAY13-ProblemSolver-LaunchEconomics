"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Điền các chỗ ghi VIẾT Ở ĐÂY (đánh dấu TODO CP1…CP4). Dữ liệu trong hai file CSV là giả lập.
Bản gốc chưa sửa nằm ở lab13_starter.py.
"""
import math
import pandas as pd

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
# TODO CP1: viết ba hàm dưới đây cho tới khi kiem_tra_dap_an_biet_truoc() in ĐẠT.
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    return 1 / p if k is None else (1 - (1 - p) ** k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    return 1.0 if k is None else 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    return so_lan_chay_ky_vong(p, k) / ti_le_thanh_cong(p, k)


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
# TODO CP1: viết mo_hinh; CP2 gọi lại hàm này với tham số giá và hệ số đã đổi.
def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, xem_lai, lam_lai, tong, thanh_cong, cps (chi phí mỗi việc thành công).
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × LUONG_PHUT. Đây là số GIẢ LẬP, phải ghi nhãn simulated khi báo cáo.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - Các tham số giá/hệ số/max_lan_chay dùng cho Nhiệm vụ B (độ nhạy, giới hạn số lần chạy); giữ mặc định ở A2.
    """
    reqs = reqs.copy()                      # làm trên bản sao, không sửa dữ liệu gốc
    # chỉ giữ các lần chạy thuộc các yêu cầu đang xét (giống WHERE request_id IN (...))
    runs = runs[runs['request_id'].isin(reqs['request_id'])]

    # Khối này dùng cho nhiệm vụ B (giới hạn số lần chạy); ở A2 nó không chạy vì max_lan_chay = None
    if max_lan_chay is not None:
        runs = runs[runs['attempt'] <= max_lan_chay]
        vuot = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0

    # Tiền máy: giá tính cho 1.000 token nên phải chia 1000 trước khi nhân giá
    tien_token = runs['tokens_in'] / 1000 * gia_vao + runs['tokens_out'] / 1000 * gia_ra
    tien_tool = runs['tool_calls'] * gia_tool

    # Tiền người (số giả lập): tổng số phút x lương mỗi phút
    xem_lai = reqs['phut_xem_lai_simulated'].sum() * luong_phut * he_so_xem_lai
    lam_lai = reqs['phut_lam_lai_simulated'].sum() * luong_phut * he_so_lam_lai

    tong = tien_token.sum() + tien_tool.sum() + xem_lai + lam_lai
    thanh_cong = (reqs['ket_qua'] == 'thanh_cong').sum()   # giống COUNT(*) WHERE ket_qua = 'thanh_cong'

    return dict(token=tien_token.sum(),
                tool=tien_tool.sum(),
                chay_lai=(tien_token + tien_tool)[runs['attempt'] > 1].sum(),  # tiền của lần chạy thứ 2, 3
                xem_lai=xem_lai,
                lam_lai=lam_lai,
                tong=tong,
                thanh_cong=thanh_cong,
                cps=tong / thanh_cong,
                hoa_don_moi_yc=(tien_token.sum() + tien_tool.sum()) / len(reqs))


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    ket_qua = mo_hinh(runs, reqs)
    for ten, gia_tri in ket_qua.items():
        print(f'{ten:12s} {gia_tri:>14,.0f}')
# TODO CP1 · Nhiệm vụ A3: tính lại theo từng giá trị của cột loai.
    print('\nA3 · Theo loại yêu cầu')
    print('loai        so_yc  ti_le_tc  lan_chay        cps   so_voi_12k')
    for loai in ['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']:
        con = reqs[reqs['loai'] == loai]          # lọc các yêu cầu của loại này
        kq = mo_hinh(runs, con)                   # tái dùng hàm A2
        so_yc = len(con)
        ti_le_tc = kq['thanh_cong'] / so_yc       # tỉ lệ thành công
        lan_chay = con['so_lan_chay'].mean()      # số lần chạy trung bình mỗi yêu cầu
        print(f"{loai:10s} {so_yc:6d} {ti_le_tc:9.1%} {lan_chay:9.2f} "
              f"{kq['cps']:10,.0f} {kq['cps'] / BASELINE:10.2f}x")

    # Tỉ lệ ok theo từng lần thử (lần 1, 2, 3) cho mỗi loại
    bang = runs.merge(reqs[['request_id', 'loai']], on='request_id')   # giống JOIN hai bảng
    bang['ok'] = bang['status'] == 'ok'
    print('\nTỉ lệ ok theo lần thử')
    print(bang.pivot_table(index='loai', columns='attempt', values='ok', aggfunc='mean').round(3))

# A4 · Chi phí cố định cho phạm vi noi_dia + hang_nang
    CO_DINH = 40_000_000
    YC_MOI_THANG = 45_000
    pham_vi = reqs[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    kq = mo_hinh(runs, pham_vi)
    print('\nA4 · Chi phí cố định (noi_dia + hang_nang)')
    print(f"Việc thành công trong mẫu: {kq['thanh_cong']} / {len(reqs)}, "
          f"tổng {kq['tong']:,.0f}, cps {kq['cps']:,.0f}")
    for ten, he_so in [('45.000 yc/tháng', 1.0), ('Một nửa khối lượng', 0.5)]:
        tc_thang = YC_MOI_THANG * he_so * kq['thanh_cong'] / len(reqs)
        co_dinh_moi_viec = CO_DINH / tc_thang
        tong_moi_viec = kq['cps'] + co_dinh_moi_viec
        print(f"{ten:20s} {tc_thang:10,.0f} {co_dinh_moi_viec:8,.0f} "
              f"{tong_moi_viec:8,.0f} {tong_moi_viec / BASELINE:5.2f}x")
# TODO CP2 · Nhiệm vụ B: đổi từng yếu tố, ghi vào bảng độ nhạy.
    kich_ban = {
        'Giá token gấp đôi':        dict(gia_vao=52, gia_ra=260),
        'Giá token giảm một nửa':   dict(gia_vao=13, gia_ra=65),
        'Xem lại gấp đôi':          dict(he_so_xem_lai=2),
        'Xem lại giảm một nửa':     dict(he_so_xem_lai=0.5),
        'Làm lại gấp đôi':          dict(he_so_lam_lai=2),
        'Làm lại giảm một nửa':     dict(he_so_lam_lai=0.5),
        'Lương tăng 25%':           dict(luong_phut=2500),
        'Tối đa 2 lần chạy':        dict(max_lan_chay=2),
        'Chỉ 1 lần chạy':           dict(max_lan_chay=1),
    }
    goc = mo_hinh(runs, reqs)['cps']
    print('\nB1 · Đổi từng yếu tố')
    print(f"{'Gốc (A2)':25s} {goc:8,.0f}")
    for ten, kw in kich_ban.items():
        cps = mo_hinh(runs, reqs, **kw)['cps']     # **kw: truyền các tham số trong dict vào hàm
        print(f'{ten:25s} {cps:8,.0f} {(cps / goc - 1) * 100:+6.1f}%')
# B2 · Đổi một cặp: giá token gấp đôi + xem lại gấp đôi
    cps_cap = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2)['cps']
    print(f"\nB2 · Token x2 + xem lại x2: {cps_cap:,.0f} ({(cps_cap / goc - 1) * 100:+.1f}%)")
# B3 · Chi phí cả hệ thống theo giới hạn số lần chạy
    print('\nB3 · Giới hạn số lần chạy: chi phí cả hệ thống cho 1.200 yêu cầu')
    print(f"{'Giới hạn':10s} {'Tổng trợ lý':>12s} {'Không TC':>9s} {'Cả hệ thống':>12s} {'cps':>7s}")
    for k in [1, 2, 3]:
        kq = mo_hinh(runs, reqs, max_lan_chay=k)
        khong_tc = len(reqs) - kq['thanh_cong']            # số yêu cầu nhân viên phải làm thay
        ca_he_thong = kq['tong'] + khong_tc * BASELINE
        print(f"{k:<10d} {kq['tong']:12,.0f} {khong_tc:9d} {ca_he_thong:12,.0f} {kq['cps']:7,.0f}")
# B4 · Xem lại 100% cho noi_dia + hang_nang
    pham_vi = reqs[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    runs_pv = runs[runs['request_id'].isin(pham_vi['request_id'])]
    so_yc_ok = runs_pv.loc[runs_pv['status'] == 'ok', 'request_id'].nunique()   # yêu cầu có ít nhất 1 lần chạy ok
    so_lam_lai = (pham_vi['ket_qua'] == 'lam_lai').sum()
    so_tc = (pham_vi['ket_qua'] == 'thanh_cong').sum()
    tien_may = (runs_pv['tokens_in'] / 1000 * GIA_VAO + runs_pv['tokens_out'] / 1000 * GIA_RA
                + runs_pv['tool_calls'] * GIA_TOOL).sum()
    phut_lam_lai_tb = reqs.loc[reqs['ket_qua'] == 'lam_lai', 'phut_lam_lai_simulated'].mean()
    print(f'\nB4 · Xem lại 100% (noi_dia + hang_nang): {len(pham_vi)} yc, {so_yc_ok} yc có lần chạy ok, '
          f'{so_lam_lai} ca làm lại, {so_tc} việc thành công, tiền máy {tien_may:,.0f}')
    print(f'Phút làm lại trung bình trong dữ liệu: {phut_lam_lai_tb:.1f}')
    for phut_lam_lai in [9, phut_lam_lai_tb]:
        xem_lai = so_yc_ok * 5 * LUONG_PHUT
        lam_lai = so_lam_lai * phut_lam_lai * LUONG_PHUT
        tong = xem_lai + lam_lai + tien_may
        cps = tong / so_tc
        hoa_von = (BASELINE * so_tc - lam_lai - tien_may) / (so_yc_ok * LUONG_PHUT)   # số phút xem lại để cps = 12.000
        print(f'Làm lại {phut_lam_lai:4.1f} phút: tổng {tong:,.0f}, cps {cps:,.0f} = {cps / BASELINE:.2f}x, '
              f'hoà vốn khi xem lại <= {hoa_von:.1f} phút')
# TODO CP4 · Nhiệm vụ D: cỡ mẫu.
#   from statsmodels.stats.proportion import proportion_effectsize
#   from statsmodels.stats.power import NormalIndPower
    from statistics import NormalDist
    from statsmodels.stats.proportion import proportion_effectsize
    from statsmodels.stats.power import NormalIndPower

    def co_mau(p1, p2, alpha=0.05, power=0.8):
        """Cỡ mẫu mỗi nhóm để so hai tỉ lệ p1 và p2 (công thức trong đề)."""
        za = NormalDist().inv_cdf(1 - alpha / 2)   # 1,96
        zb = NormalDist().inv_cdf(power)           # 0,84
        pb = (p1 + p2) / 2
        tu = (za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
        return math.ceil(tu / (p2 - p1) ** 2)      # làm tròn lên

    ICC = 0.02
    print('\nD1 · Cỡ mẫu')
    n_a = co_mau(0.70, 0.75)
    print(f'a) Chia theo yêu cầu: {n_a} yêu cầu mỗi nhóm')

    m = 75
    de_b = 1 + (m - 1) * ICC
    n_b = math.ceil(n_a * de_b)
    nv_b = math.ceil(n_b / m)
    print(f'b) Theo nhân viên, m = {m}: DE = {de_b:.2f}, cần {n_b} yêu cầu mỗi nhóm = {nv_b} nhân viên '
          f'mỗi nhóm, tổng {2 * nv_b} > 40 → không đủ người')

    print(f'c) 20 nhân viên mỗi nhóm: cỡ mẫu hiệu dụng tối đa < 20 / ICC = {20 / ICC:,.0f} < {n_a} → không đạt')
    print(f'd) 6 depot mỗi nhóm: cỡ mẫu hiệu dụng tối đa < 6 / ICC = {6 / ICC:,.0f}')

    n_e = co_mau(0.70, 0.76)
    m_e = math.ceil(n_e * (1 - ICC) / (20 - n_e * ICC))   # giải 20m / (1 + (m-1)ICC) >= n_e
    print(f'e) Mức chênh 6 điểm cần {n_e} mỗi nhóm; 20 nhân viên mỗi nhóm → mỗi người ít nhất {m_e} '
          f'yêu cầu (DE = {1 + (m_e - 1) * ICC:.2f})')

    pw = NormalIndPower().power(effect_size=proportion_effectsize(0.75, 0.70), nobs1=n_e, alpha=0.05)
    print(f'Power nếu tác động thật chỉ 5 điểm mà cỡ mẫu {n_e}: {pw:.2f}')

    # Tỉ lệ mở lại hiện tại, cần trước khi đặt luật dừng an toàn
    print(f"Tỉ lệ mở lại 7 ngày hiện tại: {reqs['mo_lai_trong_7_ngay'].mean():.2%} "
          f"({reqs['mo_lai_trong_7_ngay'].sum()}/{len(reqs)}); trong phạm vi noi_dia + hang_nang: "
          f"{pham_vi['mo_lai_trong_7_ngay'].mean():.2%}")