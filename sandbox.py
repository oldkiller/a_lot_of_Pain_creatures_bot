class Excep(BaseException):
	def __init__(self, arg):
		self.mess = arg

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

def test(p_str, *param, sep="_", **bdict):
	try:
		a=int(bdict["mess"][0])
	except:
		bdict.update({"mess":bdict["mess"][1]})
	else:
		bdict.update({"mess":a})
	print(bdict, list(param))

test("sss","lol",mess=["u",2])


input()
