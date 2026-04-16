from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)
app.secret_key = "WIZZY_SOVEREIGN_LEGENDARY_CITADEL_2026"

# --- واجهة "القلعة السيادية" (The Legendary 'Citadel' UI) ---

DOWNLOAD_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔱 Wizzy Sovereign | Legendary 'Citadel' UI</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"/>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@900&display=swap');
        
        :root { 
            --tiktok-cyan: #00f2ea; 
            --tiktok-pink: #ff0050; 
            --citadel-dark: #020617; /* لون خلفية أعمق */
        }

        body { 
            background: var(--citadel-dark); 
            color: #fff; 
            font-family: 'Cairo', sans-serif; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            min-height: 100vh; 
            margin: 0; 
            padding: 20px; 
            overflow: hidden; /* لمنع السكرول أثناء الأنيميشن */
        }

        /* توهج الخلفية "الشفقي" الدوامة (Dynamic Aura Swirl) */
        .bg-swirl {
            position: fixed; width: 100vw; height: 100vh; 
            background: radial-gradient(circle at 10% 10%, rgba(255, 0, 80, 0.08) 0%, transparent 50%),
                        radial-gradient(circle at 90% 90%, rgba(0, 242, 234, 0.08) 0%, transparent 50%),
                        radial-gradient(circle at 50% 50%, rgba(0,0,0,1) 0%, rgba(2, 6, 23, 1) 100%);
            filter: blur(10px); z-index: -2; 
            animation: swirlRotate 30s infinite linear;
        }
        @keyframes swirlRotate { from { filter: hue-rotate(0deg); } to { filter: hue-rotate(360deg); } }

        /* تراكب "الرماد" الصلب (Solid Ash Overlay) */
        .ash-overlay {
            position: fixed; inset: 0; background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5+AAAAIklEQVQIW2NkQAKrVq36z8gAFUOxGBmgAowuXbqM4QA8DAALVwsk7n1bNQAAAABJRU5ErkJggg==');
            opacity: 0.1; z-index: -1; pointer-events: none;
        }

        /* كارد "القلعة" بتأثير الزجاج المصقول (Glass Citadelle) */
        .citadel-card { 
            background: rgba(10, 10, 10, 0.8); 
            backdrop-filter: blur(25px); 
            -webkit-backdrop-filter: blur(25px);
            border: 2px solid rgba(255, 255, 255, 0.05);
            outline: 1px solid rgba(0, 0, 0, 0.8);
            border-radius: 40px; 
            width: 100%; 
            max-width: 500px; 
            text-align: center; 
            position: relative; 
            margin-top: 60px;
            box-shadow: 0 40px 100px -20px rgba(0, 0, 0, 1), 0 0 40px rgba(0, 242, 234, 0.05);
            transition: 0.5s;
        }

        /* درع النيون المزدوج المتوهج (Double Neon Shield) */
        .citadel-card::after { 
            content: ''; position: absolute; inset: -4px; padding: 4px; border-radius: 40px; 
            background: linear-gradient(90deg, transparent, var(--tiktok-cyan), var(--tiktok-pink), transparent); 
            -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0); 
            mask-composite: exclude; background-size: 200% auto; animation: beam 2.5s linear infinite; 
            pointer-events: none; 
            filter: blur(2px) brightness(1.2); /* تأثير Bloom كثيف */
        }
        @keyframes beam { to { background-position: 200% center; } }

        h1 { color: #ff0050; font-size: 3.5rem; margin: 0; font-weight: 900; letter-spacing: -3px; font-style: italic; filter: drop-shadow(0 0 15px rgba(255, 0, 80, 0.3));}
        .sub { color: #888; font-size: 11px; letter-spacing: 6px; font-weight: bold; margin-bottom: 40px; text-transform: uppercase; }
        
        input { 
            width: 85%; padding: 22px; border-radius: 20px; border: 2px solid #222; 
            background: #0d0d0d; color: var(--tiktok-cyan); font-size: 1.3rem; text-align: center; 
            margin-bottom: 25px; outline: none; transition: 0.3s;
            box-shadow: inset 0 5px 10px rgba(0,0,0,0.8);
        }
        input:focus { border-color: var(--tiktok-cyan); box-shadow: inset 0 2px 5px rgba(0,0,0,0.8), 0 0 20px rgba(0, 242, 234, 0.15); }

        /* زر الإشعال الأسطوري (Legendary Ignition Button) */
        .btn-ignition { 
            width: 90%; padding: 24px; border-radius: 20px; border: none; 
            background: linear-gradient(90deg, var(--tiktok-pink), #ff4d4d, var(--tiktok-pink)); 
            color: white; font-size: 1.7rem; font-weight: 900; cursor: pointer; 
            box-shadow: 0 8px 0 #800028, 0 10px 30px -5px rgba(255, 0, 80, 0.4); 
            transition: 0.15s ease-out; position: relative; overflow: hidden;
            animation: pulse-ignition 2s infinite;
        }
        @keyframes pulse-ignition { 0% { box-shadow: 0 8px 0 #800028, 0 10px 30px -5px rgba(255, 0, 80, 0.4); } 50% { box-shadow: 0 8px 0 #800028, 0 15px 50px rgba(255, 0, 80, 0.6); } 100% { box-shadow: 0 8px 0 #800028, 0 10px 30px -5px rgba(255, 0, 80, 0.4); } }
        .btn-ignition:hover { transform: translateY(2px) scale(1.01); box-shadow: 0 6px 0 #800028, 0 15px 60px rgba(255, 0, 80, 0.7); filter: brightness(1.1); }
        .btn-ignition:active { transform: translateY(6px); box-shadow: 0 2px 0 #800028, 0 5px 20px rgba(255, 0, 80, 0.3); }

        /* لوحة النتائج الأسطورية (The Artifact) */
        #result { display: none; margin-top: 40px; width: 100%; animation: artifactEntrance 0.7s ease-out; }
        @keyframes artifactEntrance { from { opacity: 0; transform: translateY(50px) scale(0.9); } to { opacity: 1; transform: translateY(0) scale(1); } }

        .cover-artifact { 
            width: 100%; border-radius: 30px; border: 4px solid #1a1a1a; 
            margin-bottom: 25px; transition: 0.3s;
            position: relative; overflow: hidden;
        }
        .cover-artifact::after {
            content:''; position: absolute; inset:0; background: linear-gradient(t, transparent, rgba(255,255,255,0.1), transparent);
            animation: shimmer-load 2s infinite; pointer-events: none;
        }
        @keyframes shimmer-load { from { transform: translateX(-100%); } to { transform: translateX(100%); } }

        /* أزرار التحميل بستايل الزجاج المصقول (Glass Artifacts) */
        .artifact-link { 
            display: block; padding: 22px; margin: 15px 0; border-radius: 18px; 
            text-decoration: none !important; font-weight: 900; color: #000; 
            background: linear-gradient(135deg, #00fff2, #00c8ff); 
            font-size: 1.2rem; transition: 0.2s; 
            border: 2px solid rgba(255, 255, 255, 0.1); outline: 1px solid rgba(0,0,0,0.5);
            box-shadow: 0 10px 30px -10px rgba(0, 242, 234, 0.3);
        }
        .artifact-link:hover { transform: scale(1.03); box-shadow: 0 15px 50px -10px rgba(0, 242, 234, 0.5); filter: brightness(1.1); }
        .bg-mp3 { background: linear-gradient(135deg, #fff, #bbb) !important; color: #000 !important;}
        .bg-mp3:hover { box-shadow: 0 15px 50px -10px rgba(255, 255, 255, 0.2) !important;}
    </style>
</head>
<body>
    <div class="bg-swirl"></div>
    <div class="ash-overlay"></div>

    <div class="citadel-card p-10 shadow-2xl animate__animated animate__zoomIn">
        <h1>WIZZY</h1>
        <div class="sub">Legendary 'Citadel' UI V100</div>

        <input type="text" id="url" placeholder="ضع رابط الإبداع (TikTok) هنا يا ملك...">
        
        <button onclick="startDownload()" class="btn-ignition animate__animated animate__pulse animate__infinite">
             <i class="fa-solid fa-bolt-lightning mr-3"></i> استخراج وتشغيل 🔱
        </button>

        <div id="result">
            <div class="relative rounded-3xl overflow-hidden mb-6 border-4 border-[#1a1a1a]">
                <img id="cover" class="w-full h-80 object-cover" src="">
                <div class="absolute inset-0 bg-gradient-to-t from-black flex items-end p-6">
                    <h3 id="vid-title" class="text-white font-black text-lg truncate w-full"></h3>
                </div>
            </div>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <a id="hd" class="artifact-link no-underline" href="#">
                     <i class="fa-solid fa-video mr-3"></i> تحميل فيديو HD
                </a>
                <a id="mp3" class="artifact-link bg-mp3 no-underline" href="#">
                     <i class="fa-solid fa-music mr-3"></i> تحميل الصوت MP3
                </a>
            </div>
            <p class="text-center text-[10px] text-gray-500 mt-6 font-bold uppercase tracking-widest">Wizzy Sovereign Extraction System</p>
        </div>
    </div>

    <footer class="mt-auto py-12 text-center w-full bg-black/50 backdrop-blur-sm border-t border-white/5">
        <span class="text-xl font-black italic tracking-tighter" style="color: #ff0050;">WIZZY <span style="color: #fff; text-shadow: 0 0 10px #00f2ea;">SOVEREIGN EMPIRE</span></span>
        <p class="text-[9px] text-gray-600 font-black tracking-[0.4em] uppercase mt-2">God-Tier Technology © 2026</p>
    </footer>

    <script>
        // التعامل مع الروابط القادمة من صفحة البحث
        window.onload = () => {
            const params = new URLSearchParams(window.location.search);
            if(params.has('url')) {
                const targetUrl = params.get('url');
                document.getElementById('url').value = targetUrl;
                // تأخير بسيط لضمان استقرار الصفحة
                setTimeout(() => { startDownload(); }, 600);
            }
        }

        // تنبيه سيادي مكثف (Intense Black Toast)
        function notify(msg) {
            Swal.fire({
                toast: true, position: 'top-end', icon: 'success',
                title: msg, showConfirmButton: false, timer: 3000, 
                background: '#0a0a0a', color: '#fff', 
                timerProgressBar: true,
                customClass: { popup: 'border-2 border-[var(--tiktok-cyan)]', timerProgressBar: 'bg-[var(--tiktok-cyan)]' }
            });
        }

        async function startDownload() {
            const val = document.getElementById('url').value;
            if(!val) return Swal.fire({ icon: 'warning', title: 'الرابط مفقود', text: 'أين الرابط يا ملك؟', background: '#0a0a0a', color: '#fff' });

            // لودينج سيادي مكثف
            Swal.fire({ 
                title: 'جاري استخراج القوة...', 
                allowOutsideClick: false, 
                didOpen: () => Swal.showLoading(), 
                background: '#0a0a0a', 
                color: '#fff', 
                customClass: { title: 'text-2xl font-black', popup: 'border-2 border-[var(--tiktok-pink)]', loading: 'text-[var(--tiktok-pink)]' }
            });

            try {
                const response = await fetch('/api/download', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: val})
                });
                const res = await response.json();
                
                if(res.success) {
                    const d = res.data;
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('cover').src = d.cover;
                    document.getElementById('vid-title').innerText = d.title || "Wizzy Sovereign Content";
                    
                    // إعداد روابط التحميل الإجباري
                    document.getElementById('hd').href = `/proxy?url=${encodeURIComponent(d.hdplay || d.play)}&name=Wizzy_HD.mp4`;
                    document.getElementById('mp3').href = `/proxy?url=${encodeURIComponent(d.music)}&name=Wizzy_Audio.mp3`;
                    
                    Swal.close();
                    notify('تم استخراج القوة ✅ الملفات جاهزة');
                    window.scrollTo({ top: document.getElementById('result').offsetTop - 20, behavior: 'smooth' });
                } else {
                    Swal.fire({ icon: 'error', title: 'فشل العملية', text: 'السيرفر العالمي لم يستجب، جرب رابط آخر.', background: '#0a0a0a', color: '#fff' });
                }
            } catch(e) {
                Swal.fire({ icon: 'error', title: 'خطأ عابر', text: 'المكينة تحتاج صيانة سريعة 🛠️', background: '#0a0a0a', color: '#fff' });
            }
        }
    </script>
</body>
</html>
"""

# --- منطق السيرفر الصافي والموزع (Distributor Backend) ---

@app.route('/')
def index():
    # الدخول المباشر لقاعة العرش الأسطورية
    return DOWNLOAD_HTML

@app.route('/api/download', methods=['POST'])
def download():
    url = request.json.get('url', '')
    try:
        # الاتصال بالمحرك العالمي بنفس الطريقة الشغالة (HTTP Post)
        # نستخدم Headers و Cookie لضمان المرور
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "current_language=en",
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
        }
        r = requests.post("https://tikwm.com/api/", data={"url": url, "hd": "1"}, headers=headers).json()
        if r.get('code') == 0:
            return jsonify({"success": True, "data": r['data']})
        return jsonify({"success": False})
    except Exception as e:
        print(e)
        return jsonify({"success": False})

@app.route('/proxy')
def proxy():
    target = request.args.get('url')
    filename = request.args.get('name', 'Wizzy_Video.mp4')
    
    # محرك جلب الملف المباشر
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
    }
    req = requests.get(target, headers=headers, stream=True)
    
    # إجبار التحميل المباشر وباسم فخم
    response_headers = {
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/octet-stream",
    }
    
    # توزيع الملف بالقطع (Chunked Response)
    return Response(req.iter_content(chunk_size=1024*64), headers=response_headers)

if __name__ == "__main__":
    app.run()
