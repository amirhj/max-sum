import Queue
from datetime import datetime

class Agent:
	def __init__(self, name, fg, ms, opt):
		self.name = name
		self.fg = fg
		self.ms = ms
		self.opt = opt

		self.is_terminated = False
		self.neighbors = []
		self.message_queue = Queue.Queue()

	def send_message(self, receiver, content):
		self.ms.send(self.name, receiver, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

	def receive(self, sender, content):
		self.message_queue.put((sender, content))

	def run(self):
		pass
