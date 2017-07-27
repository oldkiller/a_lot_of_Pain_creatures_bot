import requests
import telebot
import os
from flask import Flask, request

bot = telebot.TeleBot('426351504:AAHomR1jc-m2B7iabRnOFR8OkPTKlkWMIdw')
weath_token = "795819f679706a61cd7938b26ac247af"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

###############################################################################
def weath_req(types, message):
    city=message.text.split(" ")
    if city[-1]!="/"+types and len(city[-1])!=0:
        res=requests.get(f"http://api.openweathermap.org/data/2.5/{types}", 
                    params={"q":city[1],'units':'metric', 'lang':'ru', "APPID":weath_token})
    else:    
        bot.send_message(message.chat.id, "Укажите город, для которого выполняется поиск.")
    data = res.json()
    return data

def weath_mess_form(data, mess=""):
    mess+="Погода: "+data['weather'][0]['description']+"\n"
    mess+="Температура: "+"%f"%round(data['main']['temp'],2)+"\n"
    mess+="Влажность: "+"%f"%round(data["main"]["humidity"],2)+"\n"
    mess+="Скорость ветра: "+"%f"%round(data["wind"]["speed"],2)
    return mess

@bot.message_handler(commands=['weather'])
def weather(message):
    try:
        # city=message.text.split(" ")
        # if city[-1]!="/weather" and len(city[-1])!=0:
        #     res=requests.get("http://api.openweathermap.org/data/2.5/weather", 
        #         params={"q":city[1],'units':'metric', 'lang':'ru', "APPID":weath_token})
        # else:    
        #     bot.send_message(message.chat.id, "Укажите город, для которого выполняется поиск.")
        # data=res.json()
        data = weath_req("weather", message)
        # mess="Погода: "+data['weather'][0]['description']+"\n"
        # mess+="Температура: "+"%f"%round(data['main']['temp'],2)+"\n"
        # mess+="Влажность: "+"%f"%round(data["main"]["humidity"],2)+"\n"
        # mess+="Скорость ветра: "+"%f"%round(data["wind"]["speed"],2)
        mess = weath_mess_form(data)
        bot.send_message(message.chat.id,mess)
    except Exception as e:
        print('Exception', e)
        pass


@bot.message_handler(commands=['forecast'])
def forecast(message):
    try:
        # res=requests.get("http://api.openweathermap.org/data/2.5/forecast",
        #     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': weath_token})
        # data=res.json()
        # for i in data['list']:
        #     co=i['dt_txt']+'{0:+3.0f}'.format(i['main']['temp'])+i['weather'][0]['description']
        #     bot.send_message(message.chat.id,co)
        data = weath_req("forecast", message)
        for i in data["list"]:
            if i["dt_txt"][11:13]=="12" or i["dt_txt"][11:13]=="00":
                mess=i["dt_txt"]+"\n"
                mess=weath_mess_form(i, mess)
                bot.send_message(message.chat.id, mess)
    except Exception as e:
        print('Exception', e)
        pass





###############################################################################
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
