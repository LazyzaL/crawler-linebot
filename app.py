# coding=utf-8

# 歡迎使用這個LINE Bot
# 進入LINE應用程式，於官方帳號頁面搜尋
# @717dfpbz
# @也必須輸入
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
                        text=(
                            f'查無此本: {event.message.text}。\n'
                            '請確認輸入是否正確，如果要隨機產生本子，輸入-1即可'
                        )
                    )
                )
            else:
                reply_arr.append(
                    TextSendMessage(
                        text='https://nhentai.net/g/' + hentai.name + '/'
                    )
                )

                res = hentai.getInfo()

                reply_arr.append(
                    ImageSendMessage(
                        original_content_url=res[0],
                        preview_image_url=res[0]
                    )
                )
                reply_arr.append(
                    TextSendMessage(
                        text=(
                            '***若欄位為空白，表示網站亦無該資訊***\n\n'
                            f'主標題(Main Title):\n{res[1]}\n\n'
                            f'副標題(Sub Title):\n{res[2]}\n\n'
                            f'原作(Parodies):\n{res[3]}\n\n'
                            f'角色(Characters):\n{res[4]}\n\n'
                            f'標籤(Tags):\n{res[5]}\n\n'
                            f'作者(Artists):\n{res[6]}\n\n'
                            f'語言(Languages):\n{res[7]}\n\n'
                            f'本子類型(Catogories):\n{res[8]}\n\n'
                            f'頁數(Pages):\n{res[9]}'
                        )
                    )
                )
                reply_arr.append(
                    TextSendMessage(
                        text='若需繼續查詢，請直接輸入文字或號碼，輸入-1可隨機搜尋本子。'
                    )
                )
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
                    text=(
                        f'查無此標籤，亦無此本子: {event.message.text}。\n'
                        '請確認輸入是否正確，並重新輸入，如果要隨機產生本子，輸入-1即可'
                    )
                )
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

        reply_arr.append(
            TextSendMessage(
                text=(
                    '歡迎使用nhentai爬蟲機器人\n'
                    '根據輸入為文字或數字，會自動搜尋標籤或本子\n\n'
                    '更新紀錄可以透過輸入「更新紀錄」查看'
                )
            )
        )
        reply_arr.append(
            TextSendMessage(
                text=(
                    '關鍵字搜尋:\n'
                    '若輸入文字，會搜尋與該文字相關之本子，並列出至多25個今日熱門的結果。\n\n'
                    '範例:\n輸入「paizuri」，會列出25本與「paizuri」相關之今日最熱門的本子\n\n'
                    '支援搜尋多個標籤，只需以空格分隔各個標籤即可，亦支援限定語言。\n\n'
                    '範例:\n輸入「paizuri stockings chinese」，會列出25本與「paizuri」與「stockings」相關，語言為「中文」的本子\n\n'
                    '備註：目前尚無法以中文搜尋'
                )
            )
        )
        reply_arr.append(
            TextSendMessage(
                text=(
                    '本子搜尋:\n'
                    '若輸入數字，會搜尋號碼為該數字的本子，並列出與其相關的資訊。\n\n'
                    '範例:\n輸入「335974」，會搜尋335974這個本子，並列出網址、封面圖片、標題、原作、角色、標籤、作者、語言、類型，頁數等資訊'
                )
            )
        )
        reply_arr.append(
            TextSendMessage(
                text=(
                    '隨機搜尋:\n'
                    '若輸入-1，會隨機搜尋一個本子，並列出其相關資訊。\n\n'
                    '備註:目前尚未實裝篩選系統，尚無法依條件篩選隨機之結果'
                )
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            reply_arr
        )

    if event.message.text == '建議':
        reply_arr = []

        reply_arr.append(
            TextSendMessage(
                text='感謝您使用這個機器人，若有任何建議或回饋，可透過下方資訊聯絡我。'
            )
        )
        reply_arr.append(
            TextSendMessage(
                text=(
                    '聯絡資訊:\n\n'
                    'Discord: Lazy#3082\n'
                    'Instagram: i_am_lazy_boy_\n'
                    'mail: machael1209@gmail.com'
                )
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            reply_arr
        )

    if event.message.text == '更新紀錄':
        reply_arr = []

        reply_arr.append(
            TextSendMessage(
                text=(
                    '更新紀錄：\n\n'
                    '2021/08/16 18:00\n1.新增「本月推薦」功能\n2.新增「更新紀錄」功能\n3.修改「使用說明」部分內容\n\n'
                    '2021/08/19 12:00\n1.修改「使用說明」部分內容\n\n'
                    '2021/10/13 02:30\n1.刪除「本月推薦」功能\n2.重大告知，未來將不會有重大更新'
                )
            )
        )

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
