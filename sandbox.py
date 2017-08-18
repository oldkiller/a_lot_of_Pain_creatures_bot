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

# string="/mess1 key1 req1 req2 count1"
# string="/mess1 key1 req1 count1 "
# string="/mess1 key1 count1"
# st=parse(string, {"mes":1, "key":1, "req":0, "count":1})

# string="/mess1 req1 req2"
# st=parse(string, {"mes":1, "req":0})

def tt(group):
	import datetime, requests
	day=datetime.datetime.now().isoweekday()
	if day>6: day=1
	week=requests.get("https://api.rozklad.org.ua/v2/weeks").json()["data"]
	req=f"https://api.rozklad.org.ua/v2/groups/{group}/lessons"
	tt=requests.get(req).json()
	ntt=[i for i in tt["data"] if i["day_number"]==str(day) and i["lesson_week"]==str(week)]
	for i in ntt:
		mess =i["lesson_number"]+" "+f"{i['time_start']}-{i['time_end']}\n"
		mess+=i["lesson_name"]+"\n"
		mess+=i["teacher_name"]+"\n"
		mess+=i["lesson_type"]+" "+i["lesson_room"]
		print(mess,"\n")

tt("бс-51")

input()
