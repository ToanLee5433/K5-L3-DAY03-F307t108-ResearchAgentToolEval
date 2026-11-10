"""CP3: Tool Unit Test Suite for All Tools and New Custom Tool.

All tests are completely offline: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
Verified: `pytest tests/` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse
from tools import TOOL_FUNCTIONS


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    clarify_tool = TOOL_FUNCTIONS["clarify"]
    result = clarify_tool(question="Chọn một phương án", response_type="choice", options=["A", "B"])
    assert result["tool"] == "ask_user"
    assert result["options"] == ["A", "B"]
    assert result["awaiting_user"] is True
    assert result["response_type"] == "choice"


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    format_tool = TOOL_FUNCTIONS["format"]
    items = [
        {"title": "Item 1", "section": "Section A", "url": "https://a1.com"},
        {"title": "Item 2", "section": "Section B", "url": "https://b.com"},
        {"title": "Item 3", "section": "Section A", "url": "https://a2.com"},
    ]
    result = format_tool(items=items, template="sections")
    md = result["markdown"]
    assert "## Section A" in md
    assert "## Section B" in md
    assert md.count("## Section A") == 1
    assert md.count("## Section B") == 1


def test_format_thread_numbers_items() -> None:
    format_tool = TOOL_FUNCTIONS["format"]
    items = [
        {"title": "Post 1", "summary": "First post"},
        {"title": "Post 2", "summary": "Second post"},
    ]
    result = format_tool(items=items, template="thread")
    md = result["markdown"]
    assert "1/" in md
    assert "2/" in md


def test_format_empty_items_does_not_crash() -> None:
    format_tool = TOOL_FUNCTIONS["format"]
    res_none = format_tool(items=None)
    res_empty = format_tool(items=[])
    assert res_none["item_count"] == 0
    assert res_empty["item_count"] == 0
    assert isinstance(res_none["markdown"], str)
    assert isinstance(res_empty["markdown"], str)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake_bot_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "123456789")
    calls = fake_http(FakeResponse({"ok": True, "result": {"message_id": 99}}))
    send_tool = TOOL_FUNCTIONS["send"]
    result = send_tool(text="Bản tin công nghệ", confirmed=True)

    assert len(calls) == 1
    assert "fake_bot_token" in calls[0]["url"]
    assert calls[0]["json"]["chat_id"] == "123456789"
    assert calls[0]["json"]["text"] == "Bản tin công nghệ"
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))
    send_tool = TOOL_FUNCTIONS["send"]
    result = send_tool(text="Bản tin", confirmed=True)
    assert result["error"] == "RuntimeError"
    assert "TELEGRAM_BOT_TOKEN" in result["message"]
    assert len(calls) == 0


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))
    lookup_tool = TOOL_FUNCTIONS["lookup"]
    lookup_tool(query="OpenAI", timeframe=None)
    assert "time_range" not in calls[0]["json"]


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-key")
    fake_http(FakeResponse({
        "data": {
            "markdown": "Page markdown text",
            "metadata": {
                "title": "Article Title",
                "sourceURL": "https://example.com/test-article",
            },
        }
    }))
    fetch_tool = TOOL_FUNCTIONS["fetch"]
    result = fetch_tool(url="https://example.com/test-article")
    assert len(result["items"]) == 1
    item = result["items"][0]
    assert item["title"] == "Article Title"
    assert item["url"] == "https://example.com/test-article"
    assert item["source"] == "example.com"
    assert item["summary"] == "Page markdown text"


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-key")
    long_text = "M" * 6000
    fake_http(FakeResponse({
        "data": {
            "markdown": long_text,
            "metadata": {"title": "Long Page", "sourceURL": "https://example.com/long"},
        }
    }))
    fetch_tool = TOOL_FUNCTIONS["fetch"]
    result = fetch_tool(url="https://example.com/long")
    assert len(result["items"][0]["summary"]) == 4000


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "rapid-key")
    fake_http(FakeResponse({
        "timeline": [
            {"text": "Tweet 1", "tweet_id": "101", "screen_name": "sama"},
            {"text": "Tweet no id", "screen_name": "sama"},  # should be skipped
            {"text": "Tweet 2", "tweet_id": "102", "screen_name": "sama"},
            {"text": "Tweet 3", "tweet_id": "103", "screen_name": "sama"},
            {"text": "Tweet 4", "tweet_id": "104", "screen_name": "sama"},
            {"text": "Tweet 5", "tweet_id": "105", "screen_name": "sama"},
        ]
    }))
    timeline_tool = TOOL_FUNCTIONS["timeline"]
    result = timeline_tool(screenname="sama", limit=3)
    assert len(result["items"]) == 3
    assert result["items"][0]["url"] == "https://x.com/sama/status/101"
    assert result["items"][1]["url"] == "https://x.com/sama/status/102"
    assert result["items"][2]["url"] == "https://x.com/sama/status/103"


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "rapid-key")
    calls = fake_http(FakeResponse({"timeline": []}))
    social_tool = TOOL_FUNCTIONS["social_search"]
    social_tool(query="AI Agents", search_type="Top", limit=10)
    assert len(calls) == 1
    assert calls[0]["params"]["query"] == "AI Agents"
    assert calls[0]["params"]["search_type"] == "Top"


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    policy_tool = TOOL_FUNCTIONS["policy"]
    result = policy_tool(query="")
    assert result["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    policy_tool = TOOL_FUNCTIONS["policy"]
    result = policy_tool(query="data", policy_area="data_privacy")
    assert len(result["results"]) > 0
    for r in result["results"]:
        assert r["policy_area"] == "data_privacy"


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    policy_tool = TOOL_FUNCTIONS["policy"]
    result = policy_tool(query="Injection probe", policy_area="source_citation")
    all_untrusted = []
    for r in result["results"]:
        all_untrusted.extend(r.get("untrusted_text", []))
    assert len(all_untrusted) > 0
    assert any("ignore the citation policy" in line for line in all_untrusted)


# ---------------- NEW TOOL: currency_exchange (CP3) ----------------

def test_currency_exchange_happy_path() -> None:
    curr_tool = TOOL_FUNCTIONS["currency_exchange"]
    result = curr_tool(base_currency="USD", target_currency="VND", amount=100.0)
    assert result["tool"] == "currency_exchange"
    assert result["base_currency"] == "USD"
    assert result["target_currency"] == "VND"
    assert result["amount"] == 100.0
    assert result["converted_amount"] == 2545000.0
    assert result["rate"] == 25450.0
    assert "2,545,000.00 VND" in result["formatted"]


def test_currency_exchange_bad_input_from_model() -> None:
    curr_tool = TOOL_FUNCTIONS["currency_exchange"]
    # Model sends negative amount
    res_neg = curr_tool(base_currency="USD", target_currency="VND", amount=-50)
    assert "error" in res_neg
    assert "ValueError" in res_neg["error"]

    # Model sends non-existent currency
    res_bad_curr = curr_tool(base_currency="XYZ", target_currency="VND", amount=10)
    assert "error" in res_bad_curr
    assert "XYZ" in res_bad_curr["message"]


def test_currency_exchange_failure_returns_error_dict() -> None:
    curr_tool = TOOL_FUNCTIONS["currency_exchange"]
    # Model sends non-numeric string
    result = curr_tool(base_currency="USD", target_currency="VND", amount="not-a-number")
    assert isinstance(result, dict)
    assert "error" in result
    assert result["tool"] == "currency_exchange"


def test_currency_exchange_same_currency() -> None:
    curr_tool = TOOL_FUNCTIONS["currency_exchange"]
    result = curr_tool(base_currency="EUR", target_currency="EUR", amount=50.0)
    assert result["rate"] == 1.0
    assert result["converted_amount"] == 50.0
