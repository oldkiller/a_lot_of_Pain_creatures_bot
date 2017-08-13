class Excep(BaseException):
	def __init__(self, arg):
		self.mess = arg

def parse(m_t,bdict):
	try:
		m_t=m_t.split()
		if len(m_t)<len(bdict): 
			raise Excep("количество елементов")
		elif len(m_t)==len(bdict):
			return dict(zip(bdict,m_t))
		else:
			resdict=bdict.copy()
			key=list(resdict.keys())
			rkey=key.copy()
			rkey.reverse()
			for obj in key:
				if resdict[obj]:
					resdict.update({obj:"".join(m_t.pop(0))})
				else:
					break
			for obj in rkey:
				if resdict[obj]:
					resdict.update({obj:"".join(m_t.pop(len(m_t)-1))})
				else:
					resdict.update({obj:" ".join(m_t)})
					break
			return resdict
	except Excep as i:
		print("Проверьте %s запроса."%i.mess)
		return None
	except Exception as i:
		print(i)
		return None