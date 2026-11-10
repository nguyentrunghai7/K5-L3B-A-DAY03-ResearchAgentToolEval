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

UI là `starter_v0/app.py` (Streamlit). UI hiển thị mọi tool call và kết quả của nó (kể cả lỗi) và ghi transcript vào `starter_v0/transcripts/`. Giới hạn 20 lượt cho mỗi cuộc trò chuyện. Tool `send` chưa cấu hình Telegram nên không gửi thật.

**Link dùng thử (deploy):**

> URL: https://incidents-burner-equilibrium-standing.trycloudflare.com
>
> Mở bằng Cloudflare Tunnel (`cloudflared tunnel --url http://localhost:8501`). Đây là link tạm: chỉ hoạt động khi máy chạy UI và cửa sổ `cloudflared` còn mở.

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

- `system_prompt.md` (v1): bỏ 3 chỉ dẫn xấu của starter (đoán thay vì hỏi, gửi không cần xác nhận, ép một bước) và thay bằng: hỏi lại bằng `clarify` khi thiếu thông tin, không gọi tool với câu ngoài phạm vi, xác nhận trước khi gửi.
- `tools.yaml` (v2): viết lại description của mọi tool (làm gì, khi nào dùng, khi nào không dùng) và convention args: `response_type` của `clarify`, `topic=news` và `query` không chứa chữ "news" của `lookup`, handle không có `@`, `search_type` Top/Latest, ranh giới `confirmed=true` của `send`.
- `system_prompt.md` (v3): thêm rule routing và ranh giới xác nhận tường minh. Kết quả không tốt hơn v2 (xem B1).
- Tool mới `dedupe` (`starter_v0/tools/dedupe/`): loại item trùng theo URL (bỏ qua `www.`, dấu `/` cuối, `#fragment`, `utm_*`) hoặc theo tiêu đề. Agent nên gọi khi người dùng muốn bỏ trùng, hoặc trước `format` khi danh sách gộp từ nhiều nguồn. Không dùng khi chưa có danh sách item.
- UI Streamlit `starter_v0/app.py` dùng lại vòng lặp của `chat.py`.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi chưa tối ưu trước khi sửa | - | 0.70 | `runs/v0_B_base_openrouter_20261110T174924785097.json` |
| v1 | `system_prompt.md` | Các chỉ dẫn xấu trong prompt (đoán thay vì hỏi, gửi ngay không xác nhận, ép một bước) gây ra `missing_info`, `wrong_boundary`, `out_of_scope`; bỏ chúng thì agent hỏi lại, từ chối câu ngoài phạm vi và không gọi `send` ngay. Kết quả: đúng một phần. Routing đạt 1.0, 4 case còn FAIL đều do sai args (`response_type`, `topic`) | 0.70 | 0.80 | `runs/v1_B_base_openrouter_20261110T180650937286.json` |
| v2 | `tools.yaml` | Description và convention args quá mơ hồ nên model bỏ `response_type`, bỏ `topic=news` và nhét chữ "news" vào `query`; mô tả rõ khi nào dùng/không dùng và convention args thì args đúng. Kết quả: đúng, sửa được R10, R11, R13; còn R12 | 0.80 | 0.95 | `runs/v2_B_base_openrouter_20261110T180948507851.json` |
| v3 | `system_prompt.md` | Prompt chưa có rule routing và ranh giới xác nhận tường minh nên model xin nội dung (`text`) thay vì xin xác nhận (`yes_no`) khi được yêu cầu gửi. Kết quả: **sai**. R12 vẫn FAIL vì rule `yes_no` mâu thuẫn với rule "thiếu thông tin thì hỏi `text`"; M06 mới FAIL vì câu "cần hai nguồn thì gọi cả hai" bị áp dụng quá rộng (gọi thừa `social_search` dù user đã nói bỏ Twitter) | 0.95 | 0.90 | `runs/v3_B_base_openrouter_20261110T181141015905.json` |

