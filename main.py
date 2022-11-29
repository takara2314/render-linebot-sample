import os

from fastapi import FastAPI, Header, HTTPException, Request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# FastAPIのインスタンス
app = FastAPI()

# LINEのアクセストークンとチャネルシークレットを環境変数から取得
line_bot_api = LineBotApi(os.environ["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(os.environ["LINE_CHANNEL_SECRET"])

# / にGETリクエストが来たときに呼ばれる関数
@app.get("/")
def home():
    return {"message": "こんにちは、世界！"}

# /callback にPOSTリクエストが来たときに呼ばれる関数
@app.post("/callback")
async def callback(request: Request, x_line_signature=Header(...)):
    # リクエストボディを取得
    body = await request.body()

    try:
        # 署名検証
        handler.handle(body, x_line_signature)
    except InvalidSignatureError:
        # 署名検証に失敗した場合はエラーを返す
        raise HTTPException(status_code=400, detail="InvalidSignatureError")

    return {"message": "OK"}

# テキストメッセージを受け取ったときに呼ばれる関数
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 受け取ったメッセージ
    message = event.message.text
    # 返信するメッセージ
    res = ""

    if message == "こんにちは":
        res = "ハロー！"
    elif message == "ありがとう":
        res = "どういたしまして！"
    else:
        res = "わかりません"

    # メッセージをそのまま返す
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=res)
    )
