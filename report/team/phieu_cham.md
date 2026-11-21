# Phiếu chấm hội đồng Gate 2a

Nhóm số n chấm nhóm số n + 1; nhóm cuối chấm nhóm 1. Chấm theo bằng chứng trong hồ sơ, không theo cách trình bày: một đề xuất No-go có lý do bằng số được điểm cao hơn một đề xuất Go bỏ qua con số bất lợi.

- Nhóm chấm (hội đồng): ...
- Nhóm được chấm: ...

| Tiêu chí | 0 điểm | 5 điểm | 10 điểm | Điểm | Lý do (có số) |
| --- | --- | --- | --- | ---: | --- |
| Đề xuất khớp bằng chứng | Mâu thuẫn với số của chính nhóm | Khớp nhưng bỏ qua một con số bất lợi | Khớp, nêu cả con số bất lợi và cách xử lý | 9 | Go có điều kiện khớp số của nhóm: chi phí 4.472 đ/việc (gấp 16,3× hoá đơn 274,7 đ), giờ nhân viên 92,5% tổng chi phí; nêu cả số bất lợi: quoc_te 1,88× (thành công 27,3%), xem lại 100% lên 11.743–12.414 đ (0,98–1,03×), mở lại 4,25%. Trừ 1 điểm vì "kế hoạch giảm xem lại theo bậc" chưa có ngưỡng số. |
| Số giả lập và phạm vi | Không nhãn; phạm vi "mọi yêu cầu" | Có nhãn hoặc có thu hẹp phạm vi | Nhãn ở mọi số giả lập; phạm vi thu hẹp có lý do bằng số | 10 | Số giả lập có nhãn [sim]/simulated ở bảng loại, chi phí cố định 4.599 đ và B1–B4; token 246k, tool 84k ghi "đo từ trace". Phạm vi thu hẹp về noi_dia + hang_nang (0,22× và 0,69×) có lý do bằng số: quoc_te 1,88× và tỉ lệ ok theo lần thử 30,0% → 11,4% → 2,2%, doi_tac 0,85× nhưng loại vì điều khoản riêng. |
| Pilot ra được quyết định | Không đối chứng hoặc thiếu cỡ mẫu | Đủ cỡ mẫu, luật dừng chung chung | Tách được tác động, đủ mẫu, luật dừng có ngưỡng, thời hạn, người có quyền dừng | 9.5 | Tách được tác động: 20 + 20 nhân viên, ngẫu nhiên, đối chứng chạy cùng thời gian; đủ mẫu cho mức chênh 6 điểm (859/nhánh, DE 6,96) và nêu thẳng power chỉ còn 0,64 nếu tác động thật là 5 điểm. Luật dừng có ngưỡng (≥ 2 điểm hoặc > 6%), thời hạn (3 ngày liên tiếp, tắt trong 30 phút), người dừng (Giám đốc vận hành). Trừ 0,5 điểm vì slide chỉ trình bày luật dừng an toàn, chưa có luật dừng theo chi phí. |
| **Tổng** | | | | **28.5 / 30** | |

**Quyết định của hội đồng:** Go có điều kiện

**Lý do:** Phạm vi thu hẹp đúng chỗ rẻ (0,22× và 0,69×), loại quoc_te (1,88×), pilot có đối chứng và đủ mẫu (859/nhánh). Nhưng xem lại 100% đã đưa chi phí lên 0,98–1,03× và power chỉ 0,64 nếu tác động thật là 5 điểm, nên chỉ Go khi bốn điều kiện của đội (chống trùng, ký MDE 6 điểm, đủ event, giảm xem lại theo bậc) có ngưỡng đo được.

**Một câu hỏi cho đội trình:** Nếu tuần đầu phải xem lại 100% (11.743–12.414 đ, tức 0,98–1,03×), chi phí mỗi việc thành công vượt mức nào thì ai dừng pilot, và sau bao nhiêu tuần?

**Câu trả lời của đội trình (ghi lại tại buổi):** ...
