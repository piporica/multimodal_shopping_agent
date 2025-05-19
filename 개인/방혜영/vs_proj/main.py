from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# API KEY 정보를 로드합니다. 파일 이름은 앞에 comma가 있는 ".env" 파일여야 합니다!
load_dotenv(override=True)

# OpenAI의 ChatOpenAI 모델(GPT-4o)을 사용하여 LLM 초기화
llm = ChatOpenAI(model="gpt-4o-mini")  # 언어 모델을 gpt-4o로 설정
print(llm.invoke("안녕하세요").content)

