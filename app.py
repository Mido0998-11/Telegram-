from flask import Flask, render_template, request, jsonify, Response
import requests

app = Flask(__name__)

# المحرك العالمي
TIKWM_API = "https://tikwm.com/api/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download():
    video_url = request.json.get('url')
    if not video_url:
        return jsonify({"success": False, "message": "يا ملك، أين الرابط؟ 🔱"}), 400
    
    try:
        # طلب البيانات مع مهلة زمنية ذكية
        res = requests.post(TIKWM_API, data={"url": video_url, "hd": "1"}, timeout=15).json()
        if res.get('code') == 0:
            return jsonify({"success": True, "data": res['data']})
        return jsonify({"success": False, "message": "السيرفر لم يستجب، تأكد من الرابط 🚫"})
    except Exception as e:
        return jsonify({"success": False, "message": "عطل في المكنة السيادية 🛠️"})

@app.route('/proxy_download')
def proxy_download():
    target_url = request.args.get('url')
    filename = request.args.get('name', 'Wizzy_Sovereign.mp4')
    if not target_url:
        return "الرابط مفقود", 400
    
    # تحويل الفيديو لتدفق بيانات لإجبار التحميل المباشر
    req = requests.get(target_url, stream=True)
    return Response(
        req.iter_content(chunk_size=4096),
        content_type=req.headers.get('Content-Type'),
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

if __name__ == "__main__":
    app.run()
