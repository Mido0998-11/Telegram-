from flask import Flask, render_template, request, jsonify, Response, session
import requests
import random

app = Flask(__name__)
app.secret_key = "Wizzy_Sovereign_Secret_Key_2026" # مفتاح الأمان للسيادة

TIKWM_API = "https://tikwm.com/api/"

@app.route('/')
def index():
    return render_template('index.html')

# 1. دالة لتوليد سؤال "تحقق بشري" حقيقي
@app.route('/api/get_challenge', methods=['GET'])
def get_challenge():
    num1 = random.randint(1, 15)
    num2 = random.randint(1, 15)
    session['captcha_answer'] = num1 + num2 # حفظ الإجابة في السيرفر
    return jsonify({"question": f"كم حاصل جمع {num1} + {num2} ؟"})

# 2. دالة التحميل (لا تعمل إلا بالتحقق)
@app.route('/api/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('url')
    user_answer = data.get('answer') # إجابة المستخدم

    # التحقق الحقيقي من السيرفر
    correct_answer = session.get('captcha_answer')
    
    if correct_answer is None or str(user_answer) != str(correct_answer):
        return jsonify({"success": False, "message": "فشل التحقق! أنت لست بشراً سيادياً 🚫"}), 403

    # لو التحقق نجح، بنمسح الإجابة القديمة ونكمل التحميل
    session.pop('captcha_answer', None)

    try:
        res = requests.post(TIKWM_API, data={"url": video_url, "hd": "1"}, timeout=15).json()
        if res.get('code') == 0:
            return jsonify({"success": True, "data": res['data']})
        return jsonify({"success": False, "message": "لم يتم العثور على الفيديو 🚫"})
    except:
        return jsonify({"success": False, "message": "عطل في المكنة السيادية 🛠️"})

@app.route('/proxy_download')
def proxy_download():
    target_url = request.args.get('url')
    if not target_url: return "مفقود", 400
    req = requests.get(target_url, stream=True)
    return Response(req.iter_content(chunk_size=4096), content_type=req.headers.get('Content-Type'),
                    headers={"Content-Disposition": "attachment; filename=Wizzy_Sovereign.mp4"})

if __name__ == "__main__":
    app.run()
