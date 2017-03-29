class ArgParser:
	def __init__(self, args, pattern):
		self.args = args
		self.pattern = pattern

	def read(self):
		opt = {}
		for p in self.pattern:
			if p in self.args:
				if self.pattern[p]["type"] == "bool":
					opt[self.pattern[p]["name"]] = True
				elif self.pattern[p]["type"] == "int":
					opt[self.pattern[p]["name"]] = int(self.args[self.args.index(p) + 1])
				elif self.pattern[p]["type"] == "float":
					opt[self.pattern[p]["name"]] = float(self.args[self.args.index(p) + 1])
				elif self.pattern[p]["type"] == "str":
					opt[self.pattern[p]["name"]] = self.args[self.args.index(p) + 1]
			else:
				opt[self.pattern[p]["name"]] = self.pattern[p]["default"]

		return opt
