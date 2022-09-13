import logging
import configparser
import telebot

# class Config:
config = configparser.ConfigParser()
config.read('config.ini')
logging.basicConfig(format= '%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S' , filename='bot.log', level=logging.DEBUG)
bot = telebot.TeleBot(config['bot']['API_KEY'])
signs = {}
groups = []
reply_mode = {}
sign_mode = {}
audio_pv_forward = {}
audio_database = {}
