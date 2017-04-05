from functions import Functions
import json

class FactorGraph:
	def __init__(self, opt):
		self.variables = {}
		self.functions = {}
		self.constants = {}

		self.opt = opt

	def load(self, graph):
		self.fg = json.loads(open(graph, 'r').read())

		# loading functions
		for f in self.fg['functions']:
			self.functions[f['name']] = Function(f['name'], f['variables'], self)

		# loading variables
		for v in self.fg['variables']:
			functions = []
			neighbours = set()

			for f in self.functions:
				if v['name'] in self.functions[f].variables:
					functions.append(f)
					for n in self.functions[f].variables:
						if n != v['name']:
							neighbours.add(n)
			neighbours = list(neighbours)

			value = v['domain']['min']
			domain = []
			while value <= v['domain']['max']:
				domain.append(value)
				value += v['domain']['step']

			self.variables[v['name']] = Variable(v['name'], domain, functions, neighbours)

		# loading constants
		for c in self.fg['constants']:
			self.constants[c['name']] = c['value']

class Variable:
	def __init__(self, name, domain, functions, neighbours):
		self.name = name
		self.domain = domain
		self.functions = functions
		self.value_index = 0
		self.neighbours = neighbours
		self.domain_size = len(domain)

	def get_value(self):
		return self.domain[self.value_index]

	def set_value(self, value):
		self.value_index = self.domain.index(value)

class Function:
	def __init__(self, name, variables, fg):
		self.name = name
		self.variables = variables
		self.fg = fg

	def get_value(self, values):
		function = Functions(self.fg)
		return function.calculate(self.name, values)
