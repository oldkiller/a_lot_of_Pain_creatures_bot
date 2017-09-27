import re

class Except(BaseException):
	def __init__(self, arg):
		self.mess = arg
	def __repr__(self):
		return self.mess
	def __str__(self):
		return self.mess

# Захреначить все на регулярках, что ли?
# Спасибо RegEx, что прокачали мой код.
class PWR():
	def __init__(self,txt):
		txt=txt.split()[1:]
		bd=dict(key=r"^[a-z]{1,2}$", req=r"^([^0-9])([A-Za-z\-0-9]){2,}$", num=r"^([^A-Za-z])([0-9]){0,}$")
		rd={i:[] for i in bd}
		for i in bd:
			for j in txt:
				if re.search(bd[i],j):
					rd[i].append(j)
		# if not rd["req"]:
		# 	Except("Пустое тело запроса.")
		self.rd=rd

	def __repr__(self):
		return str(self.rd)

	def __str__(self):
		return str(self.rd)

	def __bool__(self):
		return bool(self.rd["key"] or self.rd["req"] or self.rd["num"])

	def key(self,default=None):
		return self.rd["key"] if self.rd["key"] else [default]

	def req(self,default=None):
		return self.rd["req"] if self.rd["req"] else [default]

	def num(self,default=None):
		return [int(i) for i in self.rd["num"]] if self.rd["num"] else [default]
	
	def fkey(self,default=None):
		return self.rd["key"][0] if self.rd["key"] else default

	def freq(self,default=None):
		return self.rd["req"][0] if self.rd["req"] else default

	def fnum(self,default=None):
		return int(self.rd["num"][0]) if self.rd["num"] else default

################################################################################

def parse(p_str, base_dict, sep="_"):
	try:
		pars_list=p_str.split()
		if len(pars_list)<len(base_dict):
			raise Except("Неполный запрос")
		if len(pars_list)==len(base_dict):
			return dict(zip(base_dict,pars_list))
		if len(pars_list)==sum(base_dict.values()):
			for i in base_dict:
				up=[pars_list.pop(0) for i in range(base_dict[i])]
				base_dict.update({i:sep.join(up)})
			return base_dict
		if 0 in base_dict.values():
			key=list(base_dict.keys())
			key.reverse()
			for obj in base_dict:
				if base_dict[obj]:
					up=[pars_list.pop(0) for _ in range(base_dict[obj])]
					base_dict.update({obj:sep.join(up)})
				else:
					break
			for obj in key:
				if base_dict[obj]:
					up=[pars_list.pop() for _ in range(base_dict[obj])]
					base_dict.update({obj:sep.join(up)})
				else:
					base_dict.update({obj:sep.join(pars_list)})
					break
			return base_dict
		else:
			raise Except("Дерьмо случается")
	except Except as i:
		raise i
	except Exception as e:
		raise e

def parse2(p_str, sep="_", **base_dict):
	try:
		pars_list=p_str.split()
		if len(pars_list)<len(base_dict):
			raise Except("Неполный запрос")
		if len(pars_list)==len(base_dict):
			return dict(zip(base_dict,pars_list))
		if len(pars_list)==sum(base_dict.values()):
			for i in base_dict:
				up=[pars_list.pop(0) for i in range(base_dict[i])]
				base_dict.update({i:sep.join(up)})
			return base_dict
		if 0 in base_dict.values():
			key=list(base_dict.keys())
			key.reverse()
			for obj in base_dict:
				if base_dict[obj]:
					up=[pars_list.pop(0) for _ in range(base_dict[obj])]
					base_dict.update({obj:sep.join(up)})
				else:
					break
			for obj in key:
				if base_dict[obj]:
					up=[pars_list.pop() for _ in range(base_dict[obj])]
					base_dict.update({obj:sep.join(up)})
				else:
					base_dict.update({obj:sep.join(pars_list)})
					break
			return base_dict
		else:
			raise Except("Дерьмо случается")
	except Except as i:
		raise i
	except Exception as e:
		raise e
