from langchain_openai import ChatOpenAI
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition  # 도구 호출 조건을 확인하는 조건부 로직
from langgraph.prebuilt import ToolNode  # 도구 노드를 정의하는 미리 빌드된 클래스

from tool_setting import tools
from agent_data import sys_msg

llm = ChatOpenAI(model="gpt-4o-mini")  # 언어 모델을 gpt-4o로 설정
llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    messages: Annotated[list, add_messages] # 사전 빌드된 함수 덕분에 messages는 기존 목록을 덮어쓰지 않고 새롭게 추가됩니다.


def chatbot(state: State):
    return {
        "messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]
    }


# initiate a graph
builder = StateGraph(State)

# add a node
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))

# connect nodes
builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")

# compile the graph
graph = builder.compile()