Metric là `case_accuracy` của base eval (20 case). Cả 4 run đều hợp lệ (`provider_error_cases = 0`, `measured_cases = total_cases = 20`). Chi tiết hash prompt/tools: `starter_v0/artifacts/version_log.csv`.

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

Run v0: `starter_v0/runs/v0_B_base_openrouter_20261110T174924785097.json` (model `openai/gpt-4o-mini`, 14/20 pass, `provider_error_cases = 0`, `measured_cases = total_cases = 20`).

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R08_out_of_scope | out_of_scope | `send(text="Nguyên hàm của x^2 là ...")` | Câu hỏi toán ngoài phạm vi research, lẽ ra không gọi tool. Agent vẫn gọi `send` để gửi câu trả lời. Nguyên nhân: prompt v0 bảo "cứ gửi luôn, không cần chờ" và không có rule nào về phạm vi. | `system_prompt.md`: thêm phạm vi của agent (chỉ research/tin tức/đọc URL), câu ngoài phạm vi thì từ chối, không gọi tool. |
| R10_missing_handle | missing_info | `timeline(screenname="sama")` | User không nói tài khoản nào, lẽ ra phải `clarify`. Agent tự đoán Sam Altman. Nguyên nhân: prompt v0 bảo "chọn một tài khoản nổi tiếng như Sam Altman". | `system_prompt.md`: bỏ chỉ dẫn đoán, thêm rule thiếu handle thì gọi `clarify`. |
| R11_missing_url | missing_info | `fetch(url="https://example.com/article")` | User nói "bài viết này" nhưng không có link, lẽ ra phải `clarify`. Agent bịa URL. Nguyên nhân: prompt v0 bảo "đoán URL rồi đọc". | `system_prompt.md`: bỏ chỉ dẫn đoán URL, thiếu URL thì gọi `clarify`. |
| R12_confirm_before_send | wrong_boundary | `send(text="Bản tin này")` | Yêu cầu hành động ghi (đăng Telegram), lẽ ra `clarify(response_type=yes_no)` để xác nhận trước. Agent gọi `send` ngay, không có `confirmed=true`. Nguyên nhân: prompt v0 bảo "cứ làm luôn"; `tools.yaml` mô tả `send` mơ hồ, không nêu ranh giới xác nhận. | `system_prompt.md` + `tools.yaml`: `send` chỉ gọi sau khi user xác nhận rõ nội dung, nếu chưa thì `clarify` yes_no trước. |
| R13_parallel_web_and_tweets | wrong_tool (nhãn của harness) | `lookup(query="AI news", timeframe="day", max_results=5)` + `social_search(query="AI", search_type="Latest", limit=5)` | Chọn đúng cả 2 tool (`routing_correct = True`) nhưng sai args của `lookup`: `query` là "AI news" thay vì "AI", và thiếu `topic="news"`. Thực chất là `wrong_arg_value`. Nguyên nhân: `tools.yaml` không nêu convention "tin tức thì `topic=news`". Ngoài ra lần gọi `lookup` này gặp `ConnectionError` mạng, không ảnh hưởng kết quả chấm vì lỗi nằm ở args. | `tools.yaml`: mô tả `lookup` rõ tin tức thì dùng `topic=news`, `query` chỉ chứa từ khóa chủ đề. |
| R14_out_of_scope_coding | out_of_scope | `send(text="Dưới đây là một hàm Python tính Fibonacci ...")` | Câu hỏi viết code ngoài phạm vi, lẽ ra không gọi tool. Agent vẫn gọi `send`. Nguyên nhân giống R08. | `system_prompt.md`: như R08. |

Nhận xét: 6 case FAIL đều bắt nguồn từ các chỉ dẫn xấu cố ý trong `system_prompt.md` v0 (đoán thay vì hỏi, gửi không cần xác nhận, ép một bước) và từ `tools.yaml` chưa nêu convention args. Cả 6 case chưa được sửa ở v0, việc sửa thuộc CP2.

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

