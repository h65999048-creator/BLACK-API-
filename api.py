from flask import Flask, request, jsonify
import requests
import random
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# 30+ Proxies (Block bypass karne ke liye)
PROXY_LIST = [
    "http://103.152.112.162:80", "http://47.88.3.19:80", "http://198.199.86.11:8080",
    "http://159.203.61.169:8080", "http://138.68.60.8:8080", "http://68.183.159.197:8080",
    "http://104.248.63.200:8080", "http://165.227.105.150:8080", "http://206.189.157.101:8080",
    "http://159.89.174.2:8080", "http://167.172.109.12:8080", "http://165.22.10.126:8080",
    "http://188.166.83.13:8080", "http://159.65.221.25:8080", "http://206.189.156.210:8080",
    "http://143.198.118.204:8080", "http://134.209.29.120:8080", "http://178.128.20.210:8080",
    "http://159.89.189.10:8080", "http://167.99.236.2:8080", "http://161.35.10.20:8080",
    "http://104.248.100.20:8080", "http://206.81.20.30:8080", "http://165.232.10.20:8080",
    "http://143.110.20.30:8080", "http://157.245.10.20:8080", "http://188.166.20.30:8080",
    "http://134.209.10.20:8080", "http://159.89.10.20:8080", "http://167.99.10.20:8080"
]

@app.route('/')
def home():
    return "Relay Server is Running!"

@app.route('/send_otp')
def send_otp():
    email = request.args.get('email')
    if not email:
        return jsonify({"error": "Email required"}), 400

    url = "https://100067.connect.garena.com/game/account_security/swap:send_otp"
    headers = {
        "User-Agent": "GarenaMSDK/4.0.41(TECNO KJ5 ;Android 13;en;HK;app 1.123.1 2019120270;)",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }
    data = {"app_id": "100067", "email": email, "locale": "hi_IN"}

    # 15 alag proxies try karega
    for _ in range(15):
        proxy = random.choice(PROXY_LIST)
        proxies = {'http': proxy, 'https': proxy}
        try:
            resp = requests.post(url, headers=headers, data=data, timeout=15, proxies=proxies, verify=False)
            if resp.status_code == 403:
                continue
            if resp.status_code == 200:
                return jsonify(resp.json())
        except Exception:
            continue

    return jsonify({"error": "all_proxies_failed"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)