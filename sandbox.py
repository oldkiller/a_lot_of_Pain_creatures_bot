class Excep(BaseException):
	def __init__(self, arg):
		self.mess = arg

# def parse(m_t,bdict):
# 	try:
# 		m_t=m_t.split()
# 		if len(m_t)<len(bdict): 
# 			raise Excep("количество елементов")
# 		elif len(m_t)==len(bdict):
# 			return dict(zip(bdict,m_t))
# 		else:
# 			resdict=bdict.copy()
# 			key=list(resdict.keys())
# 			rkey=key.copy()
# 			rkey.reverse()
# 			for obj in key:
# 				if resdict[obj]:
# 					resdict.update({obj:"".join(m_t.pop(0))})
# 				else:
# 					break
# 			for obj in rkey:
# 				if resdict[obj]:
# 					resdict.update({obj:"".join(m_t.pop(len(m_t)-1))})
# 				else:
# 					resdict.update({obj:" ".join(m_t)})
# 					break
# 			return resdict
# 	except Excep as i:
# 		print("Проверьте %s запроса."%i.mess)
# 		return None
# 	except Exception as i:
# 		print(i)
# 		return None
###############################################################################


# new func parse
def parse(p_str, base_dict, sep="_"):
	try:
		pars_list=p_str.split()
		if len(pars_list)<len(base_dict):
			raise Excep("Неполный запрос")
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
			raise Excep("Дерьмо случается")
	except Excep as e:
		print("Err: ", e)
	except Exception as e:
		print(e)


# for forecast
message_text="/weather s kiev"
mess=parse(message_text, {"m":1, "key":1, "city":1})
req=["00","03","06","09","12","15","18","21"]
keys={"s":4, "m":2, "l":1}
res=[i for i in req if i in req[::keys[mess["key"]]]]
for i in res:
	print(i)

input()
