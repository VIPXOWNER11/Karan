import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from pymongo import MongoClient
import aiohttp
import pytz
import psutil
import asyncio
import time
import random

# === CONFIG ===
BOT_TOKEN = "7744875151:AAF8P1vSd8awHrmaGmWQiI6d-S_fgoPvLkY"
OWNER_USERNAME = "VIP_OWNER9"
JOIN_LINK = "https://t.me/+z53g9tM9shUwZTY1"

MONGO_URI = "mongodb://username:password@your-cluster.mongodb.net:27017/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['karanbot']
users = db['users']

bot = telebot.TeleBot(BOT_TOKEN)

# === START ===
@bot.message_handler(commands=["start"])
def start_msg(message):
    user = message.from_user
    if not users.find_one({"id": user.id}):
        users.insert_one({"id": user.id, "name": user.first_name})
    
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🔥 CONNECT OWNER", url=f"https://t.me/{OWNER_USERNAME}"),
        InlineKeyboardButton("📢 JOIN CHANNEL", url=JOIN_LINK)
    )
    
    bot.send_message(
        message.chat.id,
        f"👋 Welcome {user.first_name}!\n\nUse: /attack <ip> <port> <time>",
        reply_markup=markup
    )

# === ATTACK ===
@bot.message_handler(commands=["attack"])
def attack_cmd(message):
    try:
        args = message.text.split()[1:]
        ip, port, secs = args[0], int(args[1]), int(args[2])
    except:
        bot.reply_to(message, "❌ Use correct format: /attack <ip> <port> <seconds>")
        return
    
    bot.reply_to(message, f"🚀 Attacking {ip}:{port} for {secs} seconds!")

    # fake attack simulation (no real attack)
    for i in range(secs):
        time.sleep(1)
        print(f"Packet sent to {ip}:{port}")
    
    bot.send_message(message.chat.id, f"✅ Attack finished on {ip}")

# === RUN ===
print("🤖 Bot is running...")
bot.polling()
