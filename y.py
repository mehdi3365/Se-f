#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 CodeCraft Telegram Bot — نسخه رایگان با تایید شماره + زیرمجموعه‌گیری + جوین اجباری

قابلیت‌ها:
  ✔ ورود رایگان با اشتراک و تایید شماره تلفن (اجباری)
  ✔ هر کاربر ۵ سؤال رایگان دارد
  ✔ با هر زیرمجموعه (دعوت با لینک اختصاصی) → ۱ سؤال بیشتر
  ✔ جوین اجباری کانال تلگرام قبل از استفاده
  ✔ پاسخ AI + ارسال کدها به صورت فایل (Document)
  ✔ پنل ادمین: بن/حذف بن، آمار، پیام همگانی

نصب:  pip install aiogram aiohttp
اجرا: python telegram_bot.py
"""

import os, re, io, json, sqlite3, datetime, asyncio, logging
import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ════════════════════════════ تنظیمات ════════════════════════════
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
DB_PATH = os.path.join(BASE_DIR, "bot.db")

DEFAULT_CONFIG = {
    "bot_token": "8758465726:AAHX77P9ZllsdQRKUE6LNUrQLegoWUMdbzI",          # ← توکن ربات را اینجا بگذارید
    "admin_ids": [8536789126],                        # ← آیدی عددی ادمین‌ها
    "channel_id": "@chgpt_Max",                   # ← کانال جوین اجباری (مثل @mychannel)
    "channel_url": "https://t.me/chgpt_Max",      # ← لینک کانال
    "force_join": True,
    "free_questions": 5,                             # سؤال‌های رایگان اولیه
    "ref_bonus": 1,                                  # سؤال اضافه به ازای هر زیرمجموعه
    "api_key": "cc_9kmD1RllwIGALtwI9hx4sDERykFJZ5cmpBZs389b1GKa1UDn",                        # ← کلید CodeCraft API
    "base_url": "https://codecraftapi.com/v1",
    "model": "gpt-5.6-luna",
    "temperature": 1,
    "max_tokens": 8192,
    "system_prompt": "You are a helpful coding assistant. Always wrap code in ```language blocks.",
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, encoding="utf-8") as f:
            cfg = json.load(f)
        for k, v in DEFAULT_CONFIG.items():
            cfg.setdefault(k, v)
        return cfg
    save_config(DEFAULT_CONFIG)
    return dict(DEFAULT_CONFIG)

def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

CFG = load_config()

# ════════════════════════════ دیتابیس ════════════════════════════
class DB:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username TEXT, full_name TEXT,
            phone TEXT DEFAULT '',
            phone_verified INTEGER DEFAULT 0,
            ref_by INTEGER DEFAULT 0,
            ref_count INTEGER DEFAULT 0,
            questions_left INTEGER DEFAULT 5,
            total_asked INTEGER DEFAULT 0,
            banned INTEGER DEFAULT 0,
            joined_at TEXT
        );
        CREATE TABLE IF NOT EXISTS questions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, question TEXT, answer TEXT, created_at TEXT
        );""")
        self.conn.commit()

    def add_user(self, uid, username, full_name):
        self.conn.execute(
            "INSERT OR IGNORE INTO users(user_id,username,full_name,joined_at) VALUES(?,?,?,?)",
            (uid, username or "", full_name or "", datetime.datetime.now().isoformat()))
        self.conn.commit()

    def get(self, uid):
        return self.conn.execute("SELECT * FROM users WHERE user_id=?", (uid,)).fetchone()

    def set_phone(self, uid, phone):
        self.conn.execute("UPDATE users SET phone=?, phone_verified=1 WHERE user_id=?",
                          (phone, uid))
        self.conn.commit()

    def set_ref(self, uid, ref_by, bonus):
        u = self.get(uid)
        if u and not u["ref_by"] and ref_by != uid:
            self.conn.execute("UPDATE users SET ref_by=? WHERE user_id=?", (ref_by, uid))
            self.conn.execute("UPDATE users SET ref_count=ref_count+1, questions_left=questions_left+? WHERE user_id=?",
                              (bonus, ref_by))
            self.conn.commit()
            return True
        return False

    def use_question(self, uid):
        self.conn.execute(
            "UPDATE users SET questions_left=questions_left-1, total_asked=total_asked+1 WHERE user_id=?",
            (uid,))
        self.conn.commit()

    def add_questions(self, uid, n):
        self.conn.execute("UPDATE users SET questions_left=questions_left+? WHERE user_id=?", (n, uid))
        self.conn.commit()

    def ban(self, uid, b=1):
        self.conn.execute("UPDATE users SET banned=? WHERE user_id=?", (b, uid))
        self.conn.commit()

    def save_q(self, uid, q, a):
        self.conn.execute(
            "INSERT INTO questions(user_id,question,answer,created_at) VALUES(?,?,?,?)",
            (uid, q, a[:2000], datetime.datetime.now().isoformat()))
        self.conn.commit()

    def stats(self):
        c = self.conn
        return {
            "users": c.execute("SELECT COUNT(*) x FROM users").fetchone()["x"],
            "verified": c.execute("SELECT COUNT(*) x FROM users WHERE phone_verified=1").fetchone()["x"],
            "banned": c.execute("SELECT COUNT(*) x FROM users WHERE banned=1").fetchone()["x"],
            "questions": c.execute("SELECT COUNT(*) x FROM questions").fetchone()["x"],
            "refs": c.execute("SELECT COALESCE(SUM(ref_count),0) x FROM users").fetchone()["x"],
        }

    def all_users(self):
        return self.conn.execute("SELECT user_id FROM users WHERE banned=0").fetchall()

    def top_refs(self, n=10):
        return self.conn.execute(
            "SELECT full_name, ref_count FROM users ORDER BY ref_count DESC LIMIT ?", (n,)).fetchall()

