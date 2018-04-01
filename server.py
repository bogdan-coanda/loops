import http.server
import socketserver
import os

PORT = 8003

#web_dir = os.path.join(os.path.dirname(__file__), 'web')
#os.chdir(web_dir)

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
	#protocol_version = "HTTP/1.1"
	def end_headers(self):
		self.send_my_headers()
		http.server.SimpleHTTPRequestHandler.end_headers(self)
	
	def send_my_headers(self):
		self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
		self.send_header("Pragma", "no-cache")
		self.send_header("Expires", "0")

Handler = MyHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

