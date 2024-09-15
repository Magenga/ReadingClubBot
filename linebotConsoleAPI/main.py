from fastapi.exceptions import HTTPException
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import requests
from pymongo import MongoClient
import certifi
from datetime import datetime
# http://localhost:8000/static/message.html
app = FastAPI()

# MongoDB URI
# uri = "mongodb+srv://willy870417:<your_password>@cluster0.chx5i.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(uri, tlsCAFile=certifi.where())
# db = client.your_database_name
# collection = db.message

# 設定允許的來源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許所有來源
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有方法
    allow_headers=["*"],  # 允許所有頭部
)

# 將靜態文件夾掛載到 "/static" 路徑
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# 接收來自前端的訊息
# @app.post("/send-message/")
# async def receive_message(request: Request):
#     data = await request.json()
#     sender = data.get('sender')
#     message = data.get('message')
    
#     # 準備要轉發到 Line Bot API 的資料
#     payload = {
#         'sender': sender,
#         'message': message
#     }
    
#     # 發送 POST 請求到 Line Bot API
#     linebot_api_url = "https://readingclub-production.up.railway.app/linebot"  # Line Bot API 的路徑
#     try:
#         response = requests.post(linebot_api_url, json=payload)
#         if response.status_code == 200:
#             return {"status": "success", "message": "訊息已轉發到 Line Bot API"}
#         else:
#             return {"status": "error", "message": "無法轉發訊息"}
#     except Exception as e:
#         return {"status": "error", "message": f"發送到 Line Bot API 時出錯: {e}"}
    
@app.post("/send-message/")
async def send_message(request: Request):
    try:
        data = await request.json()
        document = {
            "data": {
                "index": None,  # MongoDB 自動生成
                "timestamp": datetime.utcnow().isoformat(),
                "message": data.get('message'),
                "pushTime": data.get('pushTime'),
                "immediately":  data.get('immediately'),
                "status": "待發送"  # 預設狀態
            }
        }
        print(document)
        # result = collection.insert_one(document)
        # return {"message": "訊息已成功發送", "id": str(result.inserted_id)}
        if(data.get('immediately') == True):
            # 發送 POST 請求到 Line Bot API
            linebot_api_url = "https://readingclub-production.up.railway.app/linebot"  # Line Bot API 的路徑
            try:
                response = requests.post(linebot_api_url, json=document)
                if response.status_code == 200:
                    return {"status": "success", "message": "訊息已轉發到 Line Bot API"}
                else:
                    return {"status": "error", "message": "無法轉發訊息"}
            except Exception as e:
                return {"status": "error", "message": f"發送到 Line Bot API 時出錯: {e}"}
        return {"message": "訊息已成功發送"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))