db = DB()

# ════════════════════════════ هوش مصنوعی ════════════════════════════
async def ask_ai(prompt: str) -> str:
    url = f"{CFG['base_url'].rstrip('/')}/chat/completions"
    headers = {"Authorization": f"Bearer {CFG['api_key']}", "Content-Type": "application/json"}
    payload = {"model": CFG["model"], "temperature": CFG["temperature"],
               "max_tokens": CFG["max_tokens"],
               "messages": [{"role": "system", "content": CFG["system_prompt"]},
                            {"role": "user", "content": prompt}]}
    async with aiohttp.ClientSession() as s:
        async with s.post(url, headers=headers, json=payload, timeout=aiohttp.ClientTimeout(total=120)) as r:
            data = await r.json()
            return data["choices"][0]["message"]["content"]

CODE_RE = re.compile(r"```(\w*)\n(.*?)```", re.DOTALL)

def extract_codes(text: str):
    out = []
    for m in CODE_RE.finditer(text):
        out.append((m.group(1) or "txt", m.group(2).strip()))
    return out

# ═══════════════════════════=== کیبوردها ════════════════════════════
def phone_kb():
    return ReplyKeyboardMarkup(keyboard=[[
        KeyboardButton(text="📱 اشتراک شماره تلفن", request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True)

def main_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton("❓ سؤال از هوش مصنوعی"), KeyboardButton("📊 حساب من")],
        [KeyboardButton("🔗 لینک دعوت"), KeyboardButton("📞 پشتیبانی")]],
        resize_keyboard=True)

def admin_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 آمار ربات", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📢 پیام همگانی", callback_data="admin_broadcast")],
        [InlineKeyboardButton(text="⛔ بن کاربر", callback_data="admin_ban"),
         InlineKeyboardButton(text="✅ حذف بن", callback_data="admin_unban")],
        [InlineKeyboardButton(text="➕ اضافه کردن سؤال", callback_data="admin_addq")],
        [InlineKeyboardButton(text="🏆 برترین دعوت‌کنندگان", callback_data="admin_refs")],
    ])