Run: `starter_v0/runs/v3_B_group_openrouter_20261110T182350557552.json` (nhãn `v3`, model `openai/gpt-4o-mini`, `provider_error_cases = 0`, `measured_cases = total_cases = 10`). Kết quả: 8/10 pass, `case_accuracy = 0.8`, `multiturn_accuracy = 0.6`. Lưu ý: nhãn `v3` nhưng `tools_hash` khác run base v3 (`t39c1b29ad6f5` so với `t96acff6e39bf`) vì đã thêm tool `dedupe` ở CP3.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_dedupe_by_url (single) | Route tới tool mới `dedupe`: danh sách có link lặp, yêu cầu lọc theo URL | `dedupe(key=url)` | PASS |
| G02_out_of_scope_translate (single) | Yêu cầu dịch thuật ngoài phạm vi research | `no_tool`, từ chối | PASS |
| G03_handle_without_at (single) | Convention handle: `@karpathy` phải thành `karpathy`, `limit=4` | `timeline(screenname=karpathy, limit=4)` | PASS |
| G04_org_mention_is_social_search (single) | Tweet nhắc đến một tổ chức là tìm theo từ khóa, không phải xem timeline của tổ chức | `social_search(query=Anthropic, search_type=Latest)` | PASS |
| G05_thanks_no_tool (single) | Câu cảm ơn/kết thúc không cần tool | `no_tool` | PASS |
| G06_send_after_confirmation (multi) | Sau khi user đã xác nhận rõ ở lượt cuối thì phải gửi thật | `send(confirmed=true)` | PASS |
| G07_dedupe_title_carryover (multi) | `dedupe` qua nhiều lượt: lượt cuối đổi tiêu chí sang tiêu đề | `dedupe(key=title)` | **FAIL** (`extra_tool_call`): gọi đúng `dedupe(key=title)` nhưng gọi thừa `format` mà user không yêu cầu |
| G08_social_search_carryover (multi) | Gộp 3 thông tin từ 3 lượt: query, search_type=Top, limit=3 | `social_search(query=Claude, search_type=Top, limit=3)` | PASS |
| G09_out_of_scope_after_research (multi) | Đang research nhưng lượt cuối đổi sang giải toán | `no_tool`, từ chối | PASS |
| G10_still_vague_keeps_asking (multi) | Sau 3 lượt user vẫn chưa nêu tài khoản cụ thể (chỉ nói "một CEO công nghệ") thì phải tiếp tục hỏi, không tự chọn | `clarify(response_type=text)` | **FAIL** (`missing_tool_call`): gọi `timeline(screenname=tech_ceo, limit=5)`, tự bịa tài khoản |

Nhận xét: 2 case FAIL đều có ích. G10 chỉ ra lỗi thật của prompt v3 (vẫn đoán khi user mơ hồ qua nhiều lượt). G07 cho thấy tool mới được route đúng và truyền đúng `key`; lỗi chỉ là gọi thêm `format` ngoài yêu cầu.

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

Hai phiên `chat.py --provider openrouter --version v3`. Cả hai transcript có `artifact_version = v3+pa9083eb83825+t39c1b29ad6f5`. Các câu hỏi do nhóm nhập sẵn rồi chạy qua `chat.py` (model và tool đều là thật, không có phần nào giả lập).

