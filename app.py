from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
TIKWM_API = "https://tikwm.com/api/"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url')
    if not video_url:
        return jsonify({"success": False, "message": "الرجاء وضع الرابط أولاً"}), 400
    
    try:
        res = requests.post(TIKWM_API, data={"url": video_url, "hd": "1"}).json()
        if res.get('code') == 0:
            return jsonify({"success": True, "data": res['data']})
        return jsonify({"success": False, "message": "تعذر العثور على الفيديو"})
    except:
        return jsonify({"success": False, "message": "خطأ في الاتصال بالسيرفر"})

if __name__ == "__main__":
    app.run()

