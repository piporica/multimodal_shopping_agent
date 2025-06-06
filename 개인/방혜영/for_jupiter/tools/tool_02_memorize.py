from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import gradio as gr
from langgraph.graph import StateGraph, START, END
from langchain.schema import AIMessage, HumanMessage
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, RemoveMessage
from langchain_core.tools import Tool
from typing import Annotated, TypedDict,  List, Literal

from agent_setting import State;

# 대화 요약 함수 수정

SUMMARY_COUNT = 10  #요약 실행하는 메시지 수 
KEEP_LAST_N = 3 #남기는 일반 메시지 수 
SUMMARY_MARKER = "<|SUMMARIZED|>" # 고유 요약 마커 정의

llm = ChatOpenAI(model="gpt-4o-mini")

def summarize_conversation(state: State):
    """오래된 일반 메시지들을 요약하고 새로운 요약 메시지 추가"""

    messages = state["messages"]

    # 요약 대상 메시지 한정
    # 요약 메시지가 아닌 일반 메시지만 필터링
    normal_messages = [
        m for m in messages
        if not (isinstance(m, AIMessage) and m.content.startswith(SUMMARY_MARKER))
    ]

    messages_to_summarize = normal_messages[:-KEEP_LAST_N] if len(normal_messages) > KEEP_LAST_N else []

    if not messages_to_summarize:
        # 요약할 메시지가 없으면 아무것도 하지 않음
        return {}

    # 요약 프롬프트 생성
    summary_prompt = f"지금까지의 대화에서 중요한 내용을 간결하게 요약하세요:"
    prompt_messages = messages_to_summarize + [HumanMessage(content=summary_prompt)]

    # LLM을 호출하여 요약 생성
    response = llm.invoke(prompt_messages)

    # 새로운 요약 메시지 생성
    summary_message = AIMessage(content=f"{SUMMARY_MARKER} {response.content}")

    # 삭제할 메시지 지정 (요약된 메시지 삭제)
    delete_messages = [RemoveMessage(id=m.id) for m in messages_to_summarize]

    return {
        "messages": delete_messages + [summary_message] + normal_messages[-KEEP_LAST_N:] 
    }
    
    
def should_continue(state: State) -> Literal["Action", "summarize_conversation", END]:
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

    if len(normal_messages) > SUMMARY_COUNT: 
        return "summarize_conversation"

    return END
  