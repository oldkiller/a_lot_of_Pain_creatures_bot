class Except(BaseException):
	def __init__(self, arg):
		self.mess = arg

def parse(req_str,bdict): 
	try:
		req_str=req_str.split()
		if len(req_str)<len(bdict): 
			raise Except("Проверьте количество елементов запроса.")
		elif len(req_str)==len(bdict):
			return dict(zip(bdict,req_str))
		else:
			resdict=bdict.copy()
			key=list(resdict.keys())
			rkey=key.copy()
			rkey.reverse()
			for obj in key:
				if resdict[obj]:
					resdict.update({obj:"".join(req_str.pop(0))})
				else:
					break
			for obj in rkey:
				if resdict[obj]:
					resdict.update({obj:"".join(req_str.pop(len(req_str)-1))})
				else:
					resdict.update({obj:"_".join(req_str)})
					break
			return resdict
	except Except as i:
		raise i
	except Exception as e:
		raise e