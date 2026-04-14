from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for
import requests
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "WIZZY_SOVEREIGN_MULTI_PAGE_2026"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config.update(SESSION_COOKIE_SECURE=True, SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')

# إعدادات المحرك (The Code Breaker Settings)
API_URL = "https://tikwm.com/api/"
SEARCH_URL = "https://tikwm.com/api/feed/search"
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "current_language=en",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
}

# --- المسارات (Routes) ---

# 1. البوابة (التفتيش)
@app.route('/')
def gate():
    if session.get('is_verified'): return redirect(url_for('downloader_page'))
    return render_template('verify.html')

@app.route('/api/verify_success', methods=['POST'])
def verify_success():
    session.permanent = True
    session['is_verified'] = True
    return jsonify({"success": True})

# 2. صفحة التحميل
@app.route('/downloader')
def downloader_page():
    if not session.get('is_verified'): return redirect(url_for('gate'))
    return render_template('index.html')

# 3. صفحة البحث
@app.route('/search')
def search_page():
    if not session.get('is_verified'): return redirect(url_for('gate'))
    return render_template('search.html')

# --- محركات البيانات (APIs) ---

@app.route('/api/download', methods=['POST'])
def api_download():
    video_url = request.json.get('url', '').strip()
    try:
        res = requests.post(API_URL, data={"url": video_url, "hd": "1"}, headers=HEADERS).json()
        return jsonify({"success": True, "data": res['data']}) if res.get('code') == 0 else jsonify({"success": False})
    except: return jsonify({"success": False})

@app.route('/api/search', methods=['POST'])
def api_search():
    query = request.json.get('query', '').strip()
    try:
        res = requests.post(SEARCH_URL, data={"keywords": query, "count": 15}, headers=HEADERS).json()
        return jsonify({"success": True, "videos": res['data']['videos']}) if res.get('code') == 0 else jsonify({"success": False})
    except: return jsonify({"success": False})

@app.route('/proxy_download')
def proxy_download():
    target_url = request.args.get('url')
    req = requests.get(target_url, headers=HEADERS, stream=True)
    return Response(req.iter_content(chunk_size=1024*32), content_type=req.headers.get('Content-Type'))

if __name__ == "__main__":
    app.run()
