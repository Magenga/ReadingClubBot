from datetime import datetime
import certifi
from pymongo import MongoClient

uri = "mongodb+srv://willy870417:magenga@cluster0.chx5i.mongodb.net/test?retryWrites=true&w=majority&ssl=true&tlsAllowInvalidCertificates=true"

# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# db = client['your_database_name']  # 替換成你的資料庫名稱
# collection = db['message']  # 取得 collection

# # 要插入的資料
# document = {
#     "data": {
#         "index": "num",  # 替換成實際的數字或數據
#         "timestamp": datetime.now(),  # 替換成實際的時間戳記
#         "message": "這是一條測試訊息",  # 替換成實際的訊息
#         "pushTime": datetime.now(),  # 替換成實際的推送時間
#         "immediately": True,  # 替換成實際的布林值
#         "status": "pending"  # 替換成實際的狀態
#     }
# }

# # 插入資料
# result = collection.insert_one(document)

# # 輸出插入的資料 ID
# print("Inserted document ID:", result.inserted_id)
