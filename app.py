from flask import Flask, render_template, request, jsonify, Response, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "Wizzy_Sovereign_CodeBreaker_2026"

# 🔱 المحرك المستخرج من الكود الشغال
API_URL = "https://tikwm.com/api/"

# الإعدادات السرية التي تجعل المحرك لا يتوقف
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "current_language=en",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
}

# 1. بوابة التحقق
@app.route('/')
def verify_gate():
    if session.get('is_verified'):
        return redirect(url_for('downloader'))
    return render_template('verify.html')

@app.route('/api/verify_success', methods=['POST'])
def verify_success():
    session['is_verified'] = True
    return jsonify({"success": True})

# 2. المنصة الرئيسية
@app.route('/downloader')
def downloader():
    if not session.get('is_verified'):
        return redirect(url_for('verify_gate'))
    return render_template('index.html')

# 3. محرك الجلب (تم تحديثه بالكود الذي أرسلته)
@app.route('/api/download', methods=['POST'])
def download():
    if not session.get('is_verified'):
        return jsonify({"success": False, "message": "فشل التحقق الأمني 🚫"}), 403

    video_url = request.json.get('url', '').strip()
    if not video_url:
        return jsonify({"success": False, "message": "أين الرابط يا ملك؟"})

    try:
        # إرسال البيانات بنفس طريقة الكود الشغال (Encoded Params)
        payload = {
            "url": video_url,
            "hd": "1"
        }
        
        response = requests.post(API_URL, data=payload, headers=HEADERS, timeout=20)
        res_json = response.json()
        
        if res_json.get('code') == 0:
            return jsonify({"success": True, "data": res_json['data']})
        
        return jsonify({"success": False, "message": "السيرفر العالمي لم يستجب، تأكد من الرابط."})

    except Exception as e:
        return jsonify({"success": False, "message": "عطل مفاجئ في المكنة، أعد المحاولة 🛠️"})

@app.route('/proxy_download')
def proxy_download():
    target_url = request.args.get('url')
    # نستخدم نفس الـ Headers هنا لضمان التحميل
    req = requests.get(target_url, headers=HEADERS, stream=True)
    return Response(req.iter_content(chunk_size=1024*32), content_type=req.headers.get('Content-Type'))

if __name__ == "__main__":
    app.run()
