import web
import requests
import markov_gen
import log_messages
import entities
import json


urls = ('/.*', 'hooks')

app = web.application(urls, globals())

class hooks:
    def POST(self):
        data = web.data()
        imitationbot(data)

def respond(msg):
    pass

def imitationbot(response):
    msg = json.load(response)
    msg = entities.HipChatRoomMessage(**msg)
    print msg

if __name__ == '__main__':
    app.run()