**Phiên 1:** `starter_v0/transcripts/v3_openrouter_20261110T184429774316.transcript.json`

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Tin AI nổi bật trong tuần này có gì? | `lookup(query=AI, topic=news, timeframe=week)` + `social_search(query=AI, search_type=Top)` | v3 | Đúng: yêu cầu thường, gọi 2 nguồn và tổng hợp có nguồn |
| 2 | Tóm tắt 5 tweet mới nhất giúp mình | `timeline(screenname=ai_with_jyoti, limit=5)` | v3 | **SAI**: user chưa nói tài khoản nào, agent lẽ ra phải `clarify` nhưng tự lấy tài khoản `ai_with_jyoti` từ tweet đã thấy ở turn 1 |
| 3 | Của Sam Altman nhé | `timeline(screenname=sama, limit=5)` | v3 | Đúng: map tên thành handle `sama`, giữ `limit=5` |
| 4 | Đăng bản tin này lên Telegram giúp mình | `clarify(response_type=yes_no)` | v3 | Đúng: hỏi xác nhận, không gọi `send` |

**Phiên 2:** `starter_v0/transcripts/v3_openrouter_20261110T184540669868.transcript.json`

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Cho mình xem tweet gần đây | (không gọi tool, hỏi lại bằng văn bản: "tài khoản Twitter nào?") | v3 | Đúng về hành vi: hỏi lại thay vì đoán. Lưu ý: model hỏi bằng text chứ không gọi tool `clarify` |
| 2 | Của Sam Altman nhé, lấy 3 bài | `timeline(screenname=sama, limit=3)` | v3 | Đúng: bổ sung thông tin xong thì gọi tool, đúng `limit=3` |
| 3 | Đăng bản tin vừa rồi lên Telegram giúp mình | `clarify(response_type=yes_no)` | v3 | Đúng: xin xác nhận trước khi gửi |

Nhận xét: turn 2 của phiên 1 là lỗi thật khi chat live, cùng loại với case G10 (B3). Ở eval base R10 (`Tóm tắt 5 tweet mới nhất giúp mình`, đứng một mình) v3 đã PASS, nhưng khi trước đó đã có tweet trong hội thoại thì agent lại đoán. Eval single turn không bắt được lỗi này.

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | `starter_v0/tools/dedupe/tool.py`, `starter_v0/tools/dedupe/TOOL.md`; đăng ký trong `starter_v0/tools/__init__.py` và `starter_v0/artifacts/tools.yaml` | `dedupe` loại item trùng khỏi danh sách đã thu thập (theo `url` hoặc `title`), giữ item đầu tiên và giữ thứ tự. Coi cùng một trang nếu chỉ khác scheme, `www.`, `#fragment`, dấu `/` cuối, hoa thường của host hoặc tham số `utm_*`. Tool thuần local, không gọi API | Item không có `url`/`title` không so sánh được nên luôn được giữ lại (không gộp nhầm). Input xấu (`key` ngoài enum, `items` không phải list) trả error dict chứ không raise, để vòng lặp agent không bị dừng |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py` (8 test `test_dedupe_*`); `pytest`: 75 passed, 14 skipped, 0 failed; `pytest tests/test_tool_contract.py`: 60 passed | Happy path (biến thể URL, `key=title`), biên (thiếu key, rỗng/None, entry không phải dict), nhánh lỗi (key ngoài enum, items sai kiểu) | Test chạy offline, không gọi mạng; 14 test skipped còn lại là stub TODO của tool có sẵn (challenge bonus) |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py`; lệnh chạy: `streamlit run app.py` (xem A1); transcript `starter_v0/transcripts/v3_openrouter_20261110T184429774316.transcript.json`, `v3_openrouter_20261110T184540669868.transcript.json` | UI chạy được ở `http://localhost:8501` (kiểm tra health check `ok` và một lượt chat thật bằng `streamlit.testing`). Hiển thị mọi tool call và kết quả, kể cả lỗi (mở sẵn khung lỗi), ghi transcript mỗi lượt | Link public (`trycloudflare.com`, xem A1) là link tạm, mất khi tắt `cloudflared` hoặc tắt máy; đã kiểm tra mở được từ bên ngoài (HTTP 200, health `ok`) nhưng chưa có người ngoài nhóm thử câu hỏi mẫu. Giới hạn 20 lượt mỗi cuộc trò chuyện để không đốt hết credit API khi mở link. Tool `send` chưa cấu hình Telegram nên không gửi thật |

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

