import time
from telegram import Bot
from scraper import fetch_account, fetch_list
from database import is_new
from config import *

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def load_file(path):
    with open(path) as f:
        return [x.strip() for x in f if x.strip()]

def keyword_ok(text, keywords):
    if not keywords:
        return True
    t = text.lower()
    return any(k in t for k in keywords)

def send(msg):
    bot.send_message(
        chat_id=TELEGRAM_GROUP_ID,
        text=msg,
        disable_web_page_preview=False
    )

print("🚀 X ACCOUNT + LIST TRACKER RUNNING")

while True:
    accounts = load_file("accounts.txt")
    lists = load_file("lists.txt")
    keywords = load_file("keywords.txt") if USE_KEYWORD_FILTER else []

    # AKUN X
    for acc in accounts:
        try:
            tid, text, link = fetch_account(acc)
            if keyword_ok(text, keywords) and is_new(acc, tid):
                send(f"🐦 AKUN @{acc}\n\n{text}\n\n{link}")
        except Exception as e:
            print(f"[ACC ERROR] {acc}: {e}")

    # LIST X
    for lid in lists:
        try:
            tid, text, link = fetch_list(lid)
            if keyword_ok(text, keywords) and is_new(lid, tid):
                send(f"📋 LIST {lid}\n\n{text}\n\n{link}")
        except Exception as e:
            print(f"[LIST ERROR] {lid}: {e}")

    time.sleep(CHECK_INTERVAL)
