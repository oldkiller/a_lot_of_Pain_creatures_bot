import postgresql
import requests
import telebot
import pybooru
import os
from datetime import datetime,timezone,timedelta
from urllib.request import urlopen
from flask import Flask, request
from ParseMessage import *

tele_api = "426351504:AAHomR1jc-m2B7iabRnOFR8OkPTKlkWMIdw"
weath_token = "795819f679706a61cd7938b26ac247af"
yan_api = "r5oUMfysc4C566kI312u_A"
translate = "trnsl.1.1.20170926T012014Z.3f5cb4c22d376499.4dc04c7f837aa68cb2ca57420651ba47d1548711"

bot = telebot.TeleBot(tele_api)

@bot.message_handler(commands=["start"])
def start(message):
	bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(commands=["help"])
def helps(message):
	help_mess="""
	/weather <city> - Узнать погоду в <city>
	/forecast <key> <city> - Узнать прогноз погоды в <city>, 
	<key> - может принимать значения -s,-m,-l
	/yandere <tag> <count> - Поиск изображений на yande.re, 
	<tag> - теги для поиска, <count> - количество
	/timetable <key> <group> - <group> - група, для которой берется рассписание
	Ключи для рассписания: {d - day, t - tomorow, w - week, f - full}
	help is coming
	"""
	bot.send_message(message.chat.id, help_mess)

###############################################################################
def weath_req(types,city):
	req=f"http://api.openweathermap.org/data/2.5/{types}"
	param={"q":city,"units":"metric","lang":"ru","APPID":weath_token}
	return requests.get(req, params=param).json()

def weath_reply(data, mess=""):
	tostr = lambda i: "{0:+3.0f}".format(i)
	mess += data["weather"][0]["description"].capitalize()+", "
	mess += tostr(data["main"]["temp"])+"°C, "
	mess += "влажность: "+tostr(data["main"]["humidity"])+"%, "
	mess += "cкорость ветра: "+tostr(data["wind"]["speed"])+"м/с, "
	mess += "облачность: "+tostr(data["clouds"]["all"])+"%"
	return mess

@bot.message_handler(commands=["weather"])
def weather(message):
	try:
		txt=ParseMessage(message.text)
		if not txt: Except("Неполное тело запроса")
		data=weath_req("weather", txt.freq())
		bot.send_message(message.chat.id,weath_reply(data))
	except Exception as e:
		bot.send_message(message.chat.id, e)

@bot.message_handler(commands=["forecast"])
def forecast(message):
	try:
		txt=ParseMessage(message.text)
		if not txt: Except("Неполное тело запроса")
		data=weath_req("forecast", txt.freq())
		tlist=["00","03","06","09","12","15","18","21"]
		tkey={"s":4, "m":2, "l":1}
		req_key=tkey[txt.fkey("s")]
		res=[i for i in data["list"] if i["dt_txt"][11:13] in tlist[::req_key]]
		for i in res[:int(txt.fnum(5)*(8/req_key))]:
			bot.send_message(message.chat.id, i["dt_txt"]+" : "+weath_reply(i))
	except Exception as e:
		bot.send_message(message.chat.id, e)

###############################################################################
@bot.message_handler(commands=["yandere"])
def yandere(message):
	try:
		mess=ParseMessage(message.text)
		if not mess: raise Except("Неполное тело запроса")
		booru=pybooru.Moebooru("yandere", hash_string=yan_api)
		posts=booru.post_list(tags="_".join(mess.req()), limit=mess.fnum())
		if not posts: raise Except("Пост(ы) не найден(ы).")
		for post in posts:
			bot.send_photo(message.chat.id, urlopen(post["sample_url"]))
			name_file=post["file_url"].split("/")[-1].replace("%20", "_")
			with open(name_file,"wb") as pic:
				pic.write(requests.get(post["file_url"]).content)
			with open(name_file,"rb") as pic:
				bot.send_document(message.chat.id, pic)
	except Exception as e:
		bot.send_message(message.chat.id, e)

################################### DB ########################################
#On next episode...

###############################################################################
@bot.message_handler(commands=["timetable"])
def timetable(message):
	try:
		api_link="https://api.rozklad.org.ua/v2/"
		day=datetime.now(timezone(timedelta(hours=3))).isoweekday()
		if day>6: day=1
		week=requests.get(api_link+"weeks").json()["data"]
		pm=ParseMessage(message.text)
		tt=requests.get(api_link+f"groups/{pm.freq()}/lessons").json()
		key={"d":[[day],[week]], "t":[[day+1],[week]], "w":[range(1,7),[week]], "f":[range(1,7),[1,2]]}
		for k in pm.key():
			dn,lw="day_number","lesson_week"
			ntt=[i for i in tt["data"] if int(i[dn]) in key[k][0] and int(i[lw]) in key[k][1]]
			if not ntt:
				bot.send_message(message.chat.id, "Похоже, день свободен")
			for i in ntt:
				mes =i["day_name"]+" "+i["lesson_number"]+" "
				mes+=f"{i['time_start'][:5]}-{i['time_end'][:5]}\n"
				mes+=i["lesson_name"]+"\n"+i["teacher_name"]+" "
				mes+=i["lesson_type"]+" "+i["lesson_room"]
				if i["teachers"]: mes+=" R:"+i["teachers"][0]["teacher_rating"]
				bot.send_message(message.chat.id, mes)
	except Exception as e:
		bot.send_message(message.chat.id, e)

@bot.message_handler(commands=["trans"])
def trans(message):
	try:
		pm=ParseMessage(message.text)
		text=" ".join(pm.req())
		lang="-".join(pm.key("ru"))
		print(text,lang,pm,sep="\n")
		api_link="https://translate.yandex.net/api/v1.5/tr.json/translate"
		req=requests.get(api_link,params=dict(lang=lang,text=text,key=translate)).json()
		print(req)
		bot.send_message(message.chat.id, req["text"] ) 
	except Exception as e:
		bot.send_message(message.chat.id, e)

################################## Webhooks ###################################
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
