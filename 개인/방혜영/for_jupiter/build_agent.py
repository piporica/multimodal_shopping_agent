from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition  # 도구 호출 조건을 확인하는 조건부 로직
from langgraph.prebuilt import ToolNode  # 도구 노드를 정의하는 미리 빌드된 클래스
from tool_setting import tools
from agent_data import sys_msg

from tools.tool_02_memorize import summarize_conversation, should_continue
from agent_setting import State


llm = ChatOpenAI(model="gpt-4o-mini")  # 언어 모델을 gpt-4o로 설정
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {
        "messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]
    }

# initiate a graph
builder = StateGraph(State)

# add a node
builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))
builder.add_node("summarize_conversation", summarize_conversation)

# connect nodes
builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")
builder.add_conditional_edges(
    "chatbot",
    should_continue,
    {
        "Action": "tools",
        "summarize_conversation": "summarize_conversation",
        END: END,
    },
)
builder.add_edge("summarize_conversation", END)


# compile the graph
graph = builder.compile()

