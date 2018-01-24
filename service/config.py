'''
Get the configuration from the environment
'''

import os

LINE_REPORT_GENERATOR_PORT = os.environ['LINE_REPORT_GENERATOR_PORT']
LINE_BOT_CHANNEL_ACCESS_TOKEN = os.environ['LINE_BOT_CHANNEL_ACCESS_TOKEN']
LINE_BOT_CHANNEL_SECRET = os.environ['LINE_BOT_CHANNEL_SECRET']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
