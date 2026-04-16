from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)
app.secret_key = "WIZZY_SOVEREIGN_PROFESSIONAL_2026"

# --- الواجهة المهنية (Professional UI) ---

DOWNLOAD_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wizzy Sovereign | TikTok Downloader</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"/>

    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
        
        :root { 
            --primary-color: #00f2ea; 
            --accent-color: #ff0050; 
            --bg-dark: #0a0a0a;
        }

        body { 
            background: var(--bg-dark); 
            color: #ffffff; 
            font-family: 'Cairo', sans-serif; 
            margin: 0; 
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
        }

        /* حاوية التصميم الرئيسية - احترافية وبسيطة */
        .main-container { 
            background: rgba(20, 20, 20, 0.6); 
            backdrop-filter: blur(20px); 
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px; 
            width: 100%; 
            max-width: 600px; 
            padding: 40px 20px;
            margin-top: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            text-align: center;
        }

        .header-section { margin-bottom: 30px; }
        .header-section h1 { font-size: 2.2rem; font-weight: 900; margin-bottom: 8px; color: #fff; }
        .header-section p { color: #888; font-size: 0.9rem; font-weight: 400; }

        input { 
            width: 90%; padding: 18px; border-radius: 14px; border: 1px solid #333; 
            background: #111; color: var(--primary-color); font-size: 1rem; text-align: center; 
            margin-bottom: 20px; outline: none; transition: 0.3s;
        }
        input:focus { border-color: var(--primary-color); background: #151515; }

        /* زر التحميل الرسمي */
        .btn-download { 
            width: 90%; padding: 18px; border-radius: 14px; border: none; 
            background: linear-gradient(90deg, var(--accent-color), #e60045); 
            color: #fff; font-size: 1.1rem; font-weight: 700; cursor: pointer; 
            transition: 0.3s ease; box-shadow: 0 4px 15px rgba(255, 0, 80, 0.2);
        }
        .btn-download:hover { transform: translateY(-2px); filter: brightness(1.1); box-shadow: 0 6px 20px rgba(255, 0, 80, 0.3); }

        /* منطقة النتائج */
        #result-area { display: none; margin-top: 35px; border-top: 1px solid #222; padding-top: 30px; width: 100%; }
        .video-thumbnail { width: 100%; border-radius: 18px; border: 1px solid #333; margin-bottom: 20px; }

        .download-option {
            display: flex; align-items: center; justify-content: center; gap: 10px;
            padding: 15px; border-radius: 12px; font-weight: 700; text-decoration: none;
            transition: 0.2s; margin: 10px 0; font-size: 1rem;
        }
        .video-hd { background: var(--primary-color); color: #000; }
        .audio-mp3 { background: #fff; color: #000; }
        .download-option:hover { opacity: 0.9; transform: scale(1.01); }

        /* أيقونات التواصل الاجتماعي بحجم مناسب */
        .social-icon { font-size: 1.2rem; color: #666; transition: 0.3s; }
        .social-icon:hover { color: #fff; }

        /* الفوتر المهني */
        .footer-credits {
            margin-top: auto; padding: 40px 20px; text-align: center; color: #444; font-size: 0.8rem;
        }
        .wizzy-brand { color: #888; font-weight: 700; text-decoration: none; }
    </style>
</head>
<body>

    <div class="main-container">
        <div class="header-section">
            <div class="flex justify-center mb-4">
                <i class="fa-brands fa-tiktok text-3xl" style="color: var(--accent-color);"></i>
            </div>
            <h1>Wizzy Sovereign</h1>
            <p>أداة مهنية لتحميل فيديوهات تيك توك بجودة عالية وبدون علامة مائية</p>
        </div>

        <input type="text" id="videoUrl" placeholder="الصق رابط فيديو تيك توك هنا">
        <button onclick="handleDownload()" class="btn-download">
            <i class="fa-solid fa-download ml-2"></i> بدء التحميل
        </button>

        <div id="result-area">
            <img id="videoPreview" class="video-thumbnail" src="">
            <div id="videoTitle" class="text-sm text-gray-400 mb-4 px-4"></div>
            
            <div class="px-4">
                <a id="hdDownload" class="download-option video-hd" href="#">
                    <i class="fa-solid fa-video"></i> تحميل فيديو (MP4 HD)
                </a>
                <a id="mp3Download" class="download-option audio-mp3" href="#">
                    <i class="fa-solid fa-music"></i> تحميل الملف الصوتي (MP3)
                </a>
            </div>
        </div>
    </div>

    <div class="footer-credits">
        <p class="mb-4">جميع الحقوق محفوظة © 2026</p>
        <div class="flex justify-center gap-6 mb-6">
            <a href="#" class="social-icon"><i class="fa-brands fa-github"></i></a>
            <a href="#" class="social-icon"><i class="fa-brands fa-instagram"></i></a>
            <a href="#" class="social-icon"><i class="fa-brands fa-telegram"></i></a>
        </div>
        <p>تم التطوير بواسطة <a href="#" class="wizzy-brand">Wizzy Sovereign System</a></p>
    </div>

    <script>
        async function handleDownload() {
            const url = document.getElementById('videoUrl').value;
            if(!url) return Swal.fire({ icon: 'info', title: 'تنبيه', text: 'يرجى إدخال رابط صالح', background: '#111', color: '#fff' });

            Swal.fire({ 
                title: 'جاري المعالجة', 
                text: 'يرجى الانتظار قليلاً...',
                allowOutsideClick: false, 
                didOpen: () => Swal.showLoading(), 
                background: '#111', 
                color: '#fff' 
            });

            try {
                const response = await fetch('/api/process', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url: url})
                });
                const res = await response.json();
                
                if(res.status === 'success') {
                    const data = res.data;
                    document.getElementById('result-area').style.display = 'block';
                    document.getElementById('videoPreview').src = data.cover;
                    document.getElementById('videoTitle').innerText = data.title || "فيديو تيك توك";
                    
                    document.getElementById('hdDownload').href = `/proxy_file?url=${encodeURIComponent(data.hdplay || data.play)}&filename=video.mp4`;
                    document.getElementById('mp3Download').href = `/proxy_file?url=${encodeURIComponent(data.music)}&filename=audio.mp3`;
                    
                    Swal.close();
                } else {
                    Swal.fire({ icon: 'error', title: 'خطأ', text: 'فشل جلب بيانات الفيديو، تأكد من صحة الرابط', background: '#111', color: '#fff' });
                }
            } catch(e) {
                Swal.fire({ icon: 'error', title: 'خطأ تقني', text: 'حدث خطأ أثناء الاتصال بالخادم', background: '#111', color: '#fff' });
            }
        }
    </script>
</body>
</html>
"""

# --- منطق الخادم الاحترافي (Backend Logic) ---

@app.route('/')
def home():
    return DOWNLOAD_HTML

@app.route('/api/process', methods=['POST'])
def process_request():
    video_url = request.json.get('url', '')
    try:
        # استخدام هيدرز احترافية لتجنب الحظر
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }
        r = requests.post("https://tikwm.com/api/", data={"url": video_url, "hd": "1"}, headers=headers).json()
        if r.get('code') == 0:
            return jsonify({"status": "success", "data": r['data']})
        return jsonify({"status": "error"})
    except:
        return jsonify({"status": "error"})

@app.route('/proxy_file')
def proxy_file():
    target_url = request.args.get('url')
    filename = request.args.get('filename', 'download.mp4')
    
    headers = {"User-Agent": "Mozilla/5.0"}
    req = requests.get(target_url, headers=headers, stream=True)
    
    return Response(
        req.iter_content(chunk_size=1024*64),
        headers={
            "Content-Disposition": f"attachment; filename={filename}",
            "Content-Type": "application/octet-stream"
        }
    )

if __name__ == "__main__":
    app.run()
