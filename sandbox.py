import requests
import telebot
import re
from common_func import *

bot = telebot.TeleBot("317266897:AAGxt_oKV19_LG_S-xbcTH26eb8ZDGD06Fs")

# KEYS=r"^[a-z]{1}$"
# NUMS=r"^([^A-Za-z])([0-9]){0,}$"
# REQS=r"^([^0-9])([A-Za-z\-0-9]){1,}$"
#Ключ: 1 символ, запрос: все,что больше 1 символа, числа: все только числовые значения

class PWR():
	def __init__(self,txt):
		txt=txt.split()[1:]
		bd=dict(key=r"^[a-z]{1}$", req=r"^([^0-9])([A-Za-z\-0-9]){1,}$", num=r"^([^A-Za-z])([0-9]){0,}$")
		rd={i:[] for i in bd}
		for i in bd:
			for j in txt:
				if re.search(bd[i],j):
					rd[i].append(j)
		self.rd=rd
	
	def __repr__(self):
		return str(self.rd)
	
	def __str__(self):
		return str(self.rd)
	
	def key(self):
		return self.rd["key"]
	
	def req(self):
		return self.rd["req"]
	
	def num(self):
		return [int(i) for i in self.rd["num"]]
# def parse_rex(txt,sep="_",**bd):
# 	txt=txt.split()[1:]
# 	rbd={i:[] for i in bd}
# 	for i in bd:
# 		for j in txt:
# 			if re.search(bd[i],j):
# 				rbd[i].append(j)
# 	return rbd

@bot.message_handler(commands=["rex"])
def rex(message):
	pm=PWR(message.text)
	for _ in range(5):
		bot.send_message(message.chat.id, pm.key())
		bot.send_message(message.chat.id, pm.num())


if __name__=="__main__":
	bot.polling(none_stop=True)

# def parse(p_str, base_dict, sep="_"):
# 	try:
# 		pars_list=p_str.split()
# 		if len(pars_list)<len(base_dict):
# 			raise Excep("Неполный запрос")
# 		if len(pars_list)==len(base_dict):
# 			return dict(zip(base_dict,pars_list))
# 		if len(pars_list)==sum(base_dict.values()):
# 			for i in base_dict:
# 				up=[pars_list.pop(0) for i in range(base_dict[i])]
# 				base_dict.update({i:sep.join(up)})
# 			return base_dict
# 		if 0 in base_dict.values():
# 			key=list(base_dict.keys())
# 			key.reverse()
# 			for obj in base_dict:
# 				if base_dict[obj]:
# 					up=[pars_list.pop(0) for _ in range(base_dict[obj])]
# 					base_dict.update({obj:sep.join(up)})
# 				else:
# 					break
# 			for obj in key:
# 				if base_dict[obj]:
# 					up=[pars_list.pop() for _ in range(base_dict[obj])]
# 					base_dict.update({obj:sep.join(up)})
# 				else:
# 					base_dict.update({obj:sep.join(pars_list)})
# 					break
# 			return base_dict
# 		else:
# 			raise Excep("Дерьмо случается")
# 	except Excep as e:
# 		print("Err: ", e)
# 	except Exception as e:
# 		print(e)

# def test(p_str, *param, sep="_", **bdict):
# 	try:
# 		a=int(bdict["mess"][0])
# 	except:
# 		bdict.update({"mess":bdict["mess"][1]})
# 	else:
# 		bdict.update({"mess":a})
# 	print(bdict, list(param))

# test("sss","lol",mess=["u",2])
