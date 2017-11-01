class ParseMessage():
	def __init__(self,text):
		text=text.split()
		self.res=dict(com="",key=[],req=[],num=[])
		self.res["com"]=text[0][1:]
		for i in text[1:]:
			if i[0]=="-" and len(i)>1:
				self.res["key"].append(i[1:])
			elif i.isnumeric():
				self.res["num"].append(int(i))
			else:
				self.res["req"].append(i)
	#TODO flags, ex. words, whose starting at ":"
	def __repr__(self):
		return str(self.res)

	def __str__(self):
		return str(self.res)

	def __call__(self,types,d=None,c=None):
		res=self.res[types] if self.res[types] else [d]
		if c==1: res=res[0]
		if c>1: res=res[:c]
		return res

	def __bool__(self):
		return bool(self.res["key"] or self.res["req"] or self.res["num"])

	def com(self,default=None):
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