def join_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 عضویت در کانال", url=CFG["channel_url"])],
        [InlineKeyboardButton(text="✅ بررسی عضویت", callback_data="check_join")]])

# ═══════════════════════════=== FSM ادمین ════════════════════════════
class Admin(StatesGroup):
    broadcast = State()
    ban = State()
    unban = State()
    addq = State()

# ═══════════════════════════=== راه‌اندازی ════════════════════════════
bot = Bot(token=CFG["bot_token"])
dp = Dispatcher(storage=MemoryStorage())

def is_admin(uid): return uid in CFG["admin_ids"]

async def joined_channel(uid: int) -> bool:
    if not CFG["force_join"]:
        return True
    try:
        m = await bot.get_chat_member(chat_id=CFG["channel_id"], user_id=uid)
        return m.status in ("member", "administrator", "creator")
    except Exception:
        return False

async def check_user_ok(message: types.Message) -> bool:
    """بررسی بن + جوین + تایید شماره"""
    u = db.get(message.from_user.id)
    if not u:
        db.add_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
        u = db.get(message.from_user.id)
    if u["banned"]:
        await message.answer("⛔ شما از ربات بن شده‌اید.")
        return False
    if not await joined_channel(message.from_user.id):
        await message.answer(
            f"⚠️ برای استفاده از ربات ابتدا در کانال ما عضو شوید:\n{CFG['channel_url']}",
            reply_markup=join_kb())
        return False
    if not u["phone_verified"]:
        await message.answer(
            "📱 لطفاً برای استفاده رایگان از ربات، شماره تلفن خود را با دکمه زیر به اشتراک بگذارید:",
            reply_markup=phone_kb())
        return False
    return True

# ═══════════════════════════=== /start ════════════════════════════
@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    uid = message.from_user.id
    db.add_user(uid, message.from_user.username, message.from_user.full_name)

    # بررسی زیرمجموعه‌گیری
    args = message.text.split(maxsplit=1)
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            ref_id = int(args[1][4:])
            if db.set_ref(uid, ref_id, CFG["ref_bonus"]):
                await bot.send_message(ref_id,
                    f"🎉 یک نفر با لینک شما وارد شد! +{CFG['ref_bonus']} سؤال دریافت کردید.")
        except ValueError:
            pass

    if is_admin(uid):
        await message.answer("👑 پنل مدیریت:", reply_markup=admin_kb())
    if not await joined_channel(uid):
        await message.answer(
            f"👋 خوش آمدید!\nابتدا در کانال عضو شوید:\n{CFG['channel_url']}",
            reply_markup=join_kb())
        return
    u = db.get(uid)
    if not u["phone_verified"]:
        await message.answer(
            "📱 شماره تلفن خود را برای تایید به اشتراک بگذارید:",
            reply_markup=phone_kb())
        return
    await message.answer(
        f"🤖 خوش آمدید!\nشما {u['questions_left']} سؤال رایگان دارید.\n"
        "هر سوالی که بپرسید هوش مصنوعی پاسخ می‌دهد و کدها به صورت فایل ارسال می‌شوند.",
        reply_markup=main_kb())

# ═══════════════════════════=== تایید شماره ════════════════════════════
@dp.message(F.contact)
async def contact_handler(message: types.Message):
    uid = message.from_user.id
    if message.contact.user_id != uid:
        await message.answer("⚠️ لطفاً از دکمه خود ربات شماره را ارسال کنید.", reply_markup=phone_kb())
        return
    db.set_phone(uid, message.contact.phone_number)
    await message.answer(
        "✅ شماره شما تایید شد!\nاز بخش «سؤال از هوش مصنوعی» استفاده کنید. کدهای پاسخ به صورت فایل ارسال می‌شوند.",
        reply_markup=main_kb())

@dp.callback_query(F.data == "check_join")
async def check_join(cb: types.CallbackQuery):
    if await joined_channel(cb.from_user.id):
        u = db.get(cb.from_user.id)
        if not u["phone_verified"]:
            await cb.message.answer("📱 حالا شماره تلفن خود را تایید کنید:", reply_markup=phone_kb())
        else:
            await cb.message.answer("✅ عضویت تایید شد!", reply_markup=main_kb())
    else:
        await cb.answer("❌ هنوز عضو کانال نیستید!", show_alert=True)

