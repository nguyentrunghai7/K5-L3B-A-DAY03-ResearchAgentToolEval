# Báo cáo cá nhân — LeDucTrucLam-2A202603787

## 1. Thông tin thành viên

- Họ tên: Lê Đức Trúc Lâm
- MSSV: 2A202603787
- Email: 26ai.lamldt@vinuni.edu.vn

## 2. Phần việc phụ trách

CP3 (tool mới và unit test) và CP4 (10 eval case của nhóm). Cả nhóm làm trên laptop của Đạt.

## 3. Đóng góp cụ thể

- **CP3:** viết tool mới `dedupe` (`tools/dedupe/tool.py`, `TOOL.md`), đăng ký trong `tools/__init__.py` và `tools.yaml`, viết 8 unit test trong `tests/test_tools_todo.py` (happy path, input xấu, nhánh lỗi); `pytest` 0 failed.
- **CP4:** viết 10 eval case (5 single + 5 multi turn) trong `data/eval_group.json`, trong đó 2 case route tới `dedupe`; chạy `--suite group` (8/10 pass), phân tích 2 case FAIL (G07, G10).

## 4. Bằng chứng

- File/commit/PR: (điền commit hash hoặc link PR của bạn sau khi push lên GitHub)
  - Tool: `starter_v0/tools/dedupe/tool.py`, `starter_v0/tools/dedupe/TOOL.md`
  - Test: `starter_v0/tests/test_tools_todo.py` (8 test `test_dedupe_*`); `pytest`: 75 passed, 14 skipped, 0 failed
  - Eval nhóm: `starter_v0/data/eval_group.json`, run `starter_v0/runs/v3_B_group_openrouter_20261110T182350557552.json`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Nhóm làm trên laptop của Đạt với Claude Code (Claude Sonnet); Lâm đưa yêu cầu (prompt) cho phần CP3, CP4.
  - Cách kiểm tra: tool được kiểm tra bằng `pytest` chạy offline; `pytest tests/test_tool_contract.py` xanh sau khi thêm tool; 10 case eval được kiểm tra schema bằng script và chạy `--suite group` với `provider_error_cases == 0`.

## 5. Tự đánh giá

Trong bài lab này, qua quá trình chạy test AI, mình đã có hiểu biết tốt về từng case test và mục đích của các case đó, ví dụ như test yêu cầu clarify những thông tin không rõ khi user hỏi, hoặc test yêu cầu confirm trước khi gửi hay đăng bài. 

Quá trình quan sát các bài đăng hay tin tức, mình đã phát hiện 1 số tin bị trùng lặp, do vậy mình đã nảy ra ý tưởng build thêm tool dedupe để gộp các tin hay bài đăng MXH bị trùng theo tiêu đề (không theo URL), giúp hạn chế trùng lặp và user có thể đọc nhiều tin khác nhau hơn. Dẫu vậy, tool này hoạt động chưa thực sự tốt khi một số tin vẫn bị bỏ sót không rõ lý do, và nhóm mình sẽ cần phải nghiên cứu sâu hơn lý do mà tool chưa hoạt động tốt và đưa ra cách khắc phục.
