import requests
import telebot
import os
from flask import Flask, request

bot = telebot.TeleBot('426351504:AAHomR1jc-m2B7iabRnOFR8OkPTKlkWMIdw')
weath_token = "795819f679706a61cd7938b26ac247af"
city_id=703448

# if os.environ.get('DATABASE_URL') is None: ## For DB

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(commands=['weather'])
def weather(message):
    city=message.text.split(" ")
    try:
        if city[-1]!="/weather" and len(city[-1])!=0:
            res=requests.get("http://api.openweathermap.org/data/2.5/weather", params={"q":city[1],'units':'metric', 'lang':'ru', "APPID":weath_token})
        else:    
            res=requests.get("http://api.openweathermap.org/data/2.5/weather", params={'id':city_id,'units':'metric', 'lang':'ru', 'APPID':weath_token})
        data=res.json()
        mess="Погода: "+data['weather'][0]['description']+"\n"
        mess+="Температура: "+'{0:+3.0f}'.format(data['main']['temp'])
        bot.send_message(message.chat.id,mess)
    except Exception as e:
        print('Exception', e)
        pass


@bot.message_handler(commands=['forecast'])
def forecast(message):
    try:
        res=requests.get("http://api.openweathermap.org/data/2.5/forecast",
            params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': weath_token})
        data=res.json()
        for i in data['list']:
            co=i['dt_txt']+'{0:+3.0f}'.format(i['main']['temp'])+i['weather'][0]['description']
            bot.send_message(message.chat.id,co)
    except Exception as e:
        print('Exception', e)
        pass






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
