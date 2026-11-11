# Team

## Thông tin nhóm

- Tên nhóm: A nhóm A 
- Lớp: L3B
- Repo nhóm: `K5-L3A-DAY03-A-ResearchAgentToolEval` hoặc `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/nguyentrunghai7/K5-L3B-A-DAY03-ResearchAgentToolEval.git nhánh main

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

## NguyenTrungHai-2A202603728

### Phần việc phụ trách

CP2 (tối ưu prompt và tool declaration v1–v3) và báo cáo nhóm `group_report.md` (Phần A và Phần B). 

### Đóng góp cụ thể

- **CP2:** đưa ra giả thuyết và chạy 3 version, mỗi version một giả thuyết:
  - v1 sửa `system_prompt.md`, bỏ các chỉ dẫn xấu của starter (0.70 lên 0.80).
  - v2 sửa `tools.yaml`, viết lại description và convention args (0.80 lên 0.95).
  - v3 thêm rule routing vào prompt (0.95 xuống 0.90, giả thuyết sai, ghi trung thực).
  - Ghi `version_log.csv` và bảng B1.
- **Báo cáo nhóm:** điền Phần A (A1, A2, A3) và Phần B (B1, B2, B3, B4, B5a, mục 3, 5, 7) của `report/team/group_report.md`, dựa trên run JSON và transcript thật.


### Bằng chứng

- File/commit/PR: (điền commit hash hoặc link PR của bạn sau khi push lên GitHub)
  - Run: `starter_v0/runs/v1_B_base_openrouter_20261110T180650937286.json`, `v2_B_base_openrouter_20261110T180948507851.json`, `v3_B_base_openrouter_20261110T181141015905.json`
  - Log: `starter_v0/artifacts/version_log.csv`
  - Prompt và tool declaration: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`
  - Báo cáo: `report/team/group_report.md`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Nhóm làm trên laptop của Đạt với Claude Code (Claude Sonnet); Hải đưa yêu cầu (prompt) cho phần CP2 và báo cáo.
  - Cách kiểm tra: mỗi version được đo bằng base eval thật và đọc `failures` trong run JSON; mỗi version có `prompt_hash`/`tools_hash` khác version trước; `pytest tests/test_tool_contract.py` vẫn xanh sau khi sửa.

## VuTuanDat-2A202603744

### Phần việc phụ trách

CP1 (setup và baseline v0) và phần UI cùng live chat của CP5. Cả nhóm làm trên laptop của Đạt.

### Đóng góp cụ thể

- **CP1:** cấu hình `.env`, chạy preflight và `pytest`, chạy base eval v0 (14/20 pass, `case_accuracy` 0.70), gán loại lỗi cho 6 case FAIL (bảng B2), ghi dòng v0 vào `version_log.csv`.
- **CP5 (UI):** viết UI Streamlit `starter_v0/app.py`, thêm `streamlit` vào `requirements.txt`, kiểm tra UI bằng `streamlit.testing` với một lượt chat thật.
- **CP5 (live chat):** chạy `chat.py` 2 phiên (7 lượt) gồm yêu cầu thường, thiếu thông tin rồi bổ sung, và yêu cầu đăng; ghi bảng B4 gồm cả lỗi thật ở phiên 1 turn 2.

### Bằng chứng

- File/commit/PR: (điền commit hash hoặc link PR sau khi push lên GitHub)
  - Run v0: `starter_v0/runs/v0_B_base_openrouter_20261110T174924785097.json`
  - Log: `starter_v0/artifacts/version_log.csv`
  - UI: `starter_v0/app.py`
  - Transcript: `starter_v0/transcripts/v3_openrouter_20261110T184429774316.transcript.json`, `v3_openrouter_20261110T184540669868.transcript.json`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả:
  - Dùng Claude Code (Claude Sonnet) trong VS Code để viết code, prompt, test và báo cáo.
  - Cách kiểm tra: mọi thay đổi về prompt/tool đều được đo bằng base eval thật qua OpenRouter và đọc lại `failures` trong run JSON; chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases` (một run v1 bị mất mạng đã bị loại và chạy lại); `pytest tests/test_tool_contract.py` chạy lại sau mỗi lần sửa `tools.yaml`; UI được kiểm tra bằng `streamlit.testing` với một lượt chat thật.

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
