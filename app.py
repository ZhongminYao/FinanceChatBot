from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import mongodb
import re

app = Flask(__name__)

line_bot_api = LineBotApi('W4GASPbfZc5cAZqcezDY8/MeqMqwOf9fGBDN+ARBg2r+Wprku8D6qRVNT435jH1A5fqv6Mq931FAMljSXWi+64yP0V8XTa3dldCvGG/cwa79LUsvCpi/bJYCNnpbIzToTYaD4jbdM2s5GxiG+ctPMwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('52c7933d915bbea23767c2c6f5982c45')
line_bot_api.push_message('Uc3b6aa3866a6acf316e848328f5404ca', TextSendMessage(text='Good to go!'))


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id 
    usespeak=str(event.message.text) 
    line_bot_api.reply_message(event.reply_token,usespeak)
    if re.match('[0-9]{4}[<>][0-9]',usespeak): 
        mongodb.write_user_stock_fountion(stock=usespeak[0:4], bs=usespeak[4:5], price=usespeak[5:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak[0:4]+'successfully saved!'))
        return 0

    
    elif re.match('delete[0-9]{4}',usespeak): 
        mongodb.delete_user_stock_fountion(stock=usespeak[2:])
        line_bot_api.push_message(uid, TextSendMessage(usespeak+'successfully deleted!'))
        return 0

if __name__ == "__main__":
    app.run(debug=True)
