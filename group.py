import telebot
from telebot import types, util
from googletrans import Translator
import json
#! from decouple import config

BOT_TOKEN = "5809856651:AAEo2U9nMB_g8xkvsPUDsMPZ-aEOqjelUVI"
bot = telebot.TeleBot(BOT_TOKEN)
translator = Translator()

#? words to want reply
data_bot = {
    "name": ["moon", "قمر", "قموري", "القمر"]
}
greeting = ["hello", "hi", "hey", "هلا", "أهلا", "كيفك", "كيف حالك"]
said_bot = ["bot", "بوت", "البوت"]
key_translate = ["translate", "trans", "translator", "ترجم", "ترجملي"]
offensive_word = ["cat", "dog"]

#? all sinding text in my BOT 
text_message = {
    "start": "أهلا بك في بوت المجموعات الأول في منصة التيليجرام",
    "help": "كيف يمكنني مساعدتك \nمعرف مبرمج البوت @S_87_A",
    "hello": "هلا",
    "bot":  "أنا مش بوت احترم نفسك أو بيقع كلام ثاني 😾👊🏾",
    "call": "أنا موجود هنا ماذا تريد مني😒",
    "new": u"مرحباً بك عزيزي {name}🗿🐸\nفي مجموعتنا التي  فيها كل شيء بايخ زيك💩",
    "left": u"{name}غادر المجموعة🥺💔",
    "warn": 
        u"لقد ارسل {name} أحد الكلمات المحظورة 🚫❌"
        u"عدد التحذيرات لديك {safe_counter}/5 سيتم طردك إذا انتهت المحاولات ",
    "leave_group": "عفوا لقد تمت إضافي إلى غير المجموعة التي برمجة لها\n لقد غادرت😴👻"
}

#!TODO make function saving users data
def handleOffensiveMessage(message):
    id = str(message.from_user.id)
    name = message.from_user.full_name
    print(message.from_user)
    user_name = message.from_user.username
    is_bot = message.from_user.is_bot
    

    with open("data.json", "r") as file_json:
        data = json.load(file_json)
    file_json.close()

    users = data["users"]
    if id not in users:
        users[id] = {"user_name":user_name}
        users[id]["name"] = name
        users[id]["is_bot"] = is_bot
        users[id]["safe_counter"] = 5

    if id in users:
        users[id]["safe_counter"] -= 1
        if users[id]["safe_counter"] == 0:
            users.pop(id)
    
    safe_counter = users[id]["safe_counter"]
    bot.send_message(message.chat.id, text_message["warn"].format(name=message.from_user.first_name,safe_counter=safe_counter))
    bot.delete_message(message.chat.id, message.message_id)

    # num_of_users = len(users)
    # print(list(users[id].values())[2])
    with open("data.json", "w") as editedFile:
        json.dump(data, editedFile, indent=3)
    editedFile.close()



#* answer command messages
#? start
@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_message(message.chat.id,text_message["start"])

#? help
@bot.message_handler(commands=["help"])
def welcome(message):
    bot.send_message(message.chat.id,text_message["help"])

#* greet member in bot chat
#* reply member say bot
#* reply member call me
@bot.message_handler(func=lambda m:True)
def reply(message):
    words = message.text.split()
    if words[0].lower() in greeting:
        bot.reply_to(message, text_message["hello"])
    elif words[0].lower() in said_bot:
        bot.reply_to(message, text_message["bot"])
    elif words[0].lower() in data_bot["name"]:
        bot.reply_to(message, text_message["call"])

    #* adding googletrans api
    #* translating word and sentence to arabic
    elif words[0].lower() in key_translate:
        translation = translator.translate(" ".join(words[1:]), dest="ar", src="en")
        bot.send_message(message.chat.id, translation.text)

    #* delete offensive message
    elif words[0].lower() in offensive_word:
        handleOffensiveMessage(message)
        
    
    else:
        bot.reply_to(message, "I do not know what I say")

#* welcom to new members in chat
@bot.chat_member_handler()
def join_member(message:types.ChatMemberUpdated):
    NewMember = message.new_chat_member
    if NewMember.status == "member":
        bot.send_message(message.chat.id, text_message["new"].format(name=NewMember.user.full_name))
    elif NewMember.status == "left":
        bot.send_message(message.chat.id, text_message["left"].format(name=NewMember.user.full_name))

#* leave anychat thats not mine
@bot.my_chat_member_handler()
def leave(message:types.ChatMemberUpdated):
    bot.send_message(message.chat.id, text_message["leave_group"])
    bot.leave_chat(message.chat.id)


bot.infinity_polling(allowed_updates=util.update_types)