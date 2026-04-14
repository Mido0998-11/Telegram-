from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for
import requests
import os

app = Flask(__name__)
# سكرت كي ثابت وقوي لضمان استقرار الجلسة
app.secret_key = os.urandom(24) 

# إعدادات الكوكيز لتعمل في كل الظروف
app.config.update(
    SESSION_COOKIE_NAME='wizzy_session',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=3600 # ساعة واحدة تكفي
)

API_URL = "https://tikwm.com/api/"
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "current_language=en",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

@app.route('/')
def gate():
    if session.get('is_verified'):
        return redirect(url_for('downloader_page'))
    return render_template('verify.html')

@app.route('/api/verify_success', methods=['POST'])
def verify_success():
    session['is_verified'] = True
    return jsonify({"success": True})

@app.route('/downloader')
def downloader_page():
    if not session.get('is_verified'):
        return redirect(url_for('gate'))
    return render_template('index.html')

@app.route('/search')
def search_page():
    if not session.get('is_verified'):
        return redirect(url_for('gate'))
    return render_template('search.html')

@app.route('/api/download', methods=['POST'])
def api_download():
    video_url = request.json.get('url', '').strip()
    try:
        res = requests.post(API_URL, data={"url": video_url, "hd": "1"}, headers=HEADERS).json()
        if res.get('code') == 0:
            return jsonify({"success": True, "data": res['data']})
        return jsonify({"success": False, "message": "الفيديو غير موجود"})
    except:
        return jsonify({"success": False, "message": "عطل في السيرفر العالمي"})

@app.route('/api/search', methods=['POST'])
def api_search():
    query = request.json.get('query', '').strip()
    try:
        search_api = "https://tikwm.com/api/feed/search"
        res = requests.post(search_api, data={"keywords": query, "count": 12}, headers=HEADERS).json()
        if res.get('code') == 0:
            return jsonify({"success": True, "videos": res['data']['videos']})
        return jsonify({"success": False})
    except:
        return jsonify({"success": False})

@app.route('/proxy_download')
def proxy_download():
    target_url = request.args.get('url')
    req = requests.get(target_url, headers=HEADERS, stream=True)
    return Response(req.iter_content(chunk_size=1024*32), content_type=req.headers.get('Content-Type'))

if __name__ == "__main__":
    app.run()