# ═══════════════════════════=== دستورهای کاربر ════════════════════════════
@dp.message(F.text == "📊 حساب من")
async def my_account(message: types.Message):
    u = db.get(message.from_user.id)
    await message.answer(
        f"📊 حساب شما:\n\n"
        f"🆔 آیدی: <code>{u['user_id']}</code>\n"
        f"📱 شماره: {u['phone'] or 'تایید نشده'}\n"
        f"❓ سؤال‌های باقی‌مانده: <b>{u['questions_left']}</b>\n"
        f"📈 کل سؤالات پرسیده: {u['total_asked']}\n"
        f"🔗 تعداد زیرمجموعه: {u['ref_count']}")

@dp.message(F.text == "🔗 لینک دعوت")
async def referral(message: types.Message):
    me = await bot.get_me()
    link = f"https://t.me/{me.username}?start=ref_{message.from_user.id}"
    await message.answer(
        f"🔗 لینک دعوت اختصاصی شما:\n<code>{link}</code>\n\n"
        f"با هر نفری که با این لینک وارد شود، <b>+{CFG['ref_bonus']} سؤال</b> هدیه می‌گیرید! 🎁")

@dp.message(F.text == "📞 پشتیبانی")
async def support(message: types.Message):
    await message.answer(f"📞 برای پشتیبانی به ادمین پیام دهید: {CFG['channel_url']}")

@dp.message(F.text == "❓ سؤال از هوش مصنوعی")
async def ask_hint(message: types.Message, state: FSMContext):
    if not await check_user_ok(message):
        return
    await message.answer("✍️ سؤال خود را بنویسید (هر متنی ارسال کنید تا به AI برسد):")

# ═══════════════════════════=== پرسش سؤال ════════════════════════════
@dp.message(F.text)
async def handle_question(message: types.Message, state: FSMContext):
    # حالت‌های ادمین
    cur = await state.get_state()
    if cur == Admin.broadcast.state:
        await do_broadcast(message, state); return
    if cur == Admin.ban.state:
        await do_ban(message, state); return
    if cur == Admin.unban.state:
        await do_unban(message, state); return
    if cur == Admin.addq.state:
        await do_addq(message, state); return

    uid = message.from_user.id
    if is_admin(uid) and message.text.startswith("/"):
        return

    if not await check_user_ok(message):
        return

    u = db.get(uid)
    if u["questions_left"] <= 0:
        await message.answer(
            f"❌ سؤال‌های رایگان شما تمام شد!\n"
            f"با دعوت دوستان با لینک اختصاصی، به ازای هر نفر +{CFG['ref_bonus']} سؤال بگیرید. 🎁\n"
            f"از دکمه «🔗 لینک دعوت» استفاده کنید.")
        return

    wait = await message.answer("⏳ در حال پردازش سؤال شما...")
    try:
        answer = await ask_ai(message.text)
    except Exception as e:
        await wait.edit_text(f"❌ خطا: {e}")
        return

    db.use_question(uid)
    db.save_q(uid, message.text, answer)
    u = db.get(uid)

    # ارسال پاسخ (اگر طولانی بود تقسیم شود)
    for i in range(0, len(answer), 4000):
        await message.answer(answer[i:i+4000])

    # ارسال کدها به صورت فایل
    codes = extract_codes(answer)
    for lang, code_body in codes:
        fname = f"code_{lang or 'txt'}_{datetime.datetime.now():%H%M%S}.{lang or 'txt'}"
        await message.answer_document(
            document=types.BufferedInputFile(code_body.encode(), filename=fname),
            caption=f"📎 فایل کد ({lang or 'txt'})")
    try:
        await wait.delete()
    except Exception:
        pass
    await message.answer(f"✅ پاسخ ارسال شد. سؤال‌های باقی‌مانده: <b>{u['questions_left']}</b>")

