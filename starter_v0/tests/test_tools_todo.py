"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

# ---- dedupe (tool mới của nhóm) ----

dedupe_tool = TOOL_FUNCTIONS["dedupe"]


def test_dedupe_url_treats_same_page_variants_as_duplicates_and_keeps_first() -> None:
    items = [
        {"title": "A", "url": "https://www.example.com/post/"},
        {"title": "B", "url": "http://example.com/post?utm_source=x&utm_medium=y#top"},
        {"title": "C", "url": "https://EXAMPLE.com/other"},
        {"title": "D", "url": "https://example.com/post"},
    ]
    result = dedupe_tool(items=items)

    assert [i["title"] for i in result["items"]] == ["A", "C"]
    assert result["item_count"] == 2
    assert result["removed_count"] == 2
    assert result["key"] == "url"


def test_dedupe_url_keeps_pages_that_differ_only_by_real_query_param() -> None:
    items = [{"url": "https://example.com/watch?v=1"}, {"url": "https://example.com/watch?v=2"}]
    assert dedupe_tool(items=items)["item_count"] == 2


def test_dedupe_by_title_ignores_case_and_extra_whitespace() -> None:
    items = [
        {"title": "OpenAI  releases GPT", "url": "https://a.com/1"},
        {"title": "openai releases gpt", "url": "https://b.com/2"},
        {"title": "Other news", "url": "https://c.com/3"},
    ]
    result = dedupe_tool(items=items, key="title")

    assert [i["url"] for i in result["items"]] == ["https://a.com/1", "https://c.com/3"]
    assert result["removed_count"] == 1


def test_dedupe_keeps_items_missing_the_key_instead_of_merging_them() -> None:
    items = [{"title": "no url 1"}, {"title": "no url 2"}, {"title": "x", "url": ""}, {"title": "y", "url": "  "}]
    result = dedupe_tool(items=items)

    assert result["item_count"] == 4
    assert result["removed_count"] == 0


def test_dedupe_empty_or_none_items_does_not_crash() -> None:
    for empty in (None, []):
        result = dedupe_tool(items=empty)
        assert result["items"] == []
        assert result["item_count"] == 0
        assert "error" not in result


def test_dedupe_skips_non_dict_entries_and_counts_them() -> None:
    result = dedupe_tool(items=[{"url": "https://a.com"}, "oops", 42, None])

    assert result["item_count"] == 1
    assert result["skipped_invalid"] == 3


def test_dedupe_key_outside_enum_returns_error_dict_instead_of_raising() -> None:
    result = dedupe_tool(items=[{"url": "https://a.com"}], key="summary")

    assert result["error"] == "ValueError"
    assert "summary" in result["message"]
    assert "items" not in result


def test_dedupe_items_not_a_list_returns_error_dict_instead_of_raising() -> None:
    for bad in ("https://a.com", {"url": "https://a.com"}, 5):
        result = dedupe_tool(items=bad)
        assert result["error"] == "TypeError"
