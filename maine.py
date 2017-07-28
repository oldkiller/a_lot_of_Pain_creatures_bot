import requests
import telebot
import pybooru
import time
import os
from flask import Flask, request

bot = telebot.TeleBot('426351504:AAHomR1jc-m2B7iabRnOFR8OkPTKlkWMIdw')
tele_api
weath_token = "795819f679706a61cd7938b26ac247af"
yan_api = "r5oUMfysc4C566kI312u_A"

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
        print('Exception', e)
        pass

def weath_mess_form(data, mess=""):
    def tostr(i):
        return "{0:+3.0f}".format(i)
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
            mess=i["dt_txt"]+"\n" + weath_mess_form(i)
            bot.send_message(message.chat.id, mess)

####################### Block responsible for pictures ########################
@bot.message_handler(commands=["yandere"])
def yandere(message):
    yander=pybooru.Moebooru("yandere", hash_string=yan_api)
    p_list=yander.post_list(tags="loli", limit=5)
    for post in p_list:
        time.sleep(1)
        bot.send_message(message.chat.id, post["file_url"])

####################### Block responsible for music    ########################

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
