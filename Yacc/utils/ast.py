class Node(object):
	def __init__(self, t, *args):
		self.type = t
		self.args = args
		
	def __str__(self):
		s = "type: " + str(self.type) + "\n"
		s += str(self.args)
		return s