  # API 키를 환경변수로 관리하기 위한 설정 파일
import os
from dotenv import load_dotenv

# API KEY 정보를 로드합니다. 파일 이름은 앞에 comma가 있는 ".env" 파일여야 합니다!
load_dotenv(override=True)
print(f"[API KEY]\n{os.environ['OPENAI_API_KEY']}")
print(f"[API KEY]\n{os.environ['TAVILY_API_KEY']}")