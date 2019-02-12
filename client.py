import requests, _thread, sys, time

class Client(object):
	def __init__(self, user, addr):
		self.addr = addr[:-1] if addr.endswith("/") else addr
		self.user = user
	def get(self):
		msgs = requests.get(self.addr).json()
		return msgs
	def send(self, msg):
		res = requests.get(self.addr+"/send?user=%s&msg=%s" % (
				self.user, msg
			)).content
		return True if res == "" else False

class UI(object):
	def __init__(self, user, addr, input_format="[%s]: ", output_format="[%s]: %s"):
		self.client = Client(user, addr)
		self.inpf = input_format
		self.outf = output_format
		self.seen = []
	def msg_thread(self, sleep=0.5):
		while True:
			time.sleep(sleep)
			msgs = self.client.get()[len(self.seen):]
			for i in msgs:
				msg = self.outf % (i['user'], i['msg'])
				sys.stdout.write("\r%s\n%s" % (msg,self.inpf % self.client.user))
				self.seen.append(i)
	def run(self):
		self.client.send("{[%s] joined the chatroom}" % self.client.user)
		self.seen.append("joined")

		_thread.start_new_thread(self.msg_thread, ())
		try:
			while True:
				msg = input(self.inpf % self.client.user)
				self.client.send(msg)
				self.seen.append(msg) # no echo
		except KeyboardInterrupt:
			self.client.send("{[%s] left the chatroom}" % self.client.user)
			self.seen.append("left")

def main():
	user = input("User Name: ")
	addr = input("Server Address: ")
	print("\n\n")

	ui = UI(user, addr)
	ui.run()
main() if __name__ == "__main__" else None