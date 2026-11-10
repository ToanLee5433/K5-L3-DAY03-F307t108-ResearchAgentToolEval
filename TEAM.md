# Team

## Thông tin nhóm

- Tên nhóm: F307t108
- Lớp: L3B
- Repo nhóm: `K5-L3-DAY03-F307t108-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: https://github.com/ToanLee5433/K5-L3-DAY03-F307t108-ResearchAgentToolEval, nhánh `2A202603941-LeQuyToan` (chuẩn bị merge vào `main`)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Lê Quý Toàn | 2A202603941 | lequytoanptit0303@gmail.com | ToanLee5433 | Trưởng nhóm (Leader) |
|   2 | Đàm Hồng Thái | 2A202603927 | damhongthai108@gmail.com | itsbra1vo | Thành viên (Member) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/2A202603941_LeQuyToan.md`.

---

## LeQuyToan-2A202603941

### Phần việc phụ trách

- Trưởng nhóm: Điều phối chung tiến độ các Checkpoint, cấu hình môi trường Provider và Tools.
- Phụ trách chính tối ưu hóa `system_prompt.md` và `tools.yaml` qua các phiên bản `v1`, `v2`, `v3` (CP2).
- Phụ trách thiết kế và phát triển Tool mới cùng Unit Test (`pytest`) đạt 100% pass (CP3).
- Xây dựng giao diện Streamlit UI (`app.py`) phục vụ demo và test chat live (CP5).

### Đóng góp cụ thể

- Phân tích baseline `v0` thất bại, xác định các nhóm lỗi `wrong_tool`, `wrong_arg_value`, `missing_info`.
- Đặt giả thuyết và hoàn thiện `system_prompt.md` production-grade có đầy đủ ranh giới an toàn, chống bịa đặt và xác nhận trước khi gửi.
- Cùng thành viên xây dựng bộ 10 eval cases trong `eval_group.json` và hoàn thiện báo cáo nhóm `group_report.md`.

### Bằng chứng

- `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`
- `starter_v0/artifacts/version_log.csv` (các lượt `v1`, `v2`, `v3`)
- `report/team/group_report.md` (Phần A và Phần B)
- Báo cáo cá nhân: `report/team/2A202603941_LeQuyToan.md`

---

## DamHongThai-2A202603927

### Phần việc phụ trách

- Thành viên: Đồng phụ trách phân tích log lỗi baseline `v0` và các version đánh giá.
- Phụ trách chính xây dựng bộ 10 Eval Cases (5 single-turn, 5 multi-turn) trong `data/eval_group.json` (CP4).
- Phụ trách chạy thực nghiệm Chat Live đa lượt (`chat.py`) ghi nhận transcript thực tế (CP5).
- Đồng biên soạn và rà soát báo cáo nhóm `report/team/group_report.md` (CP5).

### Đóng góp cụ thể

- Soạn thảo 10 kịch bản kiểm thử trong `eval_group.json` bao phủ các trường hợp edge cases, thiếu thông tin và gọi tool mới.
- Chạy kiểm thử live chat đa lượt, đối soát kết quả tool `clarify`, `lookup`, `timeline` và kiểm soát rủi ro của `send`.
- Tổng hợp số liệu từ các file `runs/*.json` vào bảng phân tích B1, B2, B3 trong `group_report.md`.

### Bằng chứng

- `starter_v0/data/eval_group.json`
- `starter_v0/transcripts/*.transcript.json`
- Báo cáo nhóm: `report/team/group_report.md`
- Báo cáo cá nhân: `report/team/2A202603927_DamHongThai.md`
