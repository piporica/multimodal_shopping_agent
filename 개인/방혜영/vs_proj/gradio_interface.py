from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage
import base64
import gradio as gr

# API KEY 정보를 로드합니다. 파일 이름은 앞에 comma가 있는 ".env" 파일여야 합니다!
load_dotenv(override=True)

model = ChatOpenAI(model="gpt-4o-mini")

def convert_to_url(image_path):
    """이미지를 URL 형식으로 변환"""
    with open(image_path, "rb") as image_file:
        # 이미지를 base64로 인코딩
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/jpeg;base64,{encoded_string}"

def makeImageMessage(imgPath):
    image_url = convert_to_url(imgPath)
    msg = HumanMessage(content = [
        {"type": "image_url",
         "image_url": {"url": image_url}}
    ])
    return msg


def makeHumanMessageInHistory(content):
    if isinstance(content, tuple):
        imageMessage = makeImageMessage(content[0])
        return imageMessage
    else:
        return HumanMessage(content=content)
    
def makeHumanMessageInMessage(message):
    messageList = []
    if(message['text'] != ''):
        messageList.append(HumanMessage(content=message['text']))
    if(message['files'].count != 0):
        for filePath in message['files']:
            messageList.append(makeImageMessage(filePath))
    return messageList
    
def predict(message, history):
  history_langchain_format = []
  for msg in history:
      if msg['role'] == "user": 
          history_langchain_format.append(makeHumanMessageInHistory(msg['content']))
      elif msg['role'] == "assistant":
          history_langchain_format.append(AIMessage(content=msg['content']))
  history_langchain_format = history_langchain_format + makeHumanMessageInMessage(message)
  gpt_response = model.invoke(history_langchain_format)
  return gpt_response.content


demo = gr.ChatInterface(
    fn=predict,
    multimodal=True,
    type="messages",
    title="멀티모달 챗봇",
    description="쇼핑몰 문의에 대응하는 AI 챗봇입니다. 이전 대화의 이미지들도 함께 고려합니다.",
    analytics_enabled=False,
    textbox=gr.MultimodalTextbox(placeholder="텍스트를 입력하거나 이미지를 업로드해주세요.", 
                                 file_count="multiple", file_types=["image"]),
)

demo.launch(debug=True)