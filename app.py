from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
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
        # إضافة Timeout لضمان سرعة الاستجابة
        res = requests.post(TIKWM_API, data={"url": video_url, "hd": "1"}, timeout=10).json()
        if res.get('code') == 0:
            return jsonify({"success": True, "data": res['data']})
        return jsonify({"success": False, "message": "السيرفر العالمي لم يجد الفيديو 🚫"})
    except Exception as e:
        return jsonify({"success": False, "message": "حدث عطل فني في المكنة 🛠️"})

if __name__ == "__main__":
    app.run()
