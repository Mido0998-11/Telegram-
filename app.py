from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for
import requests
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "WIZZY_SOVEREIGN_FORCE_DOWNLOAD_2026"
app.permanent_session_lifetime = timedelta(days=7)

# إعدادات المحرك
API_URL = "https://tikwm.com/api/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

@app.route('/')
def gate():
    if session.get('is_verified'): return redirect(url_for('index'))
    return render_template('verify.html')

@app.route('/api/verify_success', methods=['POST'])
def verify_success():
    session['is_verified'] = True
    return jsonify({"success": True})

@app.route('/downloader')
def index():
    if not session.get('is_verified'): return redirect(url_for('gate'))
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def api_download():
    video_url = request.json.get('url', '').strip()
    try:
        res = requests.post(API_URL, data={"url": video_url, "hd": "1"}, headers=HEADERS).json()
        if res.get('code') == 0:
            return jsonify({"success": True, "data": res['data']})
        return jsonify({"success": False, "message": "الفيديو غير موجود"})
    except:
        return jsonify({"success": False, "message": "عطل في السيرفر"})

# 📥 محرك التحميل الإجباري (Forced Download Proxy)
@app.route('/proxy_download')
def proxy_download():
    target_url = request.args.get('url')
    filename = request.args.get('name', 'Wizzy_Sovereign_Video.mp4')
    
    # سحب الملف من سيرفر تيك توك
    req = requests.get(target_url, headers=HEADERS, stream=True)
    
    # إعداد رؤوس الاستجابة لإجبار التحميل
    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/octet-stream", # هذا النوع يجبر المتصفح على التحميل
    }
    
    return Response(
        req.iter_content(chunk_size=1024*64),
        headers=headers
    )

if __name__ == "__main__":
    app.run()
