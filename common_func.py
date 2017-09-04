class Except(BaseException):
	def __init__(self, arg):
		self.mess = arg
	def __repr__(self):
		return self.mess
	def __str__(self):
		return self.mess

# def parse(req_str,bdict): 
# 	try:
# 		req_str=req_str.split()
# 		if len(req_str)<len(bdict): 
# 			raise Except("Проверьте количество елементов запроса.")
# 		elif len(req_str)==len(bdict):
# 			return dict(zip(bdict,req_str))
# 		else:
# 			resdict=bdict.copy()
# 			key=list(resdict.keys())
# 			rkey=key.copy()
# 			rkey.reverse()
# 			for obj in key:
# 				if resdict[obj]:
# 					resdict.update({obj:"".join(req_str.pop(0))})
# 				else:
# 					break
# 			for obj in rkey:
# 				if resdict[obj]:
# 					resdict.update({obj:"".join(req_str.pop(len(req_str)-1))})
# 				else:
# 					resdict.update({obj:"_".join(req_str)})
# 					break
# 			return resdict
# 	except Except as i:
# 		raise i
# 	except Exception as e:
# 		raise e

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
