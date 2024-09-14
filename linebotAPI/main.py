from fastapi import FastAPI, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage
import schedule
import time
import threading
from linebot.models import MessageEvent, TextMessage, TextSendMessage


app = FastAPI()

# 替換成你的 LINE Bot 資訊
line_bot_api = LineBotApi('Ra3o/7sMnHqPpdmRF91FFS7mqHLALhENQiKLExunQFHK1rNGvET8x29hU+jR//9m/4ksOa4lSRrd67A5zDSHBybARp271lmbIwVNVZcmErSBJKqZ8s+zjA8vVonhQM27rN5aVw7mxdQ12arpkNhUaQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e70229e114eeac0f035dc81a0680a0f4')

# 定義發送定期訊息的函數
def send_scheduled_message():
    text = {
  "type": "bubble",
  "header": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "text",
        "text": "本週讀書會JS內容預告",
        "weight": "bold",
        "size": "sm",
        "color": "#040404FF",
        "align": "center",
        "contents": []
      }
    ]
  },
  "hero": {
    "type": "image",
    "url": "https://upload.wikimedia.org/wikipedia/zh/thumb/f/fb/Hogwarts-1-.jpg/300px-Hogwarts-1-.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "label": "Action",
      "uri": "https://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "horizontal",
    "spacing": "md",
    "contents": [
      {
        "type": "box",
        "layout": "vertical",
        "flex": 1,
        "contents": [
          {
            "type": "image",
            "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSuNZEQhAFsgn86ZBpPx5fvSMJeM2aa9HhkGQ&s",
            "margin": "md",
            "size": "sm",
            "aspectRatio": "4:3",
            "aspectMode": "cover"
          }
        ]
      },
      {
        "type": "box",
        "layout": "vertical",
        "flex": 2,
        "contents": [
          {
            "type": "text",
            "text": "前週內容複習",
            "size": "xs",
            "flex": 1,
            "gravity": "top",
            "contents": []
          },
          {
            "type": "separator"
          },
          {
            "type": "text",
            "text": "認識DOM",
            "size": "xs",
            "flex": 2,
            "gravity": "center",
            "contents": []
          },
          {
            "type": "separator"
          },
          {
            "type": "text",
            "text": "DOM-基本操作",
            "size": "xs",
            "flex": 2,
            "gravity": "center",
            "contents": []
          },
          {
            "type": "separator"
          },
          {
            "type": "text",
            "text": "總練習-霍格華茲分類帽",
            "size": "xs",
            "flex": 1,
            "gravity": "bottom",
            "contents": []
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "horizontal",
    "contents": [
      {
        "type": "text",
        "text": "9/18 18:00學程式魔法",
        "weight": "bold",
        "align": "center",
        "contents": []
      }
    ]
  }
}
    user_id = 'C1df9decc209425fc5340d43400b48f91'  # 或是群組的ID
    message = TextSendMessage(text)
    try:
        line_bot_api.push_message(user_id, message)
        print('訊息已成功發送！')
    except Exception as e:
        print(f'發送訊息失敗: {e}')

# 啟動定期推送訊息（每天中午12點）
def schedule_message():
    schedule.every().day.at("23:00").do(send_scheduled_message)
    while True:
        schedule.run_pending()
        time.sleep(1)

# 使用 threading 來同時運行 FastAPI 和定期訊息推送
thread = threading.Thread(target=schedule_message)
thread.start()

@app.post("/webhook")
async def webhook(request: Request):
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    
    print("收到的 Webhook 請求：", body.decode('utf-8'))

    try:
        handler.handle(body.decode('utf-8'), signature)
    except InvalidSignatureError:
        return "Invalid signature", 400

    return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.source.type == 'group':  # 檢查是否來自群組
        group_id = event.source.group_id
        print(f"群組 ID: {group_id}")
        
        # 回應群組訊息
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"來自群組的訊息，群組 ID 是：{group_id}")
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
