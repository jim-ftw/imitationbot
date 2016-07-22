import web
import socket

urls = ('/.*', 'hooks')

app = web.application(urls, globals())

class hooks:
    def POST(self):
        data = web.data()
        print
        print 'DATA RECEIVED:'
        print data
        print
        return 'OK'

if __name__ == '__main__':
    hostname = socket.gethostbyname(socket.gethostname())

    fqdn = socket.getfqdn()
    
    print hostname
    print fqdn
    app.run()