from agent import Agent

class FunctionAgent(Agent):
	def __init__(self, name, fg, ms, opt):
		Agent.__init__(self, name, fg, ms, opt)

		self.f = self.fg.functions[self.name]
		self.neighbors = self.f.variables
		self.domains = {v:self.fg.variables[v].domain for v in self.neighbors}
		self.q = {v:{value:0 for value in self.domains[v]} for v in self.neighbors}
		self.terminated_neighbors = {v:False for v in self.neighbors}

	def run(self):
		if not self.is_terminated:
			self.read_q_messages()
			self.send_r_messages()
			self.check_termination()

	def read_q_messages(self):
		while not self.message_queue.empty():
			sender, m = self.message_queue.get()
			if m['header'] == 'termination':
				self.terminated_neighbors[sender] = True
			elif m['header'] == 'q':
				q = m['content']
				for v in q:
					self.q[sender][v] = q[v]

	def send_r_messages(self):
		for v in self.neighbors:
			r = {value:0 for value in self.domains[v]}

			other_vars = []
			for vv in self.neighbors:
				if vv != v:
					other_vars.append(vv)

			for value in self.domains[v]:
				indecies = {vv:0 for vv in other_vars}
				max_r = None

				while indecies[other_vars[0]] < len(self.domains[other_vars[0]]):
					values_vector = {vv:self.domains[vv][indecies[vv]] for vv in other_vars}
					values_vector[v] = value

					rr = self.f.get_value(values_vector) + sum(self.q[vv][self.domains[vv][indecies[vv]]] for vv in other_vars)
					if max_r is None or rr > max_r:
						max_r = rr 

					for i in reversed(other_vars):
						if indecies[i] < len(self.domains[i]):
							indecies[i] += 1
							if indecies[i] == len(self.domains[i]):
								if i != other_vars[0]:
									indecies[i] = 0
							else:
								break
				r[value] = max_r

			self.send_message(v, {'header':'r', 'content':r})

	def check_termination(self):
		is_terminated = True
		for s in self.terminated_neighbors.values():
			is_terminated = is_terminated and s
		self.is_terminated = is_terminated