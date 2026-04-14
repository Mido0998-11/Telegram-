from flask import Flask, render_template, request, jsonify, Response, session
import requests

app = Flask(__name__)
app.secret_key = "Wizzy_Sovereign_Omega_Final_2026"

TIKWM_API = "https://tikwm.com/api/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url', '').lower()
    is_verified = data.get('verified', False)

    # 1. نظام الحماية السيادي (Backend Check)
    if not is_verified:
        return jsonify({"success": False, "message": "يجب تخطي نظام التحقق العالمي أولاً 🚫"}), 403

    # 2. تخصيص تيك توك (TikTok Only)
    if "tiktok.com" not in video_url and "v.douyin.com" not in video_url:
        return jsonify({"success": False, "message": "هذا المحرك مخصص لـ TikTok فقط يا ملك! ⚠️"}), 400

    try:
        res = requests.post(TIKWM_API, data={"url": video_url, "hd": "1"}, timeout=15).json()
        if res.get('code') == 0:
            return jsonify({"success": True, "data": res['data']})
        return jsonify({"success": False, "message": "تعذر العثور على الفيديو، تأكد من الرابط."})
    except:
        return jsonify({"success": False, "message": "عطل في الاتصال العالمي بالسيرفرات 🛠️"})

@app.route('/proxy_download')
def proxy_download():
    target_url = request.args.get('url')
    filename = request.args.get('name', 'Wizzy_TikTok_Sovereign.mp4')
    req = requests.get(target_url, stream=True)
    return Response(
        req.iter_content(chunk_size=1024*8),
        content_type=req.headers.get('Content-Type'),
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

if __name__ == "__main__":
    app.run()
