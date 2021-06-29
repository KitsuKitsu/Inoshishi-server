from flask import Flask, request, abort
import os
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import ambient
app = Flask(__name__)
# 環境変数の設定(LINEメッセージの送り先IDを事前に登録する)
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
MY_USER_ID = os.environ["MY_USER_ID"]
GROUP_ID = os.environ['GROUP_ID']
DEVELOP_GROUP_ID = os.environ['DEVELOP_GROUP_ID']
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
# LINEbot
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
# 生存確認
@app.route('/monitor')
def monitor():
    return 'alive'
# LINEメッセージ送信
@app.route('/captured')
def captured():
    ID = request.args.get('EndDeviceID', 'None')
    message = TextSendMessage(text=ID+"の罠が作動しました！")
    line_bot_api.push_message(DEVELOP_GROUP_ID, message)
    return 'OK'
# 電圧をambientに送信
@app.route('/voltage')
def voltage():
    voltage = request.args.get('Voltage', 'None')
    AMBIENT_WRITE_KEY = os.environ["AMBIENT_WRITE_KEY"]
    am = ambient.Ambient(30924, AMBIENT_WRITE_KEY)
    res = am.send({'d1': voltage})
    return str(res.status_code)
if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)