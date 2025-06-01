from langchain_core.messages import AnyMessage, AIMessage, SystemMessage, HumanMessage, ToolMessage
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI # 중요!

from tools.database.delivery import delivery
from tools.database.orders import orders
from tools.database.products import products

from ast import keyword
from typing import List, Dict, Any # 이 부분을 추가해주세요.
from collections import Counter
from langchain_core.tools import Tool # 직접 Tool 클래스 사용


class GetUserPastOrdersInput(BaseModel):
    user_id: str = Field(description="주문 내역을 조회할 사용자의 ID. 시스템 메시지에 명시된 현재 고객 ID를 사용해야 합니다.")

class GetOrderDetailsInput(BaseModel):
    order_id: str = Field(description="상세 정보를 조회할 주문의 ID")

class GetDeliveryStatusInput(BaseModel):
    delivery_id: str = Field(description="배송 상태를 조회할 배송의 ID")

class GetProductInformationInput(BaseModel):
    item_name: str = Field(description="상세 정보를 조회할 상품의 이름")

class SearchProductInformationInput(BaseModel):
    keyword: str = Field(description="상품 검색에 사용하는 일반적인 키워드")

class CustomerServiceTools:
    def __init__(self):

        self._products_db = products

        self._orders_db = orders

        self._delivery_db = delivery


    # 도구 메서드들은 이전과 동일하게 유지
    def get_user_past_orders(self, user_id: str) -> List[Dict[str, Any]]: # 반환 타입 수정
        """
        특정 사용자 ID를 입력받아 해당 사용자의 과거 주문 내역 목록을 반환합니다.
        각 주문 내역에는 주문 ID, 상품명, 주문 날짜, 주문 상태, 배송 ID가 포함됩니다.
        """
        print(f"[Tool Called] get_user_past_orders (user_id: {user_id})")
        orders = self._orders_db.get(user_id, [])
        if not orders:
            return [{"message": f"{user_id}님의 주문 내역을 찾을 수 없습니다. 사용자 ID를 다시 확인해주세요."}]
        # 반환하는 정보에 order_date와 order_status 추가
        return [
            {
                "order_id": o["order_id"],
                "item_name": o["item_name"],
                "order_date": o["order_date"],
                "order_status": o["order_status"],
                "delivery_id": o["delivery_id"]
            } for o in orders
        ]

    def get_order_details(self, order_id: str) -> Dict[str, Any]:
        """
        특정 주문 ID를 입력받아 해당 주문의 상세 정보(주문자 ID, 상품명, 수량, 총액, 주문날짜, 주문상태, 배송ID 등)를 반환합니다.
        """
        print(f"[Tool Called] get_order_details (order_id: {order_id})")
        for orders_list in self._orders_db.values():
            for order in orders_list:
                if order["order_id"] == order_id:
                    # 주문 상세 정보에 더 많은 필드를 포함하여 반환
                    return {
                        "order_id": order["order_id"],
                        "user_id": order["user_id"],
                        "item_name": order["item_name"],
                        "quantity": order["quantity"],
                        "total_price": order["total_price"],
                        "order_date": order["order_date"],
                        "order_status": order["order_status"],
                        "delivery_id": order["delivery_id"],
                        # 상품 DB에서 추가 정보 가져오기 (옵션)
                        "product_details": self._products_db.get(order["item_id"], {}),
                        # 배송 DB에서 추가 정보 가져오기 (옵션)
                        "delivery_details": self._delivery_db.get(order["delivery_id"], {})
                    }
        return {"error": f"주문 ID '{order_id}'에 해당하는 주문을 찾을 수 없습니다."}

    def get_delivery_status(self, delivery_id: str) -> Dict[str, Any]: # 반환 타입 수정
        """
        특정 배송 ID를 입력받아 현재 배송 상태, 발송일, 예상도착일, 위치 등의 상세 정보를 반환합니다.
        """
        print(f"[Tool Called] get_delivery_status (delivery_id: {delivery_id})")
        status_info = self._delivery_db.get(delivery_id)
        if status_info:
            # 더 많은 배송 정보 반환
            return status_info
        return {"error": f"배송 ID '{delivery_id}'에 해당하는 배송 정보를 찾을 수 없습니다."}

    def get_product_information(self, item_name: str) -> Dict[str, Any]:
        """
        상품명을 입력받아 해당 상품의 상세 정보(카테고리, 가격, 설명, 리뷰, 환불 규정 등)를 반환합니다.
        """
        print(f"[Tool Called] get_product_information (item_name: {item_name})")
        for product in self._products_db.values():
            # 상품명 검색 시 대소문자 구분 없이, 부분 일치도 고려할 수 있으나 여기서는 완전 일치(lower)
            if product["item_name"].lower() == item_name.lower():
                return product # 상품의 모든 정보 반환
        return {"error": f"상품명 '{item_name}'에 해당하는 상품 정보를 찾을 수 없습니다."}


    def search_products_by_keyword(self, keyword: str, category: str = None) -> List[Dict[str, Any]]:
        """
        일반적인 키워드로 상품을 문의할 때 관련된 상품을 반환합니다. 카테고리 값이 들어오면 카테고리를 한정합니다.
        """
        print(f"[Tool Called] search_products_by_keyword (keyword: {keyword})")
        # 부분 일치 - 추후 LLM 변환 고려
        matching_products = [
            product for product in self._products_db.values()
            if keyword.lower() in product["item_name"].lower()
            and (category is None or product["category"] == category)
        ]
        return matching_products

    # 과제 1
    def get_delivery_state_and_location(self, delivery_id: str) -> str:
        """
        특정 배송 ID를 입력받아 현재 배송 상태와 위치를 반환합니다.
        """
        print(f"[Tool Called] get_delivery_state_and_location (delivery_id: {delivery_id})")
        status_info = self._delivery_db.get(delivery_id)
        if status_info:
            return f"배송 ID {status_info.delivery_id}는 현재 {status_info.delivery_state} 상태이며, 위치는 {status_info.location} 입니다."
        return {"error": f"배송 ID '{delivery_id}'에 해당하는 배송 정보를 찾을 수 없습니다."}


    # 과제 2 사용자 주문 내역 요약 도구 만들기
    def summarize_user_order_history(self, user_id: str) -> str:
      """
      특정 사용자 ID를 입력받아 해당 사용자의 최근 주문 상태를 요약하여 반환합니다.
      응답에는 총 주문 건수와 배송 완료/배송중/결제 완료/상품 준비중 각각 몇 건인지 포함됩니다.
      """
      print(f"[Tool Called] summarize_user_order_history (user_id: {user_id})")
      # get_user_past_orders 도구를 호출하여 주문 내역을 가져옵니다.
      orders = self.get_user_past_orders(user_id)

      # 주문 내역이 없거나 오류 메시지인 경우 처리
      if not orders or ("message" in orders[0] and "주문 내역을 찾을 수 없습니다" in orders[0]["message"]):
        # get_user_past_orders에서 반환된 오류 메시지를 그대로 반환
        return orders[0].get("message", f"{user_id}님의 주문 내역을 찾을 수 없습니다.")


      total_orders_count = len(orders) # 총 주문 건수 (각 주문 객체 기준)
      # 각 상태별 주문 수를 세기 위한 Counter 객체 사용
      status_counts = Counter(order.get("order_status") for order in orders)


      summary = f"총 {total_orders_count}건의 주문 중 "
      summary_parts = []


      # 주요 상태별로 요약 문구 생성 (예시 응답에 맞게)
      if status_counts.get("배송 완료", 0) > 0:
        summary_parts.append(f"{status_counts['배송 완료']}건은 '배송 완료' 상태")
      if status_counts.get("배송중", 0) > 0:
        summary_parts.append(f"{status_counts['배송중']}건은 '배송 중' 상태")
      if status_counts.get("상품 준비중", 0) > 0:
        summary_parts.append(f"{status_counts['상품 준비중']}건은 '상품 준비중' 상태")
      if status_counts.get("결제 완료", 0) > 0:
        summary_parts.append(f"{status_counts['결제 완료']}건은 '결제 완료' 상태")


      # 그 외 상태 처리 (필요하다면 추가)
      other_statuses = {status: count for status, count in status_counts.items() if status not in ["배송 완료", "배송중", "상품 준비중", "결제 완료"]}
      for status, count in other_statuses.items():
        if count > 0:
          summary_parts.append(f"{count}건은 '{status}' 상태")

      if summary_parts:
        summary += ", ".join(summary_parts) + "입니다."
      else:
        summary += "아직 주문 내역이 없습니다." # 주문은 있지만 상태가 명시된 상태에 없는 경우

      return summary


    #과제 3
    def get_user_favorite_category(self, user_id: str) -> str:
        print(f"[Tool Called] get_user_favorite_category (user_id: {user_id})")
        orders = self._orders_db.get(user_id)
        print(f"[SELECT] orders : {orders}")
        if not orders:
          return f"[에러] 사용자 '{user_id}'의 주문 내역이 없습니다."

        categories = []
        for order in orders:
          item_id = order["item_id"]
          product = self._products_db.get(item_id)
          if product:
            categories.append(product["category"])

        if not categories:
          return "상품 카테고리 정보가 없습니다."

        category_count = Counter(categories)
        top_category, count = category_count.most_common(1)[0]
        return f"{user_id} 고객님은 {top_category}을(를) {count}회 구매하셨습니다. 가장 선호하는 카테고리는 {top_category}입니다."


    #과제 4
    def search_with_normal_keyword_use_llm(self, keyword: str) -> str:
        # OpenAI의 ChatOpenAI 모델(GPT-4o)을 사용하여 LLM 초기화
        keyword_llm = ChatOpenAI(model="gpt-4o-mini")  # 언어 모델을 gpt-4o로 설정

        search_sys_msg = SystemMessage(content=f"""
        당신은 고객의 질의에서 일반적인 키워드를 추출하여 해당하는 상품의 정보 목록을 반환하는 AI 에이전트입니다.
        검색한 결과를 간결하고 보기쉽게 정리하여 고객에게 제공하세요

        고객 질의의 키워드는 이렇습니다.
        {keyword}

        현재 상품 목록은 아래와 같습니다.
        {str(self._products_db.values())}

        """)
        return keyword_llm.invoke([search_sys_msg, HumanMessage(content=keyword)])


