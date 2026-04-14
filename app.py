from flask import Flask, render_template, request, jsonify, Response, session
import requests
import urllib3

# إيقاف تحذيرات الأمان المزعجة
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.secret_key = "Wizzy_Sovereign_Ironclad_2026"

# 🔱 المحرك العالمي (TikWM)
API_URL = "https://www.tikwm.com/api/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url', '')
    is_verified = data.get('verified', False)

    if not is_verified:
        return jsonify({"success": False, "message": "تخطى التحقق أولاً يا ملك 🚫"}), 403

    # قناع احترافي جداً (نفس متصفح الموبايل)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    payload = {'url': video_url, 'hd': '1'}

    try:
        # المحاولة الأولى بالـ API الأساسي
        response = requests.post(API_URL, data=payload, headers=headers, timeout=25, verify=False)
        
        # كود تشخيصي (Diagnostics)
        if response.status_code != 200:
            return jsonify({
                "success": False, 
                "message": f"السيرفر العالمي رفض الطلب (خطأ {response.status_code}) 🚫"
            })

        res_data = response.json()
        
        if res_data.get('code') == 0:
            return jsonify({"success": True, "data": res_data['data']})
        else:
            return jsonify({
                "success": False, 
                "message": f"تنبيه من السيرفر: {res_data.get('msg', 'رابط غير صالح')} ⚠️"
            })

    except Exception as e:
        return jsonify({"success": False, "message": "المكنة واجهت مشكلة في الاتصال، جرب مرة تانية 🛠️"})

@app.route('/proxy_download')
def proxy_download():
    target_url = request.args.get('url')
    filename = request.args.get('name', 'Wizzy_TikTok.mp4')
    if not target_url: return "مفقود", 400
    
    # تحميل الفيديو بـ Stream لضمان السرعة
    req = requests.get(target_url, stream=True, verify=False)
    return Response(
        req.iter_content(chunk_size=1024*32),
        content_type=req.headers.get('Content-Type'),
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

if __name__ == "__main__":
    app.run()
