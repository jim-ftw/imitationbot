import web
import requests
from markov_gen import gen_markov
import log_messages
import entities
import hipchat
import json
import re
import logging
import sys

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
        '%(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


urls = ('/.*', 'hooks')

app = web.application(urls, globals())

class hooks:
    def POST(self):
        data = web.data()
        imitationbot(data)

def imitationbot(response):
    msg = json.loads(response)
    msg = entities.HipChatRoomMessage(**msg)
    msg = str(msg)
    logging.info('msg received: ' + msg)
    cmd = msg.split(' ', 1)[1]
    if cmd == 'update':
        log_messages.get_messages()
        log_messages.update_trainer()
    elif cmd[:1] == '@':
        user_name = cmd[1:].split(' ',1)[0]
        user_info = hipchat.get_user_info(user_name)
        msg = gen_markov(user_info['user_id'])
        sent_from = user_info['name']
        hipchat.send_notification(msg, sent_from)
    

if __name__ == '__main__':
    app.run()