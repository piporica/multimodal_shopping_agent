# This is a simple general-purpose chatbot built on top of LangChain and Gradio.
# Before running this, make sure you have exported your OpenAI API key as an environment variable:
# export OPENAI_API_KEY="your-openai-api-key"
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
import gradio as gr

# API KEY 정보를 로드합니다. 파일 이름은 앞에 comma가 있는 ".env" 파일여야 합니다!
load_dotenv(override=True)


model = ChatOpenAI(model="gpt-4o-mini")
def predict(message, history):
    history_langchain_format = []
    for msg in history:
        if msg['role'] == "user":
            history_langchain_format.append(HumanMessage(content=msg['content']))
        elif msg['role'] == "assistant":
            history_langchain_format.append(AIMessage(content=msg['content']))
    history_langchain_format.append(HumanMessage(content=message))
    gpt_response = model.invoke(history_langchain_format)
    return gpt_response.content

demo = gr.ChatInterface(
    predict,
    type="messages"
)

demo.launch()