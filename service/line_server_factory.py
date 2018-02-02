'''
Factory in charge of delivering a server instance on demand
Define handlers to interact with the Line Bot
'''

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from service.config import LINE_BOT_CHANNEL_ACCESS_TOKEN, LINE_BOT_CHANNEL_SECRET, DB_NAME, DB_USER, DB_PASSWORD, \
    DB_HOST
from service.helpers.psycopg2_wrapper import ResilientConnection

MAIN_CALLBACK_RESOURCE = "/report_callback"


class LineServerFactory:
    def get_instance(self):

        database = ResilientConnection(
            db_name=DB_NAME,
            db_user=DB_USER,
            db_password=DB_PASSWORD,
            db_host=DB_HOST,
        )

        line_server_instance = Flask(__name__)
        self.define_line_server_handlers(line_server_instance)
        return line_server_instance

    @staticmethod
    def define_line_server_handlers(line_server_instance):

        line_bot_api = LineBotApi(LINE_BOT_CHANNEL_ACCESS_TOKEN)
        handler = WebhookHandler(LINE_BOT_CHANNEL_SECRET)

        @line_server_instance.route(MAIN_CALLBACK_RESOURCE, methods=['POST'])
        def callback():
            # get X-Line-Signature header value
            signature = request.headers['X-Line-Signature']

            # get request body as text
            body = request.get_data(as_text=True)
            line_server_instance.logger.info("Request body: " + body)

            # handle webhook body
            try:
                handler.handle(body, signature)
            except InvalidSignatureError:
                abort(400)

            response = {
                "message": "OK"
            }

            return response

        @handler.add(MessageEvent, message=TextMessage)
        def handle_message(event):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text))