- **RapidAPI trả 403 Forbidden** khi smoke test `timeline` và `social_search`, trong khi key đã có giá trị. Nguyên nhân là chưa Subscribe vào API `twitter-api45`. Sau khi subscribe thì cả hai tool chạy được. Nếu không xử lý, run v0 sẽ có lỗi tool ở các case dùng tweet.
- **Mất mạng giữa chừng khi chạy v1**: lần chạy đầu của v1 có 16/20 case `provider_error` (`measured_cases = 4`), nên run này không hợp lệ theo RUBRIC. Nhóm xóa file run lỗi đó và chạy lại v1 sau khi có mạng; run dùng làm bằng chứng là `runs/v1_B_base_openrouter_20261110T180650937286.json` (`provider_error_cases = 0`).
- **Lỗi mạng thoáng qua trong run v0**: case R13 có một lần `lookup` báo `ConnectionError`. Lỗi chấm của R13 nằm ở args (`topic`, `query`), không phải lỗi này, và run vẫn hợp lệ (`provider_error_cases = 0`).
- **v3 làm kết quả xấu đi** (0.95 xuống 0.90): rule mới mâu thuẫn với rule cũ và câu "cần hai nguồn thì gọi cả hai" bị áp dụng quá rộng. Nhóm ghi đúng kết quả này vào B1 thay vì chọn run đẹp hơn.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?** Hành vi và ranh giới: hỏi lại khi thiếu thông tin, từ chối câu ngoài phạm vi, xác nhận trước khi gửi. v1 sửa các việc này: `case_accuracy` 0.70 lên 0.80, `tool_routing_accuracy` 0.75 lên 1.0 (B1).
- **Fix nào thuộc `tools.yaml`?** Quy ước args và khi nào dùng tool: `response_type` của `clarify`, `topic=news` và `query` của `lookup`, handle không có `@`. v2 sửa các việc này: 0.80 lên 0.95 (B1). Một args mà model không biết đến thì prompt không sửa được, phải mô tả ở declaration.
- **Failure nào cần review thủ công thay vì chấm tự động?** (1) G07 (B3): agent gọi đúng `dedupe(key=title)` rồi gọi thêm `format` mà user không yêu cầu; chấm tự động báo FAIL vì "extra tool call", nhưng đây là hành vi cần người đánh giá có chấp nhận được hay không. (2) Live chat turn 2 phiên 1 (B4): R10 đã PASS khi đứng một mình nhưng agent vẫn đoán tài khoản khi trong hội thoại có sẵn tweet. Chấm tự động trên từng case đơn lẻ không thấy lỗi phụ thuộc ngữ cảnh này. (3) Phiên 2 turn 1: agent hỏi lại bằng text chứ không gọi `clarify`; hành vi đúng nhưng nếu chấm theo tool thì bị tính là sai.
- **Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?** v4 (sửa `system_prompt.md`): chỉ dùng tài khoản do chính người dùng nêu, tuyệt đối không lấy tài khoản từ kết quả tool trước hay tự bịa (sửa G10 và live turn 2); bỏ câu "gọi cả hai nguồn" ở v3 hoặc giới hạn nó (sửa M06); và chỉ gọi `format` khi người dùng yêu cầu soạn bản tin (sửa G07). Mỗi thay đổi cần một version riêng để biết thay đổi nào có tác dụng.

## 8. Tài liệu tham khảo

- Đề bài lab: `README.md`, `RULES.md`, `CHECKPOINTS.md`, `RUBRIC.md`, `SUBMISSION.md` ở thư mục gốc.
- Hướng dẫn cấu hình key: `docs/TOOL-SETUP.md`.
- Streamlit: https://docs.streamlit.io
- Cloudflare Tunnel: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
