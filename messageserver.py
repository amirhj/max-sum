import Queue, time
from util import Counter


class MessageServer:
	def __init__(self, opt):
		self.opt = opt
		self.clients = None
		#self.logfile = open('results/log.txt', 'w')
		self.agentLog = {}
		self.agentLogTest = {}
		self.timeLog = {}
		self.missPrediction = []
		self.missState = []
		#self.logger = open('logger.txt', 'w')

	
	def load(self, clients):
		self.clients = clients

		for c in self.clients:
			self.agentLog[c] = 0
			self.agentLogTest[c] = 0
			self.timeLog[c] = 0
	
	def send(self, sender, receiver, content, sendtime):
		#if self.opt['log_messages']:
		#	self.logfile.write('%s\n\n\n' % str((sender, receiver, content, sendtime)))

		self.agentLog[sender] += 1
		self.timeLog[sender] += 1

		self.clients[receiver].receive(sender, content)

	def printer(self, c, s):
		if 'Unknown' in c:
			self.missState.append(s)
		if 'Prediction' in c:
			self.missPrediction.append(s)
		print c

	def loggger(self, c):
		self.logger.write('%s\n' %c)
		self.logger.flush()
