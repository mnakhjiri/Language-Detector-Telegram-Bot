# imports
import random
import time
import pickle
import threading
from telebot import types
import lang

# bot initial configuration
from config import *


# bot menu
def menu(message):
    if message.chat.type == "private":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itembtn5 = types.KeyboardButton('راهنما')
        itembtn6 = types.KeyboardButton('زبان های پشتیبانی شده')
        markup.row(itembtn5, itembtn6)
        bot.send_message(message.chat.id, "دستور خود را وارد کنید", reply_markup=markup)


def lang_menu(message):
    if message.chat.type == "private":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        itembtn5 = types.KeyboardButton('زبان درست پیش بینی شد')
        itembtn6 = types.KeyboardButton('زبان اشتباه پیش بینی شد')
        markup.row(itembtn5, itembtn6)
        bot.send_message(message.chat.id, "دستور خود را وارد کنید", reply_markup=markup)


# Handling functions

def handle_caption_exception(message):
    caption = "None"
    try:
        caption = message.caption
    except:
        pass
    logging.warning(f" prev caption : {caption}")


def user_show_help(message):
    help_text = "راهنما" + """
متن خود را به ربات ارسال نمایید و در صورت تشخیص اشتباه زبان , زبان درست را به ربات ارسال نمایید"""
    bot.send_message(message.chat.id, help_text)


# handling start of the bot in private mode
@bot.message_handler(commands=['start'])
def greet(message):
    greet_text = "\nبه ربات پیش بینی زبان خوش آمدید خوش اومدی"
    if message.chat.type == "private":
        bot.send_message(message.chat.id, "سلام " + message.chat.first_name + greet_text)
        menu(message)


# handling menu
@bot.message_handler(regexp="راهنما")
def handle_message(message):
    if message.chat.type == "private":
        user_show_help(message)
        menu(message)

@bot.message_handler(regexp='زبان های پشتیبانی شده')
def handle_message(message):
    if message.chat.type == "private":
        langs = lang.get_all_langs()
        response = "زبان های پشتیبانی شده : \n"
        for lang_title in langs:
            response += lang_title + "\n"
        bot.send_message(message.chat.id, response)
        menu(message)


@bot.message_handler(regexp="زبان درست پیش بینی شد")
def handle_message(message):
    if message.chat.type == "private":
        menu(message)


@bot.message_handler(regexp='زبان اشتباه پیش بینی شد')
def handle_message(message):
    if message.chat.type == "private":
        bot.send_message(message.chat.id, "لطفا زبان درست را وارد نمایید")
        menu(message)
        reply_mode[message.chat.id] = "get_lang"


# handling replies
@bot.message_handler()
def message_handler(message):
    if message.chat.type == "private" and message.text == "برگشت":
        menu(message)
        return

    if message.chat.type == "private" and message.chat.id in reply_mode.keys():
        if reply_mode[message.chat.id] == "get_lang":
            lang.add_lang(reply_mode[str(message.chat.id) + "langtext"], message.text)
            bot.send_message( message.chat.id , "زبان با موفقیت ثبت شد")
            menu(message)
            reply_mode.pop(message.chat.id)
            return

    if message.chat.type == "private":
        lang_title = lang.lang_predict(message.text)
        reply_mode[str(message.chat.id) + "langtext"] = message.text
        response_text = "آیا این زبان مورد نظر شما است؟\n" + lang_title
        bot.send_message(message.chat.id, response_text)
        lang_menu(message)
        return


bot.infinity_polling()
