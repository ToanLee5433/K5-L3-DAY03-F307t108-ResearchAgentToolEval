"""Streamlit Web UI for Research Agent (Day 03 - Team F307t108).
Allows interactive chatting, live tool execution, guardrail confirmation, and prompt testing.
"""

from __future__ import annotations

import json
from pathlib import Path
import streamlit as st

from env_loader import load_lab_env
from providers import make_provider
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools
from chat import execute_tool_call, tool_results_message, assistant_tool_message

ROOT = Path(__file__).parent
ARTIFACTS_DIR = ROOT / "artifacts"
load_lab_env(ROOT)

st.set_page_config(
    page_title="Research Agent UI — Team F307t108",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Research Agent — F307t108 (L3B)")
st.caption("AI Research Assistant với Tool Calling tự động, Kiểm soát ranh giới an toàn & Đổi ngoại tệ")

# Load artifacts
@st.cache_resource
def load_agent_resources():
    system_prompt = (ARTIFACTS_DIR / "system_prompt.md").read_text(encoding="utf-8")
    tool_declarations = load_tool_declarations(ARTIFACTS_DIR / "tools.yaml")
    openai_tools = to_openai_tools(tool_declarations)
    provider = make_provider("gemini")
    return system_prompt, openai_tools, provider

try:
    system_prompt, openai_tools, provider = load_agent_resources()
except Exception as e:
    st.error(f"Lỗi khởi tạo Agent: {e}")
    st.stop()

# Sidebar: Info & Sample Prompts
with st.sidebar:
    st.header("⚙️ Cấu hình Agent")
    st.info("**Model:** Google Gemini (`gemini-3.5-flash-lite`)\n\n**Nhóm:** F307t108 — Lớp L3B\n\n**Trưởng nhóm:** Lê Quý Toàn (2A202603941)\n**Thành viên:** Đàm Hồng Thái (2A202603927)")
    
    st.subheader("🛠️ Công cụ hỗ trợ (Tools)")
    st.markdown("""
    - `lookup`: Tra cứu tin tức / web (Tavily)
    - `social_search`: Tìm bài đăng trên X/Twitter (RapidAPI)
    - `timeline`: Đọc tweet của người dùng cụ thể (RapidAPI)
    - `fetch`: Đọc nội dung bài viết từ URL (Firecrawl)
    - `currency_exchange`: **Tool mới** - Tra cứu tỷ giá & đổi ngoại tệ (USD, EUR, VND, JPY, GBP,...)
    - `format`: Định dạng bản tin theo mẫu cấu trúc
    - `clarify`: Ranh giới an toàn - hỏi lại khi thiếu thông tin hoặc cần xác nhận
    - `send`: Gửi bản tin lên Telegram (yêu cầu confirmed=True)
    """)
    
    st.subheader("💡 Câu hỏi mẫu để thử")
    sample_queries = [
        "Tin tức AI nổi bật nhất hôm nay",
        "Xem các bài đăng gần nhất của tài khoản sama trên X",
        "Đổi 100 USD sang tiền Việt Nam (VND)",
        "Đăng bản tin công nghệ mới lên Telegram giúp tôi",
        "Có thông tin gì về việc mua cổ phiếu nội bộ OpenAI không?"
    ]
    for q in sample_queries:
        if st.button(q, key=f"btn_{q[:15]}"):
            st.session_state["pending_input"] = q
            st.rerun()

    if st.button("🗑️ Xoá lịch sử hội thoại"):
        st.session_state["messages"] = []
        st.session_state["history"] = []
        st.rerun()

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Xin chào! Tôi là Research Agent của nhóm F307t108. Tôi có thể giúp bạn tra cứu tin tức web, đọc timeline mạng xã hội, quy đổi ngoại tệ và tổng hợp bản tin. Bạn cần tìm hiểu gì hôm nay?"}
    ]
if "history" not in st.session_state:
    st.session_state["history"] = []

# Display conversation
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "tools_called" in msg:
            with st.expander("🔍 Chi tiết Tool đã gọi", expanded=False):
                for call in msg["tools_called"]:
                    st.code(f"{call['name']}({json.dumps(call['args'], ensure_ascii=False, indent=2)})", language="json")

# Chat input handling
user_input = st.chat_input("Nhập câu hỏi hoặc yêu cầu nghiên cứu...")
if "pending_input" in st.session_state and st.session_state["pending_input"]:
    user_input = st.session_state.pop("pending_input")

if user_input:
    # Display user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Run agent loop
    history = st.session_state["history"]
    working_messages = [{"role": "system", "content": system_prompt}] + history[-10:] + [{"role": "user", "content": user_input}]
    
    all_calls = []
    final_response = ""

    with st.chat_message("assistant"):
        status_box = st.status("Đang xử lý...", expanded=True)
        max_tool_rounds = 4
        
        for round_idx in range(max_tool_rounds):
            status_box.write(f"Đang phân tích và chọn công cụ (vòng {round_idx + 1})...")
            resp = provider.complete(working_messages, openai_tools, temperature=0.0)
            calls = resp.tool_calls
            
            if not calls:
                final_response = resp.text or ""
                break
                
            all_calls.extend([{"name": c.name, "args": c.args} for c in calls])
            working_messages.append(assistant_tool_message(resp.text, calls))
            
            non_clarification_events = []
            is_clarifying = False
            clarify_question = ""
            
            for call in calls:
                status_box.write(f"🔧 Thực thi tool: `{call.name}`...")
                event = execute_tool_call(call)
                res = event.get("result", {})
                if isinstance(res, dict) and res.get("awaiting_user"):
                    is_clarifying = True
                    clarify_question = res.get("question") or call.args.get("question") or "Vui lòng cung cấp thêm thông tin."
                non_clarification_events.append(event)
                
            if is_clarifying:
                final_response = clarify_question
                break
                
            working_messages.append(tool_results_message(non_clarification_events))
        else:
            final_response = resp.text or "Đã đạt giới hạn số vòng gọi tool."

        status_box.update(label="Hoàn thành!", state="complete", expanded=False)
        st.markdown(final_response)
        
        if all_calls:
            with st.expander("🔍 Chi tiết Tool đã gọi", expanded=False):
                for call in all_calls:
                    st.code(f"{call['name']}({json.dumps(call['args'], ensure_ascii=False, indent=2)})", language="json")

    # Save to session history
    st.session_state["messages"].append({
        "role": "assistant",
        "content": final_response,
        "tools_called": all_calls
    })
    st.session_state["history"].append({"role": "user", "content": user_input})
    st.session_state["history"].append({"role": "assistant", "content": final_response})

