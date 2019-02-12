from flask import Flask, jsonify, request
from flask_cors import CORS

class Server(object):
	def __init__(self, messages=[]):
		self.messages = messages
	def run(self, host="0.0.0.0", port=8000):
		app = Flask(__name__)
		@app.route("/")
		def app_msg():
			return jsonify(self.messages)
		@app.route("/send")
		def app_new():
			name = request.args['user']
			msg = request.args['msg']
			self.messages.append({'user':name,'msg':msg})
			return ""
		app.run(host=host, port=port)

Server().run() if __name__ == "__main__" else None