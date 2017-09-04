import postgresql
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

@bot.message_handler(commands=["start"])
def start(message):
	bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(commands=["help"])
def helps(message):
	help_mess="""
	/weather <city> - Узнать погоду в <city>
	/forecast <key> <city> - Узнать прогноз погоды в <city>, <key> - может принимать значения s,m,l
	/yandere <tag> <count> - Поиск изображений на yande.re, <tag> - теги для поиска, <count> - количество
	/timetable <group> - <group> - група, для которой берется рассписание
	help is coming
	"""
	bot.send_message(message.chat.id, help_mess)

################## Block responsible for weather requests #####################
def weath_req(types,city):
	try:
		req=f"http://api.openweathermap.org/data/2.5/{types}"
		param={"q":city,"units":"metric","lang":"ru","APPID":weath_token}
		data=requests.get(req, params=param).json()
		return data
	except Exception as e:
		bot.send_message(message.chat.id, e)

def weath_reply(data, mess=""):
	tostr = lambda i: "{0:+3.0f}".format(i)
	mess += data['weather'][0]['description'].capitalize()+", "
	mess += tostr(data["main"]["temp"])+"°C, "
	mess += "влажность: "+tostr(data["main"]["humidity"])+"%, "
	mess += "cкорость ветра: "+tostr(data["wind"]["speed"])+"м/с, "
	mess += "облачность: "+tostr(data["clouds"]["all"])+"%"
	return mess

@bot.message_handler(commands=['weather'])
def weather(message):
	pmes=parse(message.text, {"mess":1, "city":0})
	data=weath_req("weather", pmes["city"])
	bot.send_message(message.chat.id,weath_reply(data))

@bot.message_handler(commands=["forecast"])
def forecast(message):
	pmes=parse(message.text, {"mess":1, "key":1, "city":0})
	data=weath_req("forecast", pmes["city"])
	tlist=["00","03","06","09","12","15","18","21"]
	tkey={"s":4, "m":2, "l":1}
	#tkey=dict(s=4, m=2, l=1)
	res=[i for i in data["list"] if i["dt_txt"][11:13] in tlist[::tkey[pmes["key"]]]]
	for i in res:
		bot.send_message(message.chat.id, i["dt_txt"]+" : "+weath_reply(i))

####################### Block responsible for pictures ########################
@bot.message_handler(commands=["yandere"])
def yandere(message):
	try:
		mess=parse(message.text, {"mess":1, "tag":0, "count":1})
		if not mess: raise Except("Неполное тело запроса")
		booru=pybooru.Moebooru("yandere", hash_string=yan_api)
		#booru=pybooru.Moebooru(mess["mess"][1:])#, hash_string=yan_api)
		posts=booru.post_list(tags=mess["tag"], limit=int(mess["count"]))
		if posts==[]: raise Except("Пост(ы) не найден(ы).")
		for post in posts:
			bot.send_photo(message.chat.id, urlopen(post["sample_url"]))
			bot.send_document(message.chat.id, urlopen(post["file_url"]))
	except Except as i:
		bot.send_message(message.chat.id, i)
	except Exception as e:
		bot.send_message(message.chat.id, e)
  
####################### Block responsible for music	###########################
# https://developer.jamendo.com/v3.0

################################### DB ########################################
@bot.message_handler(commands=["db"])
def bds(message):
	bot.send_message(message.chat.id, os.environ["DATABASE_URL"])
	con=postgresql.open(os.environ["DATABASE_URL"])
	con.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, login CHAR(64)")
	con.commit()
	con.close()

	bot.send_message(message.chat.id, os.environ["DATABASE_URL"])

################################# Secret ######################################
#TODO Ключи для рассписания: { n - now, d - day, t - tomorow, w - week, f - full }
@bot.message_handler(commands=["timetable"])
def timetable(message):
	try:
		mess=parse(message.text, {"mess":1, "group":1})
		day=datetime.datetime.now().isoweekday()
		if day>6: day=1
		week=requests.get("https://api.rozklad.org.ua/v2/weeks").json()["data"]
		tt=requests.get(f"https://api.rozklad.org.ua/v2/groups/{mess['group']}/lessons").json()
		ntt=[i for i in tt["data"] if i["day_number"]==str(day) and i["lesson_week"]==str(week)]
		if not ntt:
			bot.send_message(message.chat.id, "Похоже, день свободен")
		for i in ntt:
			mes =i["lesson_number"]+" "+f"{i['time_start']}-{i['time_end']}\n"
			mes+=i["lesson_name"]+"\n"+i["teacher_name"]+"\n"
			mes+=i["lesson_type"]+" "+i["lesson_room"]
			bot.send_message(message.chat.id, mes)
	except Exception as e:
		bot.send_message(message.chat.id, e)

@bot.message_handler(commands=["timetable2"])
def timetable2(message):
	try:
		api_link="https://api.rozklad.org.ua/v2/"
		mess=parse2(message.text, mess=1, key=1, group=1)
		day=datetime.datetime.now().isoweekday()
		if day>6: day=1
		week=requests.get(api_link+"weeks").json()["data"]
		tt=requests.get(api_link+f"groups/{mess['group']}/lessons").json()
		key={"d":[[day],[week]], "t":[[day+1],[week]], "w":[range(1,7),[week]], "f":[range(1,7),range(1,3)]}
		ntt=[i for i in tt["data"] if int(i["day_number"]) in key[mess["key"]][0] and int(i["lesson_week"]) in key[mess["key"]][1] ]
		if not ntt:
			bot.send_message(message.chat.id, "Похоже, день свободен")
		for i in ntt:
			mes =i["lesson_number"]+" "+f"{i['time_start']}-{i['time_end']}\n"
			mes+=i["lesson_name"]+"\n"+i["teacher_name"]+"\n"
			mes+=i["lesson_type"]+" "+i["lesson_room"]
	except Exception as e:
		bot.send_message(message.chat.id, e)

# TODO Ключи по умолчанию.
# TODO переводчика добавить
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
