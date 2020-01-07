from flask import Flask

app = Flask(__name__)

import sharesio.webhooks
import sharesio.configure_bot_api
