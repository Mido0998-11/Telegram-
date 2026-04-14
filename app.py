from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "Wizzy_Sovereign_Exclusive_Gate_2026"

TIKWM_API = "https://tikwm.com/api/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

# 1. الصفحة الأولى: بوابة التحقق السيادي
@app.route('/')
def verify_page():
    return render_template('verify.html')

# 2. استقبال نجاح التحقق
@app.route('/api/set_verified', methods=['POST'])
def set_verified():
    session['is_sovereign'] = True # إعطاء تذكرة العبور
    return jsonify({"success": True})

# 3. الصفحة الثانية: المنصة الرئيسية (ممنوع الدخول بدون تذكرة)
@app.route('/downloader')
def index():
    if not session.get('is_sovereign'):
        return redirect(url_for('verify_page'))
    return render_template('index.html')

# 4. محرك الاستخراج (API)
@app.route('/api/download', methods=['POST'])
def download():
    if not session.get('is_sovereign'):
        return jsonify({"success": False, "message": "فشل التحقق الأمني 🚫"}), 403
    
    video_url = request.json.get('url', '').lower()
    try:
        res = requests.post(TIKWM_API, data={"url": video_url, "hd": "1"}, headers=HEADERS, timeout=20).json()
        if res.get('code') == 0:
            return jsonify({"success": True, "data": res['data']})
        return jsonify({"success": False, "message": "السيرفر العالمي لم يجد الفيديو ⚠️"})
    except:
        return jsonify({"success": False, "message": "عطل في المكنة السيادية 🛠️"})

@app.route('/proxy_download')
def proxy_download():
    target_url = request.args.get('url')
    req = requests.get(target_url, headers=HEADERS, stream=True)
    return Response(req.iter_content(chunk_size=1024*16), content_type=req.headers.get('Content-Type'))

if __name__ == "__main__":
    app.run()
