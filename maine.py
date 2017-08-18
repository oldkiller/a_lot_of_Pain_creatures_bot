import requests
import datetime
import telebot
import pybooru
import os
from common_func import *
from urllib.request import urlopen
from flask import Flask, request

tele_api = "426351504:AAHomR1jc-m2B7iabRnOFR8OkPTKlkWMIdw"
weath_token = "795819f679706a61cd7938b26ac247af"
yan_api = "r5oUMfysc4C566kI312u_A"

bot = telebot.TeleBot(tele_api)

def bitch(*args):
	bot.send_message(message.chat.id, args)

@bot.message_handler(commands=['start'])
def start(message):
	bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

################## Block responsible for weather requests #####################
def weath_req(types, message):
	try:
		city=message.text.split(" ")
		if city[-1]!="/"+types and len(city[-1])!=0:
			res=requests.get(f"http://api.openweathermap.org/data/2.5/{types}", 
						params={"q":city[1],'units':'metric', 'lang':'ru', "APPID":weath_token})
		else:
			bot.send_message(message.chat.id, "Укажите город, для которого выполняется поиск.")
		data = res.json()
		return data
	except Exception as e:
		pain(e)
		print('Exception', e)

def weath_mess_form(data, mess=""):
	tostr = lambda i: "{0:+3.0f}".format(i)
	mess+= data['weather'][0]['description']+", "
	mess= mess[0].upper()+mess[1:]
	mess+= tostr(data["main"]["temp"])+"°C, "
	mess+= "влажность: "+tostr(data["main"]["humidity"])+"%, "
	mess+= "cкорость ветра: "+tostr(data["wind"]["speed"])+"м/с, "
	mess+= "облачность: "+tostr(data["clouds"]["all"])+"%"
	return mess

@bot.message_handler(commands=['weather'])
def weather(message):
	data = weath_req("weather", message)
	mess = weath_mess_form(data)
	bot.send_message(message.chat.id,mess)

@bot.message_handler(commands=['forecast'])
def forecast(message):
	data = weath_req("forecast", message)
	for i in data["list"]:
		if i["dt_txt"][11:13]=="12" or i["dt_txt"][11:13]=="00":
			mess=i["dt_txt"]+" : "+weath_mess_form(i)
			bot.send_message(message.chat.id, mess)

####################### Block responsible for pictures ########################
@bot.message_handler(commands=["yandere"])
def yandere(message):
	try:
		mess=parse(message.text, {"mess":1, "tag":0, "count":1})
		if not mess: return
		booru=pybooru.Moebooru("yandere", hash_string=yan_api)
		posts=booru.post_list(tags=mess["tag"], limit=int(mess["count"]))
		if posts==[]:
			bot.send_message(message.chat.id, "Пост(ы) не найден(ы).")
		else:
			for post in posts:
				bot.send_photo(message.chat.id, urlopen(post["sample_url"]))
				bot.send_document(message.chat.id, urlopen(post["file_url"]))
	except Exception as e:
		bot.send_message(message.chat.id, e)
  
####################### Block responsible for music	###########################
# https://developer.jamendo.com/v3.0
# 

################################# Secret ######################################

@bot.message_handler(commands=["tt"])
def tt():
	bot.send_message(message.chat.id, message.text)
	# try:
	# 	mess=parse(message.text, {"mess":1, "group":1})
	# 	bot.send_message(message.chat.id, "st 1")
	# 	bitch("start")
	# 	day=datetime.datetime.now().isoweekday()
	# 	if day>6: day=1
	# 	week=requests.get("https://api.rozklad.org.ua/v2/weeks").json()["data"]
	# 	bitch(day," ", week)
	# 	tt=requests.get(f"https://api.rozklad.org.ua/v2/groups/{mess['group']}/lessons").json()
	# 	ntt=[i for i in tt["data"] if i["day_number"]==str(day) and i["lesson_week"]==str(week)]
	# 	bitch(tt,"\n",ntt)
	# 	if not ntt:
	# 		bot.send_message(message.chat.id, "Похоже, день свободен")
	# 	for i in ntt:
	# 		mes =i["lesson_number"]+" "+f"{i['time_start']}-{i['time_end']}\n"
	# 		mes+=i["lesson_name"]+"\n"+i["teacher_name"]+"\n"
	# 		mes+=i["lesson_type"]+" "+i["lesson_room"]
	# 		bot.send_message(message.chat.id, mes)
	# except Exception as e:
	# 	bot.send_message(message.chat.id, e)

# def kpi():
# 	try:
# 		mess=parse(message.text, {"mess":1, "group":0})
# 		sear=requests.get("http://api.rozklad.hub.kpi.ua/groups/", params={"search":mess["group"]})
# 		sear=sear.json()
# 		g_id=[i["id"] for i in sear["resultss"] if i ["name"]==mess["group"]]
# 		# if 
# 		tt=requests.get("http://api.rozklad.hub.kpi.ua/groups/%s/timetable/"%g_id[0])
# 		tt=tt.json()
# 		bot.send_message(message.chat.id, tt)

# 	except Exception as e:
# 		bot.send_message(message.chat.id, e)

####################### Block responsible for webhooks ########################
server = Flask(__name__)

@server.route("/bot", methods=['POST'])
def getMessage():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "!", 200

@server.route("/")
def webhook():
	bot.remove_webhook()
	bot.set_webhook(url="https://murmuring-cove-94118.herokuapp.com/bot")
	return "!", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
