from flask import Flask, render_template, request, jsonify, Response, session
import requests

app = Flask(__name__)
app.secret_key = "Wizzy_Sovereign_Secret_Key_2026_V2"

# 🔱 المحرك العالمي المطور
TIKWM_API = "https://tikwm.com/api/"

# 🎭 قناع التنكر (Headers) عشان السيرفر يفتكرنا متصفح حقيقي
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url', '').lower()
    is_verified = data.get('verified', False)

    # 1. نظام الحماية السيادي
    if not is_verified:
        return jsonify({"success": False, "message": "يجب تخطي نظام التحقق العالمي أولاً 🚫"}), 403

    # 2. تخصيص تيك توك
    if "tiktok.com" not in video_url and "v.douyin.com" not in video_url:
        return jsonify({"success": False, "message": "هذا المحرك لـ TikTok فقط! ⚠️"}), 400

    try:
        # إرسال الطلب مع "القناع" الجديد
        response = requests.post(TIKWM_API, data={"url": video_url, "hd": "1"}, headers=HEADERS, timeout=20)
        res = response.json()
        
        if res.get('code') == 0:
            return jsonify({"success": True, "data": res['data']})
        
        # رسالة خطأ ذكية في حال فشل السيرفر الخارجي
        return jsonify({"success": False, "message": "السيرفر العالمي مشغول حالياً، جرب رابط آخر أو أعد المحاولة ⏳"})
    
    except Exception as e:
        print(f"Error: {e}") # حتظهر في سجلات Render
        return jsonify({"success": False, "message": "حدث عطل في الاتصال.. المكنة تحتاج صيانة سريعة 🛠️"})

@app.route('/proxy_download')
def proxy_download():
    target_url = request.args.get('url')
    filename = request.args.get('name', 'Wizzy_TikTok_Sovereign.mp4')
    
    # التحميل مع القناع لضمان عدم الحظر أثناء سحب الملف
    req = requests.get(target_url, headers=HEADERS, stream=True)
    return Response(
        req.iter_content(chunk_size=1024*16),
        content_type=req.headers.get('Content-Type'),
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

if __name__ == "__main__":
    app.run()
