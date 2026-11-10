# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3:

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | Baseline, chưa sửa prompt/tool declaration | Đo hiện trạng để tìm lỗi routing và boundary. | N/A | 0.70 (14/20) | [run v0](../../starter_v0/runs/v0_B_base_openrouter_20261110T180028666992.json) |
| v1 | `artifacts/system_prompt.md`: hỏi lại khi thiếu account/URL | R10 và R11 sẽ cải thiện nếu cấm đoán account/URL và yêu cầu `clarify(response_type="text")`. | 0.70 (14/20) | 0.85 (17/20) | [run v1](../../starter_v0/runs/v1_B_base_openrouter_20261110T182153182485.json) |
| v2 | `artifacts/system_prompt.md`: hỏi xác nhận trước khi gửi/đăng | R12 sẽ PASS nếu agent hỏi `clarify(response_type="yes_no")` thay vì gọi `send` ngay. Thực tế R12 vẫn FAIL: agent hỏi về nội dung với `response_type="text"`; M02 cũng chuyển từ PASS thành FAIL. | 0.85 (17/20) | 0.85 (17/20) | [run v2](../../starter_v0/runs/v2_B_base_openrouter_20261110T191037734610.json) |
| v3 |  |  |  |  |  |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

Baseline v0: [run JSON](../../starter_v0/runs/v0_B_base_openrouter_20261110T180028666992.json), 20/20 case được chấm, `provider_error_cases=0`, 14 PASS và 6 FAIL (`case_accuracy=0.70`). Cột Fix dưới đây là **đề xuất cho các version sau**, chưa phải thay đổi đã áp dụng. Các lần gọi `send` trong v0 đều trả `needs_confirmation`, không gửi tin thật.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R08_out_of_scope | `out_of_scope` | `send(text="Nguyên hàm của x^2 là ...")` | Mong đợi không gọi tool; agent dùng nhầm action tool để trả lời toán học. | Giới hạn `send` cho yêu cầu đăng/gửi đã được xác nhận; câu ngoài phạm vi research không gọi tool. |
| R10_missing_handle | `missing_info` | `timeline(screenname="sama")` | Thiếu tài khoản nhưng agent tự chọn `sama` thay vì `clarify(response_type="text")`. | Khi thiếu tên hoặc handle tài khoản, gọi `clarify` và không đoán. |
| R11_missing_url | `missing_info` | `fetch(url="https://example.com/article")` | Thiếu URL nhưng agent tự tạo URL thay vì `clarify(response_type="text")`. | Khi người dùng nói “bài này” mà không có URL, gọi `clarify` để xin link. |
| R12_confirm_before_send | `wrong_boundary` | `send(text="Bản tin này")` | Agent gọi `send` trước khi hỏi xác nhận; mong đợi `clarify(response_type="yes_no")`. | Hỏi xác nhận rõ nội dung trước; chỉ gọi `send` sau khi user đồng ý và truyền `confirmed=true`. |
| R13_parallel_web_and_tweets | `wrong_tool` | `lookup(query="AI news", timeframe="day", max_results=5)` và `social_search(query="AI", search_type="Latest", limit=5)` | Đã gọi đúng cả hai tool, nhưng `lookup` dùng `query="AI news"` thay vì `"AI"` và bỏ `topic="news"`. | Quy định tin tức web dùng `lookup(query="AI", topic="news", timeframe="day")`; giữ cả hai nguồn khi yêu cầu. |
| R14_out_of_scope_coding | `out_of_scope` | `send(text="Dưới đây là một hàm Python ...")` | Mong đợi không gọi tool; agent dùng nhầm `send` để trả lời yêu cầu viết code. | Không dùng `send` như công cụ trả lời; câu ngoài phạm vi research không gọi tool. |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
