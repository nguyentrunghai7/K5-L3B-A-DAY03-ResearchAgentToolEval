# Báo cáo cá nhân — LeDucPhucLam-2A202603787

## 1. Thông tin thành viên

- Họ tên: Lê Đức Phúc Lâm
- MSSV: 2A202603787
- Email: 26ai.lamldt@vinuni.edu.vn

## 2. Phần việc phụ trách

CP3 (tool mới và unit test) và CP4 (10 eval case của nhóm). Cả nhóm làm trên laptop của Đạt.

## 3. Đóng góp cụ thể

- **CP3:** viết tool mới `dedupe` (`tools/dedupe/tool.py`, `TOOL.md`), đăng ký trong `tools/__init__.py` và `tools.yaml`, viết 8 unit test trong `tests/test_tools_todo.py` (happy path, input xấu, nhánh lỗi); `pytest` 0 failed.
- **CP4:** viết 10 eval case (5 single + 5 multi turn) trong `data/eval_group.json`, trong đó 2 case route tới `dedupe`; chạy `--suite group` (8/10 pass), phân tích 2 case FAIL (G07, G10).

## 4. Bằng chứng

- Bằng chứng CP3–CP4 được nhóm ghi chung trong commit `ab78b1a` trên nhánh `datvu`. Run v2 thử nghiệm riêng của Lâm ở commit `59f4487` trên `v2-prompt-leductruclam`.
  - Tool: `starter_v0/tools/dedupe/tool.py`, `starter_v0/tools/dedupe/TOOL.md`
  - Test: `starter_v0/tests/test_tools_todo.py` (8 test `test_dedupe_*`); `pytest`: 75 passed, 14 skipped, 0 failed
  - Eval nhóm: `starter_v0/data/eval_group.json`, run `starter_v0/runs/v3_B_group_openrouter_20261110T182350557552.json`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Nhóm làm trên laptop của Đạt với Claude Code (Claude Sonnet); Lâm đưa yêu cầu (prompt) cho phần CP3, CP4.
  - Cách kiểm tra: tool được kiểm tra bằng `pytest` chạy offline; `pytest tests/test_tool_contract.py` xanh sau khi thêm tool; 10 case eval được kiểm tra schema bằng script và chạy `--suite group` với `provider_error_cases == 0`.

## 5. Tự đánh giá

(Bạn tự điền: điều gì làm tốt, điều gì chưa, và bạn có giải thích được vì sao tool `dedupe` và các case G07, G10 được thiết kế như vậy không.)
