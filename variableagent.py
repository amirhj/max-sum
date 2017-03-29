from agent import Agent

class VariableAgent(Agent):
	def __init__(self, name, fg, ms, opt):
		Agent.__init__(self, name, fg, ms, opt)

		self.v = self.fg.variables[self.name]
		self.neighbors = self.v.functions
		self.domain = self.v.domain
		self.z = {value:0 for value in self.domain}
		self.r = {f:{value:0 for value in self.domain} for f in self.neighbors}
		self.z_queue = []

	def run(self):
		if not self.is_terminated:
			self.read_r_messages()
			self.send_q_messages()
			self.calculate_z()
			self.check_convergence()

	def read_r_messages(self):
		while not self.message_queue.empty():
			sender, r = self.message_queue.get()
			for value in r:
				self.r[sender][value] = r[value]

	def send_q_messages(self):
		for f in self.neighbors:
			q = {value:0 for value in self.domain}
			for value in self.domain:
				for ff in self.neighbors:
					if f != ff:
						q[value] += self.r[ff][value]
			self.send_message(f, {'header':'q', 'content':q})

	def calculate_z(self):
		for value in self.domain:
			self.z[value] = sum(self.r[f][value] for f in self.neighbors)

	def get_solution(self):
		max_z = None
		solution = None

		for value in self.domain:
			if max_z is None or max_z < self.z[value]:
				max_z = self.z[value]
				solution = value

		return solution

	def check_convergence(self):
		self.z_queue.append(self.z)
		if len(self.z_queue) == self.opt['lambda']:
			converged = True
			for value in self.z:
				value_converged = True

				const_value = self.z_queue[0][value]
				for z in self.z_queue:
					value_converged = z[value] == const_value
					if not value_converged:
						break

				if not value_converged:
					converged = False
					break

			self.is_terminated = converged
			if self.is_terminated:
				for f in self.neighbors:
					self.send_message(f, {'header':'termination', 'content':None})
			else:
				del self.z_queue[0]