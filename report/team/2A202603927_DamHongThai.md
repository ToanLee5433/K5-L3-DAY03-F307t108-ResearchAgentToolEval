# Báo cáo cá nhân — 2A202603927_DamHongThai

## 1. Thông tin thành viên

- Họ tên: Đàm Hồng Thái
- MSSV: 2A202603927
- Email: thai.dh1012@gmail.com
- Vai trò: Thành viên (Member)
- Nhóm: F307t108 — Lớp L3B

## 2. Phần việc phụ trách

- Thành viên: Đồng phụ trách phân tích log lỗi baseline `v0` và các version đánh giá.
- Phụ trách chính xây dựng bộ 10 Eval Cases (5 single-turn, 5 multi-turn) trong `data/eval_group.json` (CP4).
- Phụ trách chạy thực nghiệm Chat Live đa lượt (`chat.py`) ghi nhận transcript thực tế (CP5).
- Đồng biên soạn và rà soát báo cáo nhóm `report/team/group_report.md` (CP5).

## 3. Đóng góp cụ thể

- Soạn thảo 10 kịch bản kiểm thử trong `eval_group.json` bao phủ các trường hợp edge cases, thiếu thông tin và gọi tool mới.
- Chạy kiểm thử live chat đa lượt, đối soát kết quả tool `clarify`, `lookup`, `timeline` và kiểm soát rủi ro của `send`.
- Tổng hợp số liệu từ các file `runs/*.json` vào bảng phân tích B1, B2, B3 trong `group_report.md`.

## 4. Bằng chứng

- File/commit/PR:
  - `starter_v0/data/eval_group.json`
  - `starter_v0/transcripts/*.transcript.json`
  - Báo cáo nhóm: `report/team/group_report.md`
  - `TEAM.md`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Sử dụng AI để gợi ý các test scenario phức tạp.
  - Tự kiểm chứng bằng cách chạy `run_eval.py --suite group` và kiểm tra transcript JSON đảm bảo flow logic chạy đúng.

## 5. Tự đánh giá

- Mức độ hoàn thành: 100% các nhiệm vụ được phân công.
