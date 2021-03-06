import traceback
import requests
import telebot
import pybooru
import os
from datetime import datetime,timezone,timedelta
from urllib.request import urlopen
from flask import Flask, request
from ParseMessage import ParseMessage
from Postgres import Postgress

# tele_api="426351504:AAHomR1jc-m2B7iabRnOFR8OkPTKlkWMIdw"
# weath_token="795819f679706a61cd7938b26ac247af"
# yan_api="r5oUMfysc4C566kI312u_A"
# translate="trnsl.1.1.20170926T012014Z.3f5cb4c22d376499.4dc04c7f837aa68cb2ca57420651ba47d1548711"
# db_address="postgres://lciehxdy:m2xMdBB_HMr_QrvwntIeGva5ngPcSNL7@dumbo.db.elephantsql.com:5432/lciehxdy"

tele_api=os.environ['telegram_token']
weath_token=os.environ['weather_token']
bot = telebot.TeleBot(tele_api)
database=Postgress(db_address)

@bot.message_handler(commands=["start"])
def start(message):
	bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(commands=["help"])
def helps(message):
	help_mess="Все ключи начинаются с минуса (-)\n"\
	"/weather <city> - Узнать погоду в <city>\n"\
	"/forecast <key> <city> - Узнать прогноз погоды в <city>, "\
	"<key> - может принимать значения s,m,l\n"\
	"/yandere <tag> <count> - Поиск изображений на yande.re, "\
	"<tag> - теги для поиска, <count> - количество\n"\
	"/konachan <tag> <count> - Поиск изображений на konachan.com, "\
	"<tag> - теги для поиска, <count> - количество\n"\
	"/timetable <key> <group> - <group> - група, для которой берется рассписание"\
	"Ключи для рассписания: {d - day, t - tomorrow, w - week, f - full}"
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
		if not txt.req(): raise ValueError("Неполное тело запроса")
		data=weath_req("weather", txt.freq())
		bot.send_message(message.chat.id,weath_reply(data))
	except Exception as e:
		bot.send_message(message.chat.id, e)

@bot.message_handler(commands=["forecast"])
def forecast(message):
	try:
		txt=ParseMessage(message.text)
		if not txt.req(): raise ValueError("Неполное тело запроса")
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
@bot.message_handler(commands=["yandere","konachan"])
def yandere(message):
	try:
		mess=ParseMessage(message.text)
		if not mess: raise ValueError("Неполное тело запроса")
		booru=pybooru.Moebooru(mess.com())
		posts=booru.post_list(tags=" ".join(mess.req()), limit=mess.fnum(5))
		if not posts: raise ValueError("Пост(ы) не найден(ы).")
		for post in posts:
			bot.send_photo(message.chat.id, urlopen("https://"+post["sample_url"].split("//")[1]))
			if "d" in mess.key():
				name_file=post["file_url"].split("/")[-1].replace("%20", "_")
				with open(name_file,"wb") as pic:
					pic.write(requests.get("https://"+post["file_url"].split("//")[1]).content)
				with open(name_file,"rb") as pic:
					bot.send_document(message.chat.id, pic)
	except Exception as e:
		bot.send_message(message.chat.id, e)

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
		if tt["statusCode"]==404: raise ValueError(tt["message"])
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
		if "help" in pm.key():
			api_link="https://translate.yandex.net/api/v1.5/tr.json/getLangs"
			req=requests.get(api_link, params=dict(ui="ru",key=translate)).json()
			bot.send_message(message.chat.id, str(req["langs"]))
			return
		if not pm.req(): raise ValueError("Неполное тело запроса")
		text=" ".join(pm.req())
		lang="-".join(pm.key("ru"))
		api_link="https://translate.yandex.net/api/v1.5/tr.json/translate"
		req=requests.get(api_link,params=dict(lang=lang,text=text,key=translate)).json()
		if req["code"]!=200:
			bot.send_message(message.chat.id, req["message"])
			return
		bot.send_message(message.chat.id, req["text"] ) 
	except Exception as e:
		bot.send_message(message.chat.id, e)

###############################################################################
@bot.message_handler(commands=["beta"]) # testing new function 
def beta(message):
	try:
		txt=ParseMessage(message.text)
		if not txt.req():
			city=database.read(message.chat.id, "city")
			if not city:
				raise ValueError("Неполное тело запроса")
		if txt("req"):
			city=txt("req")[0]
			if "save" in txt("key"):
				database.write(message.chat.id, "city",city)
		data=weath_req("weather", city)
		bot.send_message(message.chat.id,weath_reply(data))
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
