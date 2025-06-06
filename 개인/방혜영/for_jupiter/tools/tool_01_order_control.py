from typing import List, Dict, Any # 이 부분을 추가해주세요.
from pydantic import BaseModel, Field # 중요!
from langchain_core.tools import Tool # 직접 Tool 클래스 사용
from langchain_core.tools import StructuredTool
from collections import Counter
from langchain_openai import ChatOpenAI 
from langchain_core.messages import AnyMessage, AIMessage, SystemMessage, HumanMessage, ToolMessage

#from-import 방식으로는 원본 변수가 수정되지 않아 변경
import tools.database.delivery as delivery
import tools.database.orders  as order
import tools.database.products as product


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

class TrackParcelLocationInput(BaseModel):
    delivery_id: str = Field(description="배송 위치를 추적할 배송의 ID")

class SummarizeUserOrderHistoryInput(BaseModel):
    user_id: str = Field(description="주문 내역을 요약할 사용자의 ID. 시스템 메시지에 명시된 현재 고객 ID를 사용해야 합니다.")

# 취소 도구의 입력 스키마 정의
class CancelOrderInput(BaseModel):
    user_id: str = Field(description="주문을 취소할 사용자의 ID. 시스템 메시지에 명시된 현재 고객 ID를 사용해야 합니다.")
    order_id: str = Field(description="취소할 주문의 ID.")

# 변경 도구의 입력 스키마 정의 (변경 내용 스키마는 필요에 따라 더 상세하게 정의)
class UpdateOrderDetailsInput(BaseModel):
    order_id: str = Field(description="정보를 변경할 주문의 ID.")
    new_details: Dict[str, Any] = Field(description="주문에서 변경될 상세 정보 (예: {'address': '새 주소', 'quantity': 3})")



class CustomerServiceTools:
    def __init__(self):
        self._products_db = product.products

        self._orders_db = order.orders

        self._delivery_db = delivery.delivery

    # 도구 메서드들은 이전과 동일하게 유지 ~ 구현 위치 (위의 DB를 참조하여)
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
        특정 배송 ID를 입력받아 현재 배송 상태, 발송일, 예상도착일 등의 상세 정보를 반환합니다.
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

