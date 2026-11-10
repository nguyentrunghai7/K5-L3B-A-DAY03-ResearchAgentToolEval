"""Streamlit UI cho Research Agent.

Chạy (từ starter_v0/):  streamlit run app.py
UI dùng đúng vòng lặp model -> tool của chat.py, hiển thị MỌI tool call và kết quả
(kể cả lỗi) và ghi transcript vào transcripts/*.transcript.json.
"""
from __future__ import annotations

import json
from datetime import datetime
from typing import Any

import streamlit as st

from chat import (
    ARTIFACTS_DIR,
    ROOT,
    now_iso,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

PROVIDER = "openrouter"
VERSION = "v3-ui"
HISTORY_WINDOW = 5
MAX_TOOL_ROUNDS = 4
MAX_TURNS_PER_SESSION = 20  # giới hạn để link public không đốt hết credit API

SAMPLES = [
    "Tin AI nổi bật trong tuần này có gì?",
    "Tweet mới nhất của Sam Altman là gì?",
    "Tóm tắt 5 tweet mới nhất giúp mình",
    "Lọc trùng giúp mình theo URL: 1) 'OpenAI ra mô hình mới' - https://openai.com/blog/x?utm_source=tw 2) 'OpenAI ra mô hình mới' - https://www.openai.com/blog/x/ 3) 'Claude cập nhật' - https://anthropic.com/news/claude",
    "Đăng bản tin này lên Telegram giúp mình",
]

st.set_page_config(page_title="Research Agent", page_icon="🔎", layout="wide")


@st.cache_resource
def load_agent_config() -> dict[str, Any]:
    prompt_path = ARTIFACTS_DIR / "system_prompt.md"
    tools_path = ARTIFACTS_DIR / "tools.yaml"
    declarations = load_tool_declarations(tools_path)
    provider = make_provider(PROVIDER)
    return {
        "system_prompt": prompt_path.read_text(encoding="utf-8"),
        "declarations": declarations,
        "openai_tools": to_openai_tools(declarations),
        "provider": provider,
        "model": getattr(provider, "default_model", None),
        "artifact_version": build_artifact_version(VERSION, prompt_path, tools_path),
        "prompt_path": prompt_path,
        "tools_path": tools_path,
    }


def new_session(config: dict[str, Any]) -> None:
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join([safe_slug(VERSION), safe_slug(PROVIDER), timestamp])
    st.session_state.transcript_path = ROOT / "transcripts" / f"{transcript_id}.transcript.json"
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(config["artifact_version"]),
        "provider": PROVIDER,
        "model": config["model"],
        "system_prompt": str(config["prompt_path"]),
        "tools": str(config["tools_path"]),
        "history_window": HISTORY_WINDOW,
        "max_tool_rounds": MAX_TOOL_ROUNDS,
        "source": "streamlit_ui",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }
    st.session_state.history = []  # lịch sử gửi cho model
    st.session_state.messages = []  # lịch sử để hiển thị
    st.session_state.turn_index = 0


def render_events(events: list[dict[str, Any]]) -> None:
    for event in events:
        args = json.dumps(event.get("args", {}), ensure_ascii=False)
        result = event.get("result", {})
        failed = isinstance(result, dict) and result.get("error")
        label = f"{'❌' if failed else '🔧'} {event.get('tool')}({args[:120]}{'…' if len(args) > 120 else ''})"
        with st.expander(label, expanded=bool(failed)):
            if failed:
                st.error(f"{result.get('error')}: {result.get('message', '')}")
            text = json.dumps(result, ensure_ascii=False, indent=2, default=str)
            st.code(text[:4000] + ("\n...<truncated>" if len(text) > 4000 else ""), language="json")


def render_message(message: dict[str, Any]) -> None:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            if message.get("events"):
                render_events(message["events"])
            if message.get("status") == "waiting_for_user":
                st.caption("🙋 Agent hỏi lại bạn, hãy trả lời ở ô bên dưới")
            if message.get("status") == "provider_error":
                st.error(message["content"])
                return
        st.markdown(message["content"])


config = load_agent_config()
if "transcript" not in st.session_state:
    new_session(config)

# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("🔎 Research Agent")
    st.caption(f"Model: `{config['model']}`  \nPhiên bản: `{config['artifact_version'].artifact_version}`")
    st.subheader("Tool của agent")
    for tool in config["declarations"]:
        st.markdown(f"- **{tool['name']}**")
    st.subheader("Câu hỏi mẫu")
    for index, sample in enumerate(SAMPLES):
        if st.button(sample[:60] + ("…" if len(sample) > 60 else ""), key=f"sample_{index}", use_container_width=True):
            st.session_state.pending = sample
    st.divider()
    st.caption("Lưu ý: tool `send` (Telegram) chưa được cấu hình nên sẽ không gửi thật.")
    if st.button("🗑️ Cuộc trò chuyện mới", use_container_width=True):
        new_session(config)
        st.rerun()

st.title("Research Agent")
st.caption("Tìm tin trên web, đọc URL, xem tweet, lọc trùng. Agent sẽ hỏi lại khi thiếu thông tin và xin xác nhận trước khi gửi.")

for message in st.session_state.messages:
    render_message(message)

prompt = st.chat_input("Nhập yêu cầu…") or st.session_state.pop("pending", None)

if prompt:
    if st.session_state.turn_index >= MAX_TURNS_PER_SESSION:
        st.warning(f"Đã đạt giới hạn {MAX_TURNS_PER_SESSION} lượt cho một cuộc trò chuyện. Bấm 'Cuộc trò chuyện mới' ở thanh bên.")
        st.stop()

    user_message = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_message)
    render_message(user_message)

    st.session_state.turn_index += 1
    turn_record: dict[str, Any] = {
        "turn_index": st.session_state.turn_index,
        "started_at": now_iso(),
        "user": prompt,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }
    messages = [
        {"role": "system", "content": config["system_prompt"]},
        *trim_history(st.session_state.history, HISTORY_WINDOW),
        {"role": "user", "content": prompt},
    ]

    with st.chat_message("assistant"):
        with st.spinner("Agent đang xử lý…"):
            try:
                result = run_model_tool_loop(
                    provider=config["provider"],
                    messages=messages,
                    tools=config["openai_tools"],
                    model=None,
                    max_tool_rounds=MAX_TOOL_ROUNDS,
                )
                turn_record.update(result)
                reply = {
                    "role": "assistant",
                    "content": result["assistant_text"],
                    "events": result["tool_events"],
                    "status": result["status"],
                }
                st.session_state.history.append({"role": "user", "content": prompt})
                st.session_state.history.append({"role": "assistant", "content": result["assistant_text"]})
            except Exception as exc:  # hiển thị lỗi thật, không che giấu
                error = f"{type(exc).__name__}: {exc}"
                turn_record.update({"status": "provider_error", "error": error})
                reply = {"role": "assistant", "content": error, "events": [], "status": "provider_error"}

    turn_record["ended_at"] = now_iso()
    st.session_state.transcript["turns"].append(turn_record)
    write_transcript(st.session_state.transcript_path, st.session_state.transcript)
    st.session_state.messages.append(reply)
    st.rerun()
