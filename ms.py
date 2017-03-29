import sys, json
from argparser import ArgParser
from factor_graph import FactorGraph
from scheduler import Scheduler
from variableagent import VariableAgent
from functionagent import FunctionAgent
from messageserver import MessageServer

opt_pattern = { '--temperature': {'name': 'temperature', 'type': 'float', 'default': 1.0},
				'--test-temperature': {'name': 'test-temperature', 'type': 'float', 'default': 3.0},
				'--decay': {'name': 'decay', 'type': 'float', 'default': 1.0009},
				'--alpha': {'name': 'alpha', 'type': 'float', 'default': 0.9},
				'--gamma': {'name': 'gamma', 'type': 'float', 'default': 0.8},
				'-t': {'name': 'tests', 'type': 'int', 'default': 20},
				'-c': {'name': 'convergence_size', 'type': 'int', 'default': 30},
				'-s': {'name': 'standard_deviation', 'type': 'float', 'default': 1.0},
				'--beta': {'name': 'beta', 'type': 'float', 'default': 0.8},
				'-l': {'name': 'lambda', 'type': 'int', 'default': 10}
				}

arg = ArgParser(sys.argv[2:], opt_pattern)
opt = arg.read()

fg = FactorGraph(opt)

fg.load(sys.argv[1])

ms = MessageServer(opt)
agents = {}
for v in fg.variables:
	agent = VariableAgent(v, fg, ms, opt)
	agents[v] = agent

for f in fg.functions:
	agent = FunctionAgent(f, fg, ms, opt)
	agents[f] = agent

scheduler = Scheduler(fg, agents, ms, opt)

scheduler.initialize()
scheduler.run()
scheduler.terminate()