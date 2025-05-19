from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage, RemoveMessage

# AI 메시지와 tool 관련 모듈을 가져옵니다.
from langchain_core.tools import tool
from llm_tools import add, multiply, divide

from langgraph.checkpoint.memory import MemorySaver  # MemorySaver 모듈 가져오기
from langgraph.graph import StateGraph, START, END

from llm_state import ConversationState
from memorize_message import summarize_conversation, should_continue


# API KEY 정보를 로드합니다. 파일 이름은 앞에 comma가 있는 ".env" 파일여야 합니다!
load_dotenv(override=True)
llm = ChatOpenAI(model="gpt-4o-mini")

# Augment the LLM with tools
tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)


# 노드 정의
def llm_call(state: ConversationState):
    """LLM이 툴 호출 여부를 결정"""
    return {
        "messages": [
            llm_with_tools.invoke(
                [
                    SystemMessage(
                        content="당신은 유저의 요청을 친절하게 처리하는 모델입니다."
                    )
                ]
                + state["messages"]
            )
        ]
    }

def tool_node(state: ConversationState):
    """툴을 호출하여 실행"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}


  # 4. 워크플로우 구축
agent_builder = StateGraph(ConversationState)

# 노드 추가
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)
agent_builder.add_node("summarize_conversation", summarize_conversation)

# 엣지 연결
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    {
        "Action": "tool_node",
        "summarize_conversation": "summarize_conversation",
        END: END,
    },
)
agent_builder.add_edge("tool_node", "llm_call")
agent_builder.add_edge("summarize_conversation", END)



memory = MemorySaver()  # 메모리 기반 체크포인터 초기화

# 에이전트 컴파일 (체크포인트 사용)
agent_summarization = agent_builder.compile(checkpointer=memory)


summarization_config = {"configurable": {"thread_id": "11"}}
messages = [HumanMessage(content="1과 3을 더한 이후 4를 더한다. 그 뒤 5를 곱하고, 6을 더한다. 그리고 3을 더하고, 5를 곱한다.")]

initial_state = {
    "messages": messages,
    "summary_list": []
}

messages = [HumanMessage(content="3을 더한다.")]

messages = [HumanMessage(content="다시 2를 더하고, 4를 곱한다.")]

messages = [HumanMessage(content="다시 2를 더하고, 4를 곱한다.")]

messages = agent_summarization.invoke({"messages": messages}, config=summarization_config)
for m in messages["messages"]:
    m.pretty_print()

