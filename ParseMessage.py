class Except(BaseException):
	def __init__(self, arg):
		self.mess = arg
	def __repr__(self):
		return self.mess
	def __str__(self):
		return self.mess

class ParseMessage():
	def __init__(self,text):
		text=text.split()
		self.res=dict(com=[],key=[],req=[],num=[])
		self.res["com"].append(text[0][1:])
		for i in text[1:]:
			if i[0]=="-":
				self.res["key"].append(i[1:])
			elif i.isnumeric():
				self.res["num"].append(int(i))
			else:
				self.res["req"].append(i)

	def __repr__(self):
		return str(self.res)

	def __str__(self):
		return str(self.res)

	def __bool__(self):
		return bool(self.res["key"] or self.res["req"] or self.res["num"])

	def com(self,default):
		return self.res["com"] if self.res["com"] else default

	def key(self,default=None):
		return self.res["key"] if self.res["key"] else [default]

	def req(self,default=None):
		return self.res["req"] if self.res["req"] else [default]

	def num(self,default=None):
		return self.res["num"] if self.res["num"] else [default]
	
	def fkey(self,default=None):
		return self.res["key"][0] if self.res["key"] else default

	def freq(self,default=None):
		return self.res["req"][0] if self.res["req"] else default

	def fnum(self,default=None):
		return self.res["num"][0] if self.res["num"] else default