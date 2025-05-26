
from datetime import datetime, timedelta
# 오늘 날짜를 기준으로 데이터 생성 (2025-05-12)
today = datetime(2025, 5, 12)

orders =  {
            "user_123": [
                {"order_id": "order_U123_001", "user_id": "user_123", "delivery_id": "delivery_D123_001", "item_id": "item_C01", "item_name": "오가닉 코튼 티셔츠 (화이트)", "quantity": 2, "total_price": 70000, "order_date": (today - timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S"), "order_status": "배송 완료"},
                {"order_id": "order_U123_002", "user_id": "user_123", "delivery_id": "delivery_D123_002", "item_id": "item_P03", "item_name": "기계식 게이밍 키보드 K7", "quantity": 1, "total_price": 180000, "order_date": (today - timedelta(days=60)).strftime("%Y-%m-%d %H:%M:%S"), "order_status": "배송 완료"},
                {"order_id": "order_U123_003", "user_id": "user_123", "delivery_id": "delivery_D123_003", "item_id": "item_B01", "item_name": "AI 시대의 마케팅 전략 (도서)", "quantity": 1, "total_price": 22000, "order_date": (today - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"), "order_status": "배송 완료"},
                {"order_id": "order_U123_004", "user_id": "user_123", "delivery_id": "delivery_D123_004", "item_id": "item_P02", "item_name": "노이즈캔슬링 헤드폰 Pro", "quantity": 1, "total_price": 350000, "order_date": (today - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"), "order_status": "배송중"},
                {"order_id": "order_U123_005", "user_id": "user_123", "delivery_id": "delivery_D123_005", "item_id": "item_K01", "item_name": "프리미엄 믹서기 세트", "quantity": 1, "total_price": 125000, "order_date": (today - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"), "order_status": "상품 준비중"},
                {"order_id": "order_U123_006", "user_id": "user_123", "delivery_id": "delivery_D123_006", "item_id": "item_P01", "item_name": "프리미엄 스마트폰 X200", "quantity": 1, "total_price": 1200000, "order_date": (today - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S"), "order_status": "결제 완료"},
                {"order_id": "order_U123_007", "user_id": "user_123", "delivery_id": "delivery_D123_007", "item_id": "item_S01", "item_name": "탭댄스에 특화된 운동화", "quantity": 1, "total_price": 95000, "order_date":(today - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"), "order_status": "배송 완료"}
            ],
            "user_124": [
                 {"order_id": "order_U124_001", "user_id": "user_124", "delivery_id": "delivery_D124_001", "item_id": "item_P01", "item_name": "프리미엄 스마트폰 X200", "quantity": 1, "total_price": 1200000, "order_date": (today - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"), "order_status": "배송 완료"},
                 {"order_id": "order_U124_002", "user_id": "user_124", "delivery_id": "delivery_D124_002", "item_id": "item_C02", "item_name": "슬림핏 데님 팬츠", "quantity": 1, "total_price": 78000, "order_date": (today - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"), "order_status": "상품 준비중"}
            ],
            "user_125": [
                {"order_id": "order_U125_001", "user_id": "user_125", "delivery_id": "delivery_D125_001", "item_id": "item_P04", "item_name": "울트라 HD 4K 모니터 27인치", "quantity": 1, "total_price": 450000, "order_date": (today - timedelta(days=15)).strftime("%Y-%m-%d %H:%M:%S"), "order_status": "배송 완료"}
            ],
            "user_126": [
                {"order_id": "order_U126_001", "user_id": "user_126", "delivery_id": "delivery_D126_001", "item_id": "item_C01", "item_name": "오가닉 코튼 티셔츠 (화이트)", "quantity": 3, "total_price": 105000, "order_date": (today - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"), "order_status": "배송중"},
                {"order_id": "order_U126_002", "user_id": "user_126", "delivery_id": "delivery_D126_002", "item_id": "item_K01", "item_name": "프리미엄 믹서기 세트", "quantity": 1, "total_price": 125000, "order_date": (today - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), "order_status": "결제 완료"},
            ]
        }