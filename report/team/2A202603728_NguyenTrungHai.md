# Báo cáo cá nhân — NguyenTrungHai-2A202603728

## 1. Thông tin thành viên

- Họ tên: Nguyễn Trung Hải
- MSSV: 2A202603728
- Email: 26ai.haint2@vinuni.edu.vn

## 2. Phần việc phụ trách

CP2 (tối ưu prompt v1–v3) và báo cáo nhóm `group_report.md` (Phần A và Phần B).

## 3. Đóng góp cụ thể

- **CP2:** chuỗi được chọn cho báo cáo nhóm:
  - v1 yêu cầu hỏi lại khi thiếu tài khoản hoặc URL (14/20 lên 17/20).
  - v2 yêu cầu xác nhận trước khi gửi (17/20, R12 vẫn sai kiểu xác nhận).
  - v3 thêm quy tắc chọn tool và phạm vi (18/20).
  - Ghi `version_log.csv` và bảng B1.
- **Báo cáo nhóm:** điền Phần A (A1, A2, A3) và Phần B (B1, B2, B3, B4, B5a, mục 3, 5, 7) của `report/team/group_report.md`, dựa trên run JSON và transcript thật.
- Bản tích hợp đã kiểm tra UI cục bộ. Link công khai dùng thử đang chờ cập nhật ở A1.

## 4. Bằng chứng

- Commit: `0dff482` (v1), `488b064` (v2), `a49a3fd` (v3).
  - Run: `starter_v0/runs/v1_B_base_openrouter_20261110T182153182485.json`, `v2_B_base_openrouter_20261110T191037734610.json`, `v3_B_base_openrouter_20261110T192900085847.json`
  - Log: `starter_v0/artifacts/version_log.csv`
  - Prompt và tool declaration: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`
  - Báo cáo: `report/team/group_report.md`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Nhóm làm trên laptop của Đạt với Claude Code (Claude Sonnet); Hải đưa yêu cầu (prompt) cho phần CP2 và báo cáo.
  - Cách kiểm tra: mỗi version được đo bằng base eval thật và đọc `failures` trong run JSON; mỗi version có `prompt_hash`/`tools_hash` khác version trước; `pytest tests/test_tool_contract.py` vẫn xanh sau khi sửa.

## 5. Tự đánh giá
