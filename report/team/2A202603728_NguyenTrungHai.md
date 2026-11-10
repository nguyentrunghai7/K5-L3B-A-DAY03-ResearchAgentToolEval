# Báo cáo cá nhân — NguyenTrungHai-2A202603728

## 1. Thông tin thành viên

- Họ tên: Nguyễn Trung Hải
- MSSV: 2A202603728
- Email: 26ai.haint2@vinuni.edu.vn

## 2. Phần việc phụ trách

CP2 (tối ưu prompt và tool declaration v1–v3) và báo cáo nhóm `group_report.md` (Phần A và Phần B). 

## 3. Đóng góp cụ thể

- **CP2:** đưa ra giả thuyết và chạy 3 version, mỗi version một giả thuyết:
  - v1 sửa `system_prompt.md`, bỏ các chỉ dẫn xấu của starter (0.70 lên 0.80).
  - v2 sửa `tools.yaml`, viết lại description và convention args (0.80 lên 0.95).
  - v3 thêm rule routing vào prompt (0.95 xuống 0.90, giả thuyết sai, ghi trung thực).
  - Ghi `version_log.csv` và bảng B1.
- **Báo cáo nhóm:** điền Phần A (A1, A2, A3) và Phần B (B1, B2, B3, B4, B5a, mục 3, 5, 7) của `report/team/group_report.md`, dựa trên run JSON và transcript thật.
- Chưa xong:
  - mở link dùng thử bằng Cloudflare Tunnel và dán URL vào A1;
  - nhờ một người ngoài nhóm thử câu hỏi mẫu A3;
  - tạo repo GitHub đúng tên `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` và push (không có `.env`).

## 4. Bằng chứng

- File/commit/PR: (điền commit hash hoặc link PR của bạn sau khi push lên GitHub)
  - Run: `starter_v0/runs/v1_B_base_openrouter_20261110T180650937286.json`, `v2_B_base_openrouter_20261110T180948507851.json`, `v3_B_base_openrouter_20261110T181141015905.json`
  - Log: `starter_v0/artifacts/version_log.csv`
  - Prompt và tool declaration: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`
  - Báo cáo: `report/team/group_report.md`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Nhóm làm trên laptop của Đạt với Claude Code (Claude Sonnet); Hải đưa yêu cầu (prompt) cho phần CP2 và báo cáo.
  - Cách kiểm tra: mỗi version được đo bằng base eval thật và đọc `failures` trong run JSON; mỗi version có `prompt_hash`/`tools_hash` khác version trước; `pytest tests/test_tool_contract.py` vẫn xanh sau khi sửa.

## 5. Tự đánh giá

