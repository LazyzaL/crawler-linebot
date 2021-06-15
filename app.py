from __future__ import unicode_literals
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import configparser
import crawler_for_linebot

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def show(event):
    hentai = crawler_for_linebot.view(event.message.text)
    reply_arr = []

    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        if event.message.text == '-1':
            while True:
                hentai.randombook()
                if hentai.checkConnection() == True:
                    break

        if hentai.checkConnection() == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='查無此本。\n請確認輸入是否正確，如果要隨機產生本子，輸入-1即可。')
            )
        else:
            reply_arr.append(TextSendMessage(
                text='https://nhentai.net/g/' + hentai.name + '/'))
            reply_arr.append(ImageSendMessage(
                original_content_url=hentai.getInfo()[0],
                preview_image_url=hentai.getInfo()[0]))
            reply_arr.append(TextSendMessage(
                text='***若欄位為空白，表示網站亦無該資訊***\n\n主標題(Main Title):\n{}\n\n副標題(Sub Title):\n{}\n\n原作(Parodies):\n{}\n\n角色(Characters):\n{}\n\n標籤(Tags):\n{}\n\n作者(Artists):\n{}\n\n語言(Languages):\n{}\n\n本子類型(Catogories):\n{}\n\n頁數(Pages):\n{}'.format(
                    hentai.getInfo()[1],
                    hentai.getInfo()[2],
                    hentai.getInfo()[3],
                    hentai.getInfo()[4],
                    hentai.getInfo()[5],
                    hentai.getInfo()[6],
                    hentai.getInfo()[7],
                    hentai.getInfo()[8],
                    hentai.getInfo()[9])))
            reply_arr.append(TextSendMessage(
                text='若需查詢下一本，請直接輸入號碼，輸入-1可隨機搜尋本子。'))
            line_bot_api.reply_message(
                event.reply_token,
                reply_arr
            )


if __name__ == "__main__":
    app.run()
