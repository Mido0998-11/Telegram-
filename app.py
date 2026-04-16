from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)
# السكرت كي لم يعد ضرورياً بشدة بعد إلغاء التحقق ولكن سنتركه لاستقرار Flask
app.secret_key = "WIZZY_SOVEREIGN_DIRECT_ACCESS_2026"

# --- واجهة التحميل المباشرة (Direct Access UI) ---

DOWNLOAD_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔱 Wizzy Sovereign | TikTok Direct</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@900&display=swap');
        
        body { 
            background: #000; 
            color: #fff; 
            font-family: 'Cairo', sans-serif; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            min-height: 100vh; 
            margin: 0; 
            padding: 20px; 
        }

        /* توهج رماد الخرطوم */
        .bg-glow {
            position: fixed; width: 500px; height: 500px; 
            background: radial-gradient(circle, rgba(0, 242, 234, 0.05) 0%, transparent 70%); 
            filter: blur(100px); z-index: -1; top: -10%; left: -10%;
        }

        .main-card { 
            background: #0a0a0a; 
            border: 4px solid #1a1a1a; 
            padding: 40px 20px; 
            border-radius: 35px; 
            width: 100%; 
            max-width: 500px; 
            text-align: center; 
            position: relative; 
            margin-top: 60px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        }

        /* خطوط النيون السيادية المتوهجة */
        .main-card::after { 
            content: ''; position: absolute; inset: -4px; padding: 4px; border-radius: 35px; 
            background: linear-gradient(90deg, #ff0050, #00f2ea, #ff0050); 
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0); 
            mask-composite: exclude; background-size: 200% auto; animation: beam 3s linear infinite; 
            pointer-events: none; 
        }
        @keyframes beam { to { background-position: 200% center; } }

        h1 { color: #ff0050; font-size: 3.5rem; margin: 0; font-weight: 900; letter-spacing: -2px; }
        .sub { color: #555; font-size: 10px; letter-spacing: 5px; font-weight: bold; margin-bottom: 35px; text-transform: uppercase; }
        
        input { 
            width: 85%; padding: 20px; border-radius: 18px; border: 2px solid #333; 
            background: #111; color: #00f2ea; font-size: 1.2rem; text-align: center; 
            margin-bottom: 25px; outline: none; transition: 0.3s;
        }
        input:focus { border-color: #00f2ea; box-shadow: 0 0 15px rgba(0, 242, 234, 0.2); }

        button { 
            width: 90%; padding: 22px; border-radius: 18px; border: none; 
            background: linear-gradient(45deg, #ff0050, #ff4d4d); 
            color: white; font-size: 1.6rem; font-weight: 900; cursor: pointer; 
            box-shadow: 0 7px 0 #800028; transition: 0.1s; 
        }
        button:active { transform: translateY(4px); box-shadow: 0 2px 0 #800028; }

        /* النتائج */
        #result { display: none; margin-top: 35px; width: 100%; animation: fadeInUp 0.5s; }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

        img { width: 100%; border-radius: 25px; border: 3px solid #1a1a1a; margin-bottom: 25px; }
        
        .dl-btn { 
            display: block; padding: 20px; margin: 12px 0; border-radius: 15px; 
            text-decoration: none; font-weight: 900; color: #000; 
            background: #00f2ea; font-size: 1.1rem; transition: 0.3s;
        }
        .dl-btn:hover { transform: scale(1.02); filter: brightness(1.1); }
        .bg-white { background: #fff !important; }
    </style>
</head>
<body>
    <div class="bg-glow"></div>

    <div class="main-card">
        <h1>WIZZY</h1>
        <div class="sub">Sovereign Direct Access</div>

        <input type="text" id="url" placeholder="ضع رابط التيك توك هنا...">
        
        <button onclick="startDownload()">
             استخراج القوة 🔱
        </button>

        <div id="result">
            <img id="cover" src="">
            <a id="hd" class="dl-btn" href="#">تحميل فيديو HD 🎥</a>
            <a id="mp3" class="dl-btn bg-white" href="#">تحميل صوت MP3 🎵</a>
        </div>
    </div>

    <div style="margin-top: 50px; color: #222; font-weight: 900; font-size: 11px; letter-spacing: 3px;">
        WIZZY ASH EMPIRE © 2026
    </div>

    <script>
        async function startDownload() {
            const urlInput = document.getElementById('url').value;
            if(!urlInput) return alert("أين الرابط يا ملك؟");

            const btn = document.querySelector('button');
            btn.innerText = "جاري الاستخراج...";

            try {
                const response = await fetch('/api/download', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: urlInput})
                });
                const res = await response.json();
                
                if(res.success) {
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('cover').src = res.data.cover;
                    
                    // إعداد الروابط للتحميل المباشر (Forced Download)
                    document.getElementById('hd').href = `/proxy?url=` + encodeURIComponent(res.data.hdplay || res.data.play) + `&name=Wizzy_HD.mp4`;
                    document.getElementById('mp3').href = `/proxy?url=` + encodeURIComponent(res.data.music) + `&name=Wizzy_Audio.mp3`;
                    
                    btn.innerText = "تم الاستخراج ✅";
                    setTimeout(() => { btn.innerText = "استخراج القوة 🔱"; }, 3000);
                } else {
                    alert("عذراً! الرابط غير صالح أو الفيديو خاص.");
                    btn.innerText = "استخراج القوة 🔱";
                }
            } catch(e) {
                alert("خطأ في الاتصال بمحرك السيادة 🛠️");
                btn.innerText = "استخراج القوة 🔱";
            }
        }
    </script>
</body>
</html>
"""

# --- منطق السيرفر الصافي (Clean Backend) ---

@app.route('/')
def index():
    # الدخول المباشر لواجهة التحميل
    return DOWNLOAD_HTML

@app.route('/api/download', methods=['POST'])
def download():
    url = request.json.get('url', '')
    try:
        # الاتصال بالمحرك العالمي
        r = requests.post("https://tikwm.com/api/", data={"url": url, "hd": "1"}).json()
        if r.get('code') == 0:
            return jsonify({"success": True, "data": r['data']})
        return jsonify({"success": False})
    except:
        return jsonify({"success": False})

@app.route('/proxy')
def proxy():
    target = request.args.get('url')
    filename = request.args.get('name', 'Wizzy_Video.mp4')
    
    # جلب الملف
    req = requests.get(target, stream=True)
    
    # إجبار التحميل المباشر (Forced Download)
    headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/octet-stream",
    }
    
    return Response(req.iter_content(chunk_size=1024*64), headers=headers)

if __name__ == "__main__":
    app.run()