# CustomerServiceTools 인스턴스 생성
customer_service = CustomerServiceTools()


# Tool.from_function을 사용하여 도구 목록 준비 (도구 설명도 약간 업데이트)
tools = [
    Tool.from_function(
        func=customer_service.get_user_past_orders,
        name="get_user_past_orders",
        description="특정 사용자 ID를 입력받아 해당 사용자의 과거 주문 내역 목록을 반환합니다. 각 주문 내역에는 주문 ID, 상품명, 주문 날짜, 주문 상태, 배송 ID가 포함됩니다. 시스템 메시지에 명시된 현재 고객 ID를 사용해야 합니다.",
        args_schema=GetUserPastOrdersInput
    ),
    Tool.from_function(
        func=customer_service.get_order_details,
        name="get_order_details",
        description="특정 주문 ID를 입력받아 해당 주문의 상세 정보(주문자 ID, 상품명, 수량, 총액, 주문날짜, 주문상태, 배송ID, 상품 및 배송 추가정보 등)를 반환합니다.",
        args_schema=GetOrderDetailsInput
    ),
    Tool.from_function(
        func=customer_service.get_delivery_status,
        name="get_delivery_status",
        description="특정 배송 ID를 입력받아 현재 배송 상태, 발송일, 예상도착일 등의 상세 정보를 반환합니다.",
        args_schema=GetDeliveryStatusInput
    ),
    Tool.from_function(
        func=customer_service.get_product_information,
        name="get_product_information",
        description="상품명을 입력받아 해당 상품의 상세 정보(카테고리, 가격, 설명, 리뷰, 환불 규정 등)를 반환합니다.",
        args_schema=GetProductInformationInput
    ),
    Tool.from_function(
        func=customer_service.get_delivery_state_and_location,
        name="get_delivery_state_and_location",
        description="특정 배송 ID를 입력받아 현재 배송 상태와 위치 정보를 반환합니다",
        args_schema=GetDeliveryStatusInput
        ),
    Tool.from_function(
        func=customer_service.get_user_favorite_category,
        name="get_user_favorite_category",
        description="주문 내역에서 가장 많이 구매한 상품 카테고리를 찾아 반환합니다.",
        args_schema=GetUserPastOrdersInput
        ),
    Tool.from_function(
        func=customer_service.search_with_normal_keyword_use_llm,
        name="search_with_normal_keyword_use_llm",
        description="일반적인 키워드가 들어왔을 때 해당하는 상품의 목록을 반환합니다.",
        args_schema=SearchProductInformationInput
    ),
      Tool.from_function(
        func=customer_service.summarize_user_order_history,
        name="summarize_user_order_history",
        description="특정 사용자 ID를 입력받아 해당 사용자의 최근 주문 상태를 요약하여 반환합니다. 응답에는 총 배송 건수와 배송 완료/배송중/결제 완료/상품 준비중 각각 몇 건인지 포함됩니다.",
        args_schema=GetUserPastOrdersInput
    )
]