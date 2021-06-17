# 歡迎使用這個LINE Bot
# 進入LINE應用程式，於官方帳號頁面搜尋
# @717dfpbz
# @也必須輸入
from __future__ import unicode_literals
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import configparser
import crawler_for_linebot

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


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
    def booksearch():
        hentai = crawler_for_linebot.book(event.message.text)

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
                    TextSendMessage(
                        text='查無此本: ' + event.message.text + '。\n請確認輸入是否正確，如果要隨機產生本子，輸入-1即可')
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
                    text='若需繼續查詢，請直接輸入文字或號碼，輸入-1可隨機搜尋本子。'))
                line_bot_api.reply_message(
                    event.reply_token,
                    reply_arr
                )

    def tagsearch():
        hentai = crawler_for_linebot.tag(event.message.text)

        reply_arr = []

        if hentai.checkConnection() == False:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='查無此標籤，亦無此本子: ' + event.message.text + '。\n請確認輸入是否正確，並重新輸入，如果要隨機產生本子，輸入-1即可')
            )
        else:
            reply_arr.append(TextSendMessage(
                text=hentai.getInfo()))
            reply_arr.append(TextSendMessage(
                text='若需繼續查詢，請直接輸入文字或號碼，輸入-1可隨機搜尋本子。'))

            line_bot_api.reply_message(
                event.reply_token,
                reply_arr
            )

    if event.message.text == '使用說明':
        reply_arr = []

        reply_arr.append(TextSendMessage(
            text='歡迎使用nhentai爬蟲機器人\n根據輸入為文字或數字，會自動搜尋標籤或本子'))
        reply_arr.append(TextSendMessage(
            text='標籤搜尋:\n若輸入文字，會搜尋名稱為該文字的標籤，並列出25個有此標籤的本子。\n\n範例:\n輸入「paizuri」，會列出25本標籤中包含「paizuri」的本子\n\n支援搜尋多個標籤，只需以空格分隔各個標籤即可，亦支援限定語言。\n\n範例:\n輸入「paizuri stockings chinese」，會列出25本標籤中包含「paizuri」與「stockings」，語言為「中文」的本子\n\n備註:目前僅支援輸入的語言為英文，中文部分尚未完善'))
        reply_arr.append(TextSendMessage(
            text='本子搜尋:\n若輸入數字，會搜尋號碼為該數字的本子，並列出與其相關的資訊。\n\n範例:\n輸入「335974」，會搜尋335974這個本子，並列出網址、封面圖片、標題、原作、角色、標籤、作者、語言、類型，頁數等資訊'))
        reply_arr.append(TextSendMessage(
            text='隨機搜尋:\n若輸入-1，會隨機搜尋一個本子，並列出其相關資訊。\n\n備註:目前尚未實裝篩選系統，尚無法依條件篩選隨機之結果'))

        line_bot_api.reply_message(
            event.reply_token,
            reply_arr
        )

    if event.message.text == '建議':
        reply_arr = []

        reply_arr.append(TextSendMessage(
            text='感謝您使用這個機器人，若有任何建議或回饋，可透過下方資訊聯絡我。'))
        reply_arr.append(TextSendMessage(
            text='聯絡資訊:\n\nDiscord: Lazy#3082\nInstagram: i_am_lazy_boy_\nmail: machael1209@gmail.com'))

        line_bot_api.reply_message(
            event.reply_token,
            reply_arr
        )

    if str(event.message.text).isdigit() or event.message.text == '-1':
        booksearch()
    else:
        tagsearch()


if __name__ == "__main__":
    app.run()
