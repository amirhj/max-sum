import sys, os, json
from datetime import datetime

class Scheduler:
	def __init__(self, fg, agents, ms, opt):
		self.fg = fg
		self.agents = agents
		self.opt = opt
		self.ms = ms

	def initialize(self):
		self.ms.load(self.agents)

	def run(self):
		terminated = False
		while not terminated:
			terminated = True
			for a in self.agents:
				self.agents[a].run()
				terminated = terminated and self.agents[a].is_terminated

				if terminated:
					print 'agent %s terminated' % a

	def terminate(self):
		for v in self.fg.variables:
			print 'variable %s = %f' % (v, self.agents[v].get_solution())