# ═══════════════════════════=== پنل ادمین ════════════════════════════
@dp.message(Command("admin"))
async def admin_cmd(message: types.Message):
    if is_admin(message.from_user.id):
        await message.answer("👑 پنل مدیریت:", reply_markup=admin_kb())

@dp.callback_query(F.data == "admin_stats")
async def admin_stats(cb: types.CallbackQuery):
    s = db.stats()
    await cb.message.answer(
        f"📊 آمار ربات:\n\n"
        f"👥 کل کاربران: {s['users']}\n"
        f"✅ کاربران تاییدشده: {s['verified']}\n"
        f"⛔ کاربران بن‌شده: {s['banned']}\n"
        f"❓ کل سؤالات: {s['questions']}\n"
        f"🔗 کل دعوت‌ها: {s['refs']}")

@dp.callback_query(F.data == "admin_refs")
async def admin_refs(cb: types.CallbackQuery):
    rows = db.top_refs()
    txt = "🏆 برترین دعوت‌کنندگان:\n\n" + "\n".join(
        f"{i+1}. {r['full_name']} — {r['ref_count']} نفر" for i, r in enumerate(rows) if r['ref_count'] > 0)
    await cb.message.answer(txt or "هنوز دعوتی انجام نشده است.")

@dp.callback_query(F.data == "admin_broadcast")
async def admin_broadcast(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.answer("📢 پیام همگانی خود را ارسال کنید (متن/عکس/فایل):")
    await state.set_state(Admin.broadcast)

async def do_broadcast(message: types.Message, state: FSMContext):
    await state.clear()
    users = db.all_users()
    ok, fail = 0, 0
    status = await message.answer(f"⏳ در حال ارسال به {len(users)} کاربر...")
    for u in users:
        try:
            await message.copy_to(u["user_id"])
            ok += 1
        except Exception:
            fail += 1
        await asyncio.sleep(0.05)
    await status.edit_text(f"✅ ارسال شد!\nموفق: {ok} | ناموفق: {fail}")

@dp.callback_query(F.data == "admin_ban")
async def admin_ban(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.answer("⛔ آیدی عددی کاربر را برای بن ارسال کنید:")
    await state.set_state(Admin.ban)

async def do_ban(message: types.Message, state: FSMContext):
    await state.clear()
    try:
        uid = int(message.text.strip())
        db.ban(uid, 1)
        await message.answer(f"⛔ کاربر {uid} بن شد.")
    except ValueError:
        await message.answer("⚠️ آیدی نامعتبر است.")

@dp.callback_query(F.data == "admin_unban")
async def admin_unban(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.answer("✅ آیدی عددی کاربر را برای حذف بن ارسال کنید:")
    await state.set_state(Admin.unban)

async def do_unban(message: types.Message, state: FSMContext):
    await state.clear()
    try:
        uid = int(message.text.strip())
        db.ban(uid, 0)
        await message.answer(f"✅ بن کاربر {uid} برداشته شد.")
    except ValueError:
        await message.answer("⚠️ آیدی نامعتبر است.")

@dp.callback_query(F.data == "admin_addq")
async def admin_addq(cb: types.CallbackQuery, state: FSMContext):
    await cb.message.answer("➕ به این صورت ارسال کنید:\n<code>آیدی_کاربر تعداد_سؤال</code>\nمثال: <code>123456 10</code>")
    await state.set_state(Admin.addq)

async def do_addq(message: types.Message, state: FSMContext):
    await state.clear()
    try:
        uid, n = message.text.split()
        db.add_questions(int(uid), int(n))
        await message.answer(f"✅ {n} سؤال به کاربر {uid} اضافه شد.")
    except ValueError:
        await message.answer("⚠️ فرمت اشتباه است.")

# ═══════════════════════════=== اجرا ════════════════════════════
async def main():
    logging.basicConfig(level=logging.INFO)
    print("🤖 ربات روشن شد...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
          