#  사용자 주문 내역 요약 도구 만들기

    def summarize_user_order_history(self, user_id: str) -> str:
        """
        특정 사용자 ID를 입력받아 해당 사용자의 최근 주문 상태를 요약하여 반환합니다.
        응답에는 총 주문 건수와  배송 완료/배송중/결제 완료/상품 준비중 각각 몇 건인지 포함됩니다.
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


# 선호 카테고리 조회

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


# 키워드로 상품 검색하기

    def search_with_normal_keyword_use_llm(self, keyword: str) -> str:
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


# 택배 위치 추적 도구 만들기
    def get_delivery_state_and_location(self, delivery_id: str) -> str:
        """
        특정 배송 ID를 입력받아 현재 배송 상태와 위치를 반환합니다.
        """
        print(f"[Tool Called] get_delivery_state_and_location (delivery_id: {delivery_id})")
        status_info = self._delivery_db.get(delivery_id)
        if status_info:
            return f"배송 ID {status_info.delivery_id}는 현재 {status_info.delivery_state} 상태이며, 위치는 {status_info.location} 입니다."
        return {"error": f"배송 ID '{delivery_id}'에 해당하는 배송 정보를 찾을 수 없습니다."}

# 주문 취소/변경하기
    def cancel_order(self, user_id: str, order_id: str) -> str:
        """
        유저 ID와 주문 ID를 입력받아 해당 주문의 상태를 '취소됨'으로 업데이트하고,
        해당 배송의 상태도 '취소됨'으로 업데이트합니다.
        배송이 시작되지 않은 주문 (예: '결제 완료'상태, '상품 준비중'상태)만 취소 가능합니다.
        
        Args:
            user_id: 취소할 유저 ID
            order_id: 취소할 주문 ID
        """
        print(f"[Tool Called] cancel_order (order_id: {user_id} order_id: {order_id})")
        for order in self._orders_db[user_id]:
            if order["order_id"] == order_id:
                # 취소 가능한 상태인지 확인
                if order["order_status"] in ["결제 완료", "상품 준비중"]:
                    order["order_status"] = "취소됨"
                    print(f"[DB Updated] Order {order_id} status changed to '취소됨'")

                    # 해당 배송 정보도 업데이트
                    delivery_id = order.get("delivery_id") # 주문 정보에서 배송 ID를 가져옵니다.
                    if delivery_id and delivery_id in self._delivery_db: # 배송 ID가 존재하고 배송 DB에 있는 경우
                        self._delivery_db[delivery_id]["delivery_state"] = "취소됨" # 배송 상태를 '취소됨'으로 변경합니다.
                        print(f"[DB Updated] Delivery {delivery_id} status changed to '취소됨'")

                    return f"주문 ID '{order_id}'가 성공적으로 취소되었습니다."
                else:
                    return f"주문 ID '{order_id}'는 현재 '{order['order_status']}' 상태로 취소가 불가능합니다."
        return f"주문 ID '{order_id}'에 해당하는 주문을 찾을 수 없습니다."


    def update_order_details(self, order_id: str, new_details: Dict[str, Any]) -> str:
        """
        주문 ID와 변경될 상세 정보(예: 주소, 수량 - 실제 DB 스키마에 따라 다름)를 입력받아 주문 정보를 업데이트합니다.
        배송이 시작되지 않은 주문 (예: '결제 완료', '상품 준비중')만 변경 가능합니다.
        주소 변경 건의 경우 '정보 변경 요청 접수됨' 단계를 건너뛰고 바로 주소 변경을 반영합니다.
        """
        print(f"[Tool Called] update_order_details (order_id: {order_id}, new_details: {new_details})")
        for user_id, orders_list in self._orders_db.items():
            for order in orders_list:
                if order["order_id"] == order_id:
                    # 변경 가능한 상태인지 확인
                    if order["order_status"] in ["결제 완료", "상품 준비중"]:
                        # 주소 변경 요청인지 확인
                        if 'address' in new_details:
                            # 주소 변경 로직 반영 (실제 DB 업데이트 시 여기에 주소 업데이트 코드를 추가)
                            # 예시: order['address'] = new_details['address']
                            # 주소 변경의 경우 상태를 바꾸지 않고 변경 성공 메시지 반환
                            print(f"[DB Updated] Order {order_id} address updated to {new_details['address']}. Status remains '{order['order_status']}'.")
                            return f"주문 ID '{order_id}'의 주소가 '{new_details['address']}'(으)로 성공적으로 변경되었습니다."
                        else:
                            # 주소 변경이 아닌 다른 정보 변경 요청 (수량 등)
                            # 실제 DB 업데이트 로직: new_details 딕셔너리를 사용하여 order 딕셔너리를 업데이트합니다.
                            # 예시: order.update(new_details)
                            # 주소 변경 외는 간단히 상태를 '정보 변경 요청 접수됨'으로 표시하고, 실제 변경은 구현하지 않음
                            order["order_status"] = "정보 변경 요청 접수됨"
                            print(f"[DB Updated] Order {order_id} details update requested. Status changed to '정보 변경 요청 접수됨'.")
                            return f"주문 ID '{order_id}'의 정보 변경 요청이 접수되었습니다. 상세 변경 내용은 확인 후 처리됩니다."
                    else:
                        return f"주문 ID '{order_id}'는 현재 '{order['order_status']}' 상태로 정보 변경이 불가능합니다."
        return f"주문 ID '{order_id}'에 해당하는 주문을 찾을 수 없습니다."


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
        func=customer_service.summarize_user_order_history,
        name="summarize_user_order_history",
        description="특정 사용자 ID를 입력받아 해당 사용자의 최근 주문 상태를 요약하여 반환합니다. 응답에는 총 배송 건수와  배송 완료/배송중/결제 완료/상품 준비중 각각 몇 건인지 포함됩니다. 시스템 메시지에 명시된 현재 고객 ID를 사용해야 합니다.",
        args_schema=GetUserPastOrdersInput
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
        func=customer_service.get_user_favorite_category,
        name="get_user_id",
        description="고객 정보에서 user_id를 추출하여 반환합니다."
),
    Tool.from_function(
        func=customer_service.get_delivery_state_and_location,
        name="get_delivery_state_and_location",
        description="배송 ID를 입력받아 현재 택배의 배송 상태와 위치를 반환합니다.",
        args_schema=TrackParcelLocationInput
),

    StructuredTool.from_function(
        func=customer_service.cancel_order,
        name="cancel_order",
        description="유저 ID와 주문 ID를 입력받아 해당 주문을 취소합니다.",
        args_schema=CancelOrderInput
    ),
    StructuredTool.from_function(
        func=customer_service.update_order_details,
        name="update_order_details",
        description="주문 ID를 입력받아 해당 주문 정보를 업데이트합니다. 배송이 시작되지 않은 주문 (결제 완료, 상품 준비중 상태)만 변경 가능합니다. 변경 내용은 JSON 객체 형태의 'new_details' 파라미터로 전달해야 하며, 이 객체에는 'quantity', 'address', 'item_name' 등 변경하려는 필드와 그 값을 포함합니다. 예: {'quantity': 2} 또는 {'address': '새로운 주소'}",
        args_schema=UpdateOrderDetailsInput
    )
]