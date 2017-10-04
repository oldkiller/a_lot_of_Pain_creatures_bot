import requests
import telebot
import re
from ParseMessage import *
from datetime import datetime,timezone,timedelta

bot = telebot.TeleBot("317266897:AAGxt_oKV19_LG_S-xbcTH26eb8ZDGD06Fs")

# KEYS=r"^[a-z]{1}$"
# NUMS=r"^([^A-Za-z])([0-9]){0,}$"
# REQS=r"^([^0-9])([A-Za-z\-0-9]){1,}$"
#Ключ: 1 символ, запрос: все,что больше 1 символа, числа: все только числовые значения

# class ParseMessage():
# 	def __init__(self,txtb,sep="$"):
# 		txt=txtb.split(sep)[0]
# 		txt=txt.split()[1:]
# 		# bd=dict(key=r"^[a-z]{1,2}$", req=r"^([^0-9])([A-Za-z\-0-9]){2,}$", num=r"^([^A-Za-z])([0-9]){0,}$")
# 		bd=dict(key=r"^([^\d])([\w]){1}$", req=r"^([^\d])([\w\-]){2,}$", num=r"^([^A-Za-z])([0-9]){0,}$")
# 		rd={i:[] for i in bd}
# 		if sep in txtb:
# 			rd["req"].append(txtb[1:].split(sep)[1])
# 		for i in bd:
# 			for j in txt:
# 				if re.search(bd[i],j):
# 					rd[i].append(j)
# 		self.rd=rd


# class PWR():
# 	def __init__(self,txt):
# 		txt=txt.split()[1:]
# 		# bd=dict(key=r"^[[:alpha:]]{,2}$", req=r"^([^\d])([\w\-]){2,}$", num=r"^([^[:alpha:]])([\d])$")
# 		# bd=dict(key=r"^[[:alpha:]]{,2}$", req=r"^(^[\d])([\w\-]){2,}$", num=r"^(^[\w\-])([\d]+)$")
# 		# bd=dict(key=r"^[[:alpha:]]{1,2}$", req=r"^([^0-9])([\w\-]){2,}$", num=r"^([^A-Za-z])([0-9]){0,}$")
# 		bd=dict(key=r"^([^\d])([\w]){1}$", req=r"^([^\d])([\w\-]){2,}$", num=r"^([^A-Za-z])([0-9]){0,}$")
# 		rd={i:[] for i in bd}
# 		for i in bd:
# 			for j in txt:
# 				if re.search(bd[i],j):
# 					rd[i].append(j)
# 		self.rd=rd
	
# 	def __repr__(self):
# 		return str(self.rd)
	
# 	def __str__(self):
# 		return str(self.rd)

# 	def __bool__(self):
# 		return bool(self.rd["key"] or self.rd["req"] or self.rd["num"])

# 	def key(self):
# 		return self.rd["key"]
	
# 	def req(self):
# 		return self.rd["req"]
	
# 	def num(self):
# 		return [int(i) for i in self.rd["num"]]

# class PWR():
# 	def __init__(self,txtb,sep="$"):

# 		# bd=dict(key=r"^[a-z]{1,2}$", req=r"^([^0-9])([A-Za-z\-0-9]){2,}$", num=r"^([^A-Za-z])([0-9]){0,}$")
# 		bd=dict(key=r"^([^\d])([\w]){1}$", req=r"^([^\d])([\w\-]){2,}$", num=r"^([^A-Za-z])([0-9]){0,}$")
# 		rd={i:[] for i in bd}
# 		if sep in txtb[1:]:
# 			txt=txtb.split(sep)[0]
# 			txt=txt.split()[1:]
# 			rd["req"].append(txtb[1:].split(sep)[1])
# 		else:
# 			txt=txtb.split()[1:]
# 		for i in bd:
# 			for j in txt:
# 				if re.search(bd[i],j):
# 					rd[i].append(j)
# 		self.rd=rd

# 	def __repr__(self):
# 		return str(self.rd)

# 	def __str__(self):
# 		return str(self.rd)

# 	def __bool__(self):
# 		return bool(self.rd["key"] or self.rd["req"] or self.rd["num"])

# 	def key(self,default=None):
# 		return self.rd["key"] if self.rd["key"] else [default]

# 	def req(self,default=None):
# 		return self.rd["req"] if self.rd["req"] else [default]

# 	def num(self,default=None):
# 		return [int(i) for i in self.rd["num"]] if self.rd["num"] else [default]
	
# 	def fkey(self,default=None):
# 		return self.rd["key"][0] if self.rd["key"] else default

# 	def freq(self,default=None):
# 		return self.rd["req"][0] if self.rd["req"] else default

# 	def fnum(self,default=None):
# 		return int(self.rd["num"][0]) if self.rd["num"] else default

# @bot.message_handler(commands=["test"])
# def test(message):
# 	pm=PWR(message.text,sep="/")
# 	bot.send_message(message.chat.id, str(pm))
# 	# lang="-".join(pm.key())
# 	# text=" ".join(pm.req())
# 	# bot.send_message(message.chat.id, text+" ||| "+lang)

@bot.message_handler(commands=["rex"])
def rex(message):
	pm=ParseMessage(message.text)
	# bot.send_message(message.chat.id, bool(pm))
	bot.send_message(message.chat.id, "key")
	if pm.key():
		bot.send_message(message.chat.id, str(pm.key()))
	bot.send_message(message.chat.id, "num")
	if pm.num():
		bot.send_message(message.chat.id, str(pm.num()))
	bot.send_message(message.chat.id, "req")
	if pm.req():
		bot.send_message(message.chat.id, str(pm.req()))


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
