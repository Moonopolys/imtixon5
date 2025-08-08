from telebot import TeleBot

from config import TOKEN
from database.dbase import Database

bot = TeleBot(TOKEN, parse_mode="html")
db = Database()