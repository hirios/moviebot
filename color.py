

class Color():
	def __init__(self):
		self.w  = '\033[0m'  # white (normal)
		self.r  = '\033[31m' # red
		self.g  = '\033[32m' # green
		self.o  = '\033[33m' # orange
		self.b  = '\033[34m' # blue
		self.p  = '\033[35m' # purple


	def cr(self, text):
		return self.r + text + self.w


	def cg(self, text):
		return self.g + text + self.w


	def co(self, text):
		return self.o + text + self.w


	def cb(self, text):
		return self.b + text + self.w


	def cp(self, text):
		return self.p + text + self.w								