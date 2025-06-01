
from datetime import datetime, timedelta
# 오늘 날짜를 기준으로 데이터 생성 (2025-05-12)
today = datetime(2025, 5, 12)

delivery = {
            "delivery_D123_001": {"delivery_id": "delivery_D123_001", "delivery_state": "배송 완료", "shipped_date": (today - timedelta(days=88)).strftime("%Y-%m-%d"), "estimated_arrival_date": (today - timedelta(days=87)).strftime("%Y-%m-%d"), "actual_arrival_date": (today - timedelta(days=87)).strftime("%Y-%m-%d"), "shipping_company": "대한통운", "delivery_history": [
                {"timestamp": (today - timedelta(days=88, hours=3)).strftime("%Y-%m-%d %H:%M:%S"), "location": "서울 강남 물류센터", "status": "상품인수"},
                {"timestamp": (today - timedelta(days=88, hours=1)).strftime("%Y-%m-%d %H:%M:%S"), "location": "수도권 터미널", "status": "터미널 입고"},
                {"timestamp": (today - timedelta(days=87, hours=10)).strftime("%Y-%m-%d %H:%M:%S"), "location": "고객님 지역 배송캠프", "status": "배송출발"},
                {"timestamp": (today - timedelta(days=87, hours=5)).strftime("%Y-%m-%d %H:%M:%S"), "location": "고객님 댁", "status": "배송 완료"}
            ]},
            "delivery_D123_002": {"delivery_id": "delivery_D123_002", "delivery_state": "배송 완료", "shipped_date": (today - timedelta(days=58)).strftime("%Y-%m-%d"), "estimated_arrival_date": (today - timedelta(days=57)).strftime("%Y-%m-%d"), "actual_arrival_date": (today - timedelta(days=57)).strftime("%Y-%m-%d"), "shipping_company": "우체국택배", "delivery_history": [
                {"timestamp": (today - timedelta(days=58)).strftime("%Y-%m-%d %H:%M:%S"), "location": "제주 물류센터", "status": "집화처리"},
                {"timestamp": (today - timedelta(days=57)).strftime("%Y-%m-%d %H:%M:%S"), "location": "고객님 댁", "status": "배송 완료"}
            ]},
            "delivery_D123_003": {"delivery_id": "delivery_D123_003", "delivery_state": "배송 완료", "shipped_date": (today - timedelta(days=29)).strftime("%Y-%m-%d"), "estimated_arrival_date": (today - timedelta(days=28)).strftime("%Y-%m-%d"), "actual_arrival_date": (today - timedelta(days=28)).strftime("%Y-%m-%d"), "shipping_company": "CJ대한통운", "delivery_history": [{"timestamp": (today - timedelta(days=28)).strftime("%Y-%m-%d %H:%M:%S"), "location": "고객님 댁", "status": "배송 완료"}]},
            "delivery_D123_004": {"delivery_id": "delivery_D123_004", "delivery_state": "배송중 (터미널 간선상차)", "shipped_date": (today - timedelta(days=6)).strftime("%Y-%m-%d"), "estimated_arrival_date": (today - timedelta(days=4)).strftime("%Y-%m-%d"), "actual_arrival_date": None, "shipping_company": "로젠택배", "delivery_history": [
                {"timestamp": (today - timedelta(days=6, hours=5)).strftime("%Y-%m-%d %H:%M:%S"), "location": "인천 물류센터", "status": "상품인수"},
                {"timestamp": (today - timedelta(days=6, hours=2)).strftime("%Y-%m-%d %H:%M:%S"), "location": "인천터미널", "status": "터미널입고"},
                {"timestamp": (today - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"), "location": "대전HUB", "status": "터미널간선상차 (현재위치)"}
            ]},
            "delivery_D123_005": {"delivery_id": "delivery_D123_005", "delivery_state": "상품 준비중", "shipped_date": None, "estimated_arrival_date": (today + timedelta(days=2)).strftime("%Y-%m-%d"), "actual_arrival_date": None, "shipping_company": "롯데택배", "delivery_history": [
                 {"timestamp": (today - timedelta(days=2, hours=1)).strftime("%Y-%m-%d %H:%M:%S"), "location": "판매자 확인", "status": "주문확인 및 상품준비중"}
            ]},
            "delivery_D123_006": {"delivery_id": "delivery_D123_006", "delivery_state": "결제 완료 (배송 준비 예정)", "shipped_date": None, "estimated_arrival_date": (today + timedelta(days=3)).strftime("%Y-%m-%d"), "actual_arrival_date": None, "shipping_company": "한진택배", "delivery_history": [
                {"timestamp": (today - timedelta(minutes=20)).strftime("%Y-%m-%d %H:%M:%S"), "location": "결제시스템", "status": "결제완료"}
            ]},
            "delivery_D123_007": {"delivery_id": "delivery_D123_007", "delivery_state": "배송 완료", "shipped_date": (today - timedelta(days=13)).strftime("%Y-%m-%d"), "estimated_arrival_date": (today - timedelta(days=12)).strftime("%Y-%m-%d"), "actual_arrival_date": (today - timedelta(days=10)).strftime("%Y-%m-%d"), "shipping_company": "CJ대한통운", "delivery_history": [{"timestamp": (today - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"), "location": "서울 중구 을지로 50 을지한국빌딩 19층", "status": "배송 완료"}]},
            "delivery_D124_001": {"delivery_id": "delivery_D124_001", "delivery_state": "배송 완료", "shipped_date": (today - timedelta(days=9)).strftime("%Y-%m-%d"), "estimated_arrival_date": (today - timedelta(days=8)).strftime("%Y-%m-%d"), "actual_arrival_date": (today - timedelta(days=8)).strftime("%Y-%m-%d"), "shipping_company": "대한통운", "delivery_history": [{"timestamp": (today - timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S"), "location": "고객님 댁", "status": "배송 완료"}]},
            "delivery_D124_002": {"delivery_id": "delivery_D124_002", "delivery_state": "상품 준비중", "shipped_date": None, "estimated_arrival_date": (today + timedelta(days=1)).strftime("%Y-%m-%d"), "actual_arrival_date": None, "shipping_company": "CJ대한통운", "delivery_history": [{"timestamp": (today - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"), "location": "판매자 확인", "status": "주문확인 및 상품준비중"}]},
            "delivery_D125_001": {"delivery_id": "delivery_D125_001", "delivery_state": "배송 완료", "shipped_date": (today - timedelta(days=14)).strftime("%Y-%m-%d"), "estimated_arrival_date": (today - timedelta(days=13)).strftime("%Y-%m-%d"), "actual_arrival_date": (today - timedelta(days=13)).strftime("%Y-%m-%d"), "shipping_company": "우체국택배", "delivery_history": [{"timestamp": (today - timedelta(days=13)).strftime("%Y-%m-%d %H:%M:%S"), "location": "고객님 댁", "status": "배송 완료"}]},
            "delivery_D126_001": {"delivery_id": "delivery_D126_001", "delivery_state": "배송중 (집화처리)", "shipped_date": (today - timedelta(days=4)).strftime("%Y-%m-%d"), "estimated_arrival_date": (today - timedelta(days=2)).strftime("%Y-%m-%d"), "actual_arrival_date": None, "shipping_company": "롯데택배", "delivery_history": [
                {"timestamp": (today - timedelta(days=4, hours=3)).strftime("%Y-%m-%d %H:%M:%S"), "location": "경기 광주 물류센터", "status": "상품인수"},
                {"timestamp": (today - timedelta(days=4, hours=1)).strftime("%Y-%m-%d %H:%M:%S"), "location": "경기 광주 터미널", "status": "집화처리 (현재위치)"}
            ]},
            "delivery_D126_002": {"delivery_id": "delivery_D126_002", "delivery_state": "결제 완료 (배송 준비 예정)", "shipped_date": None, "estimated_arrival_date": (today + timedelta(days=2)).strftime("%Y-%m-%d"), "actual_arrival_date": None, "shipping_company": "한진택배", "delivery_history": [{"timestamp": (today - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), "location": "결제시스템", "status": "결제완료"}]},
        }