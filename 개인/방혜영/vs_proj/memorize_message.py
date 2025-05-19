from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import gradio as gr
from langgraph.graph import StateGraph, START, END
from langchain.schema import AIMessage, HumanMessage
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, RemoveMessage
from langchain_core.tools import Tool
from typing import Annotated, TypedDict,  List, Literal

from llm_state import ConversationState;

# 대화 요약 함수 수정

SUMMARY_MARKER = "<|SUMMARIZED|>" # 고유 요약 마커 정의

llm = ChatOpenAI(model="gpt-4o-mini")

def summarize_conversation(state: ConversationState):
    """오래된 일반 메시지들을 요약하고 새로운 요약 메시지 추가"""

    messages = state["messages"]

    # 요약 프롬프트 생성
    summary_prompt = f"지금까지의 대화에서 중요한 내용을 간결하게 요약하세요:"
    prompt_messages = messages + [HumanMessage(content=summary_prompt)]

    # LLM을 호출하여 요약 생성
    response = llm.invoke(prompt_messages)

    # 새로운 요약 메시지 생성
    summary_message = AIMessage(content=f"{SUMMARY_MARKER} {response.content}")

    # 요약 메시지가 아닌 일반 메시지만 필터링
    normal_messages = [
        m for m in messages
        if not (isinstance(m, AIMessage) and m.content.startswith(SUMMARY_MARKER))
    ]

    keep_last_n = 3  # 최근 몇 개 일반 메시지는 남긴다
    messages_to_summarize = normal_messages[:-keep_last_n] if len(normal_messages) > keep_last_n else []

    if not messages_to_summarize:
        # 요약할 메시지가 없으면 아무것도 하지 않음
        return {}

    # 삭제할 메시지 지정 (요약된 메시지 삭제)
    delete_messages = [RemoveMessage(id=m.id) for m in messages_to_summarize]

    # summary_list에도 요약 추가 (optional)
    updated_summary_list = state.get("summary_list", []) + [response.content]

    return {
        "messages": delete_messages + [summary_message],
        "summary_list": updated_summary_list
    }
    
    
def should_continue(state: ConversationState) -> Literal["Action", "summarize_conversation", END]:
    """LLM이 도구 호출을 했는지, 또는 요약이 필요한지 결정"""

    messages = state["messages"]
    last_message = messages[-1]

    # 툴 호출이 있으면 Action 수행
    if last_message.tool_calls:
        return "Action"

    # 요약 필요 여부 판단 (요약 메시지는 제외하고 세기)
    normal_messages = [
        m for m in messages
        if not (isinstance(m, AIMessage) and m.content.startswith(SUMMARY_MARKER))
    ]

    if len(normal_messages) > 10:  # 일반 메시지가 10개 이상이면 요약
        return "summarize_conversation"

    return END
  