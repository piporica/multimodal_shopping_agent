
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict,  List

# 1. State 정의 (메모리 리스트 추가)
class ConversationState(TypedDict):
    messages: Annotated[list, add_messages]
    summary_list: List[str] = []  # 요약된 결과를 리스트로 보관. 필수는 아님.