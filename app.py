from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for
import requests
from datetime import timedelta

app = Flask(__name__)

# 🔱 إعدادات السيادة (الإصدار العابر للحدود)
app.secret_key = "WIZZY_EMPIRE_ULTIMATE_KEY_2026" 
app.permanent_session_lifetime = timedelta(days=30) # التذكرة تدوم شهر كامل

# إعدادات الكوكيز (تم التعديل لضمان القبول في الموبايل)
app.config.update(
    SESSION_COOKIE_SECURE=False,   # غيرناها لـ False عشان تشتغل في كل الحالات
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

API_URL = "https://tikwm.com/api/"
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "current_language=en",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
}

@app.route('/')
def verify_gate():
    # لو اليوزر محقق، ندخله طوالي
    if session.get('is_verified') == True:
        return redirect(url_for('downloader_page'))
    return render_template('verify.html')

@app.route('/api/verify_success', methods=['POST'])
def verify_success():
    session.permanent = True # تثبيت الجلسة
    session['is_verified'] = True
    return jsonify({"success": True})

@app.route('/downloader')
def downloader_page():
    if not session.get('is_verified'):
        return redirect(url_for('verify_gate'))
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def api_download():
    if not session.get('is_verified'):
        return jsonify({"success": False, "message": "انتهت الجلسة 🚫"}), 403
    
    video_url = request.json.get('url', '').strip()
    try:
        res = requests.post(API_URL, data={"url": video_url, "hd": "1"}, headers=HEADERS).json()
        if res.get('code') == 0:
            return jsonify({"success": True, "data": res['data']})
        return jsonify({"success": False, "message": "الفيديو غير موجود"})
    except:
        return jsonify({"success": False, "message": "عطل فني 🛠️"})

@app.route('/proxy_download')
def proxy_download():
    target_url = request.args.get('url')
    req = requests.get(target_url, headers=HEADERS, stream=True)
    return Response(req.iter_content(chunk_size=1024*32), content_type=req.headers.get('Content-Type'))

if __name__ == "__main__":
    app.run()
