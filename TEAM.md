# Team

## Thông tin nhóm

- Tên nhóm: A nhóm A 
- Lớp: L3A / L3B
- Repo nhóm: `K5-L3A-DAY03-A-ResearchAgentToolEval` hoặc `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Vũ Tuấn Đạt | 2A202603744 | 26ai.datvt@vinuni.edu.vn | datkunal | CP1 (setup, baseline v0), UI và live chat (CP5) |
|   2 | Nguyễn Trung Hải | 2A202603728 | 26ai.haint2@vinuni.edu.vn | nguyentrunghai7 | CP2 (tối ưu v1–v3), báo cáo nhóm |
|   3 | Lê Đức Phúc Lâm | 2A202603787 | 26ai.lamldt@vinuni.edu.vn | truclamld | CP3 (tool `dedupe`, unit test), CP4 (eval nhóm) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## LeDucTrucLam-2A202603787

### Phần việc phụ trách

- CP3 (tool mới và unit test) và CP4 (10 eval case của nhóm). Cả nhóm làm trên laptop của Đạt.

### Đóng góp cụ thể

- CP3: viết tool mới dedupe (tools/dedupe/tool.py, TOOL.md), đăng ký trong tools/__init__.py và tools.yaml, viết 8 unit test trong tests/test_tools_todo.py (happy path, input xấu, nhánh lỗi); pytest 0 failed.
- CP4: viết 10 eval case (5 single + 5 multi turn) trong data/eval_group.json, trong đó 2 case route tới dedupe; chạy --suite group (8/10 pass), phân tích 2 case FAIL (G07, G10).

### Bằng chứng

- File/commit/PR: (điền commit hash hoặc link PR của bạn sau khi push lên GitHub)
  - Tool: `starter_v0/tools/dedupe/tool.py`, `starter_v0/tools/dedupe/TOOL.md`
  - Test: `starter_v0/tests/test_tools_todo.py` (8 test `test_dedupe_*`); `pytest`: 75 passed, 14 skipped, 0 failed
  - Eval nhóm: `starter_v0/data/eval_group.json`, run `starter_v0/runs/v3_B_group_openrouter_20261110T182350557552.json`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Nhóm làm trên laptop của Đạt với Claude Code (Claude Sonnet); Lâm đưa yêu cầu (prompt) cho phần CP3, CP4.
  - Cách kiểm tra: tool được kiểm tra bằng `pytest` chạy offline; `pytest tests/test_tool_contract.py` xanh sau khi thêm tool; 10 case eval được kiểm tra schema bằng script và chạy `--suite group` với `provider_error_cases == 0`.
