# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: A
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: OpenRouter, model `openai/gpt-4o-mini` (xem trường `provider`, `model` trong các run JSON)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research agent: tìm tin tức trên web, xem bài đăng của một tài khoản hoặc tìm bài đăng theo từ khóa, đọc và tóm tắt một URL, lọc trùng các kết quả gộp từ nhiều nguồn, và soạn thành bản tin. Agent hỏi lại khi người dùng thiếu thông tin (không rõ tài khoản, không có URL), từ chối câu hỏi ngoài phạm vi research, và xin xác nhận trước khi gửi bản tin lên Telegram.

**Cách chạy UI:**

```bash
cd starter_v0
pip install -r requirements.txt     # đã thêm streamlit vào requirements.txt
streamlit run app.py                # mở http://localhost:8501
```

UI là `starter_v0/app.py` (Streamlit). UI hiển thị mọi tool call và kết quả (kể cả lỗi) và ghi transcript vào `starter_v0/transcripts/`. Giới hạn 20 lượt cho mỗi cuộc trò chuyện.

**Link dùng thử (deploy):**

- Chạy thử trên máy tại [localhost:8501](http://localhost:8501). Chưa có URL công khai cho bản tích hợp.
- Khi demo từ máy khác, có thể mở tunnel bằng `cloudflared tunnel --url http://localhost:8501` và cập nhật URL đang hoạt động tại đây.

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin, hoặc xin xác nhận yes/no trước khi hành động | không |
| timeline | lấy các bài đăng gần đây của một tài khoản (handle không có `@`) | không |
| social_search | tìm bài đăng theo từ khóa (`Latest` hoặc `Top`) | không |
| lookup | tìm thông tin/tin tức trên web (`topic` general/news, `timeframe`) | không |
| fetch | đọc nội dung một URL | không |
| format | trình bày các item đã có thành bản tin markdown | không |
| **dedupe** | loại item trùng khỏi danh sách đã thu thập, theo URL hoặc tiêu đề | **có** |
| send | gửi văn bản lên Telegram, chỉ khi người dùng đã xác nhận (`confirmed=true`) | không |
| policy | tìm trong chính sách nội bộ của công ty | không |
| papers | tìm bài báo trên arXiv | không |
| paper_text | đọc nội dung text của một bài báo arXiv | không |

### A3. Câu hỏi mẫu để thử

1. `Tin AI nổi bật trong tuần này có gì?` (tìm tin trên web)
2. `Tweet mới nhất của Sam Altman là gì?` (xem bài đăng của một tài khoản)
3. `Tóm tắt 5 tweet mới nhất giúp mình` (thiếu thông tin: agent nên hỏi lại tài khoản nào, rồi trả lời tiếp `Của Sam Altman nhé`)
4. `Lọc trùng giúp mình theo URL: 1) 'OpenAI ra mô hình mới' - https://openai.com/blog/x?utm_source=tw 2) 'OpenAI ra mô hình mới' - https://www.openai.com/blog/x/ 3) 'Claude cập nhật' - https://anthropic.com/news/claude` (tool mới `dedupe`: giữ 2 item)
5. `Đăng bản tin này lên Telegram giúp mình` (agent phải hỏi xác nhận trước, không gửi ngay)

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- **v1** thay việc đoán tài khoản hoặc URL bằng quy tắc hỏi lại.
- **v2** thêm quy tắc xác nhận trước khi gửi.
- **v3** nêu rõ cách chọn tool, xử lý thông tin thiếu, giới hạn phạm vi và yêu cầu gửi.
- **v3-integrated** dùng prompt v3 với `tools.yaml` từ `datvu`. Bản này có mô tả cách dùng từng tool, quy ước tham số, tool mới `dedupe`, bộ eval nhóm và UI Streamlit.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | Baseline, chưa sửa prompt/tool declaration | Đo hiện trạng để tìm lỗi routing và boundary. | N/A | 0.70 (14/20) | [run v0](../../starter_v0/runs/v0_B_base_openrouter_20261110T180028666992.json) |
| v1 | `artifacts/system_prompt.md`: hỏi lại khi thiếu account/URL | R10 và R11 sẽ cải thiện nếu cấm đoán account/URL và yêu cầu `clarify(response_type="text")`. | 0.70 (14/20) | 0.85 (17/20) | [run v1](../../starter_v0/runs/v1_B_base_openrouter_20261110T182153182485.json) |
| v2 | `artifacts/system_prompt.md`: hỏi xác nhận trước khi gửi/đăng | R12 sẽ PASS nếu agent hỏi `clarify(response_type="yes_no")` thay vì gọi `send` ngay. Thực tế R12 vẫn FAIL: agent hỏi về nội dung với `response_type="text"`; M02 cũng chuyển từ PASS thành FAIL. | 0.85 (17/20) | 0.85 (17/20) | [run v2](../../starter_v0/runs/v2_B_base_openrouter_20261110T191037734610.json) |
| v3 | `artifacts/system_prompt.md`: prompt có mục routing, thiếu thông tin, ngoài phạm vi và gửi/đăng | Quy tắc routing rõ hơn sẽ tăng case accuracy và tool routing accuracy. R01 và M02 chuyển sang PASS; R12 vẫn dùng `clarify(response_type="text")`, M06 gọi thừa `social_search`. | 0.85 (17/20) | 0.90 (18/20) | [run v3](../../starter_v0/runs/v3_B_base_openrouter_20261110T192900085847.json) |
| v3-integrated | `artifacts/tools.yaml` và đăng ký tool từ `datvu` | Đo cấu hình cuối có `dedupe`. R12 và M06 vẫn sai. R01 chuyển từ PASS sang FAIL vì agent hỏi lại handle thay vì gọi `timeline`. | 0.90 (18/20) | 0.85 (17/20) | [run base tích hợp](../../starter_v0/runs/v3-integrated_B_base_openrouter_20261110T195722964347.json) |

Lưu ý về v3: prompt do nhóm đề xuất thay nhiều quy tắc cùng lúc, nên run này cho thấy hiệu quả của **toàn bộ prompt v3**, không tách được tác động của từng quy tắc. Ở R12, mục "Missing information" yêu cầu hỏi `response_type=text` khi chưa rõ nội dung gửi, trong khi mục "Sending" yêu cầu hành động đầu tiên là `response_type=yes_no`; hai chỉ dẫn này cần được làm rõ ở vòng tiếp theo.

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

Bộ eval nhóm gồm 5 case một lượt và 5 case nhiều lượt. Bản tích hợp đạt **8/10**, `multiturn_accuracy = 0.60`, 0 lỗi provider. [Run group tích hợp](../../starter_v0/runs/v3-integrated_B_group_openrouter_20261110T195758371581.json).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_dedupe_by_url | Lọc trùng danh sách đã có | `dedupe(key="url")` | PASS |
| G02_out_of_scope_translate | Yêu cầu dịch ngoài phạm vi | Không gọi tool | PASS |
| G03_handle_without_at | Bỏ `@` và giữ số lượng bài | `timeline(screenname="karpathy", limit=4)` | PASS |
| G04_org_mention_is_social_search | Tìm bài nhắc đến tổ chức | `social_search(query="Anthropic", search_type="Latest")` | PASS |
| G05_thanks_no_tool | Kết thúc hội thoại | Không gọi tool | PASS |
| G06_send_after_confirmation | Chọn action sau khi có xác nhận | `send(confirmed=true)` | PASS về tool call. Telegram được tắt trong tiến trình eval nên không có tin thật. |
| G07_dedupe_title_carryover | Đổi tiêu chí sang tiêu đề qua nhiều lượt | `dedupe(key="title")` | FAIL. Gọi `fetch` cho ba URL thay vì dùng các mục đã có. |
| G08_social_search_carryover | Giữ chủ đề, kiểu sắp xếp và số lượng qua nhiều lượt | `social_search(query="Claude", search_type="Top", limit=3)` | PASS |
| G09_out_of_scope_after_research | Đổi từ tra cứu sang giải toán | Không gọi tool | PASS |
| G10_still_vague_keeps_asking | Hỏi lại khi vẫn chưa có tài khoản | `clarify(response_type="text")` | FAIL. Tự dùng `timeline(screenname="techceo", limit=5)`. |

### B4. Live Chat Evidence

Phiên chạy `chat.py` với OpenRouter trên bản tích hợp. [Transcript CLI](../../starter_v0/transcripts/v3-integrated_openrouter_20261110T195720576802.transcript.json).

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Lọc ba mục theo URL | `dedupe(key="url")` | v3-integrated | Giữ hai mục và trả kết quả. |
| 2 | Tóm tắt 5 tweet, chưa nêu tài khoản | Không có tool call | v3-integrated | Hỏi lại bằng văn bản. |
| 3 | Bổ sung tên Sam Altman | `timeline(screenname="sama", limit=5)` | v3-integrated | Lấy và tóm tắt 5 bài. |
| 4 | Yêu cầu đăng bản tin vừa rồi lên Telegram | `clarify(response_type="yes_no")` | v3-integrated | Dừng chờ xác nhận. |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/dedupe/tool.py`, `starter_v0/tools/dedupe/TOOL.md`; đăng ký trong `starter_v0/tools/__init__.py` và `starter_v0/artifacts/tools.yaml` | `dedupe` loại item trùng khỏi danh sách đã thu thập (theo `url` hoặc `title`), giữ item đầu tiên và giữ thứ tự. Coi cùng một trang nếu chỉ khác scheme, `www.`, `#fragment`, dấu `/` cuối, hoa thường của host hoặc tham số `utm_*`. Tool thuần local, không gọi API | Item không có `url`/`title` không so sánh được nên luôn được giữ lại (không gộp nhầm). Input xấu (`key` ngoài enum, `items` không phải list) trả error dict chứ không raise, để vòng lặp agent không bị dừng |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py` (8 test `test_dedupe_*`); `pytest`: 75 passed, 14 skipped, 0 failed; `pytest tests/test_tool_contract.py`: 60 passed | Happy path (biến thể URL, `key=title`), biên (thiếu key, rỗng/None, entry không phải dict), nhánh lỗi (key ngoài enum, items sai kiểu) | Test chạy offline, không gọi mạng; 14 test skipped còn lại là stub TODO của tool có sẵn (challenge bonus) |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py`, `streamlit run app.py` (xem A1). [Transcript UI tích hợp](../../starter_v0/transcripts/v3-integrated-ui_openrouter_20261110T195955316752.transcript.json) | Máy chủ Streamlit trả HTTP 200 ở health endpoint. Một lượt chat thật bằng `streamlit.testing` gọi `dedupe` và giữ đúng 2 mục. | UI đã kiểm tra cục bộ. Giới hạn 20 lượt mỗi cuộc trò chuyện. |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

- Số test: 8 test cho `dedupe`.
- Loại lỗi mà unit test kiểm tra được nhưng eval không thấy: nếu `dedupe` chuẩn hóa URL quá tay (ví dụ bỏ luôn mọi query param) thì `https://example.com/watch?v=1` và `...?v=2` bị gộp nhầm. Model vẫn gọi đúng `dedupe(items=..., key="url")` nên eval vẫn báo PASS, chỉ có `test_dedupe_url_keeps_pages_that_differ_only_by_real_query_param` mới phát hiện. Lưu ý: đây là test phòng ngừa đã viết trước khi có lỗi, chưa có lỗi thật nào được test bắt trong lúc viết tool này.

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

- Hai nhánh có lịch sử eval khác nhau. Nhóm giữ chuỗi v0–v3 đã chốt và dùng nhãn `v3-integrated` cho cấu hình cuối để mỗi điểm số trỏ tới đúng hash.
- Kiểm thử UI trên Windows phát hiện `UnicodeEncodeError` khi vòng lặp chat in emoji trong log. Log tool call chuyển sang ASCII, còn văn bản tiếng Việt trong UI và transcript vẫn dùng Unicode. Chạy lại mẫu `dedupe` thành công (B5a).
- Sau khi ghép bộ tool, base eval giảm một case do R01 hỏi lại handle. Group eval còn lỗi ở G07 và G10. Chi tiết ở B1 và B3.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

Các run và transcript trên nhánh `datvu` vẫn có trong repo để đối chiếu với báo cáo cá nhân. Bảng B1–B4 của báo cáo nhóm dùng chuỗi v0–v3 đã chốt và bằng chứng mới của bản tích hợp.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- `system_prompt.md` kiểm soát thời điểm hỏi lại, phạm vi và xác nhận. R12 cho thấy cần quy định rõ thứ tự giữa hỏi nội dung và xin xác nhận.
- `tools.yaml` mô tả điều kiện dùng tool và quy ước tham số. Việc thêm tool thay đổi các lựa chọn model thấy, nên nhóm chạy lại cả base lẫn group sau tích hợp.
- Cần xem transcript song song với điểm eval. Ở lượt 2, agent hỏi đúng thông tin bằng văn bản. Harness sẽ tính thiếu tool nếu case yêu cầu một tool call cụ thể.
- Vòng sau có thể kiểm tra riêng giả thuyết rằng yêu cầu mới nhất thu hẹp nguồn tìm kiếm sẽ ngăn M06 gọi thừa `social_search`.

## 8. Tài liệu tham khảo

- Đề bài lab: `README.md`, `RULES.md`, `CHECKPOINTS.md`, `RUBRIC.md`, `SUBMISSION.md` ở thư mục gốc.
- Hướng dẫn cấu hình key: `docs/TOOL-SETUP.md`.
- Streamlit: https://docs.streamlit.io
- Cloudflare Tunnel: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
