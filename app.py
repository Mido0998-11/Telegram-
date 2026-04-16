from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)
app.secret_key = "WIZZY_SOVEREIGN_PRO_V2_2026"

# --- الواجهة المهنية المحدثة (Professional UI - Large Input) ---

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
            --bg-dark: #070707;
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

        .main-container { 
            background: rgba(15, 15, 15, 0.7); 
            backdrop-filter: blur(25px); 
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 30px; 
            width: 100%; 
            max-width: 650px; 
            padding: 50px 25px;
            margin-top: 50px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.6);
            text-align: center;
        }

        .header-section h1 { font-size: 2.5rem; font-weight: 900; margin-bottom: 10px; }
        .header-section p { color: #777; font-size: 1rem; margin-bottom: 40px; }

        /* خانة الرابط الكبيرة (Large Input Area) */
        input { 
            width: 95%; 
            padding: 25px; /* تم التكبير هنا */
            border-radius: 18px; 
            border: 2px solid #222; 
            background: #0c0c0c; 
            color: var(--primary-color); 
            font-size: 1.25rem; /* تم تكبير الخط */
            text-align: center; 
            margin-bottom: 25px; 
            outline: none; 
            transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
        }
        input:focus { 
            border-color: var(--primary-color); 
            background: #111;
            box-shadow: 0 0 25px rgba(0, 242, 234, 0.15), inset 0 2px 10px rgba(0,0,0,0.5); 
        }

        .btn-download { 
            width: 95%; 
            padding: 22px; 
            border-radius: 18px; 
            border: none; 
            background: linear-gradient(90deg, var(--accent-color), #d60043); 
            color: #fff; 
            font-size: 1.3rem; 
            font-weight: 900; 
            cursor: pointer; 
            transition: 0.3s;
            box-shadow: 0 8px 20px rgba(255, 0, 80, 0.2);
        }
        .btn-download:hover { transform: translateY(-3px); filter: brightness(1.1); box-shadow: 0 12px 30px rgba(255, 0, 80, 0.4); }

        #result-area { display: none; margin-top: 40px; border-top: 1px solid #1a1a1a; padding-top: 35px; width: 100%; }
        .video-thumbnail { width: 100%; border-radius: 24px; border: 1px solid #222; margin-bottom: 25px; }

        .download-option {
            display: flex; align-items: center; justify-content: center; gap: 12px;
            padding: 18px; border-radius: 15px; font-weight: 900; text-decoration: none;
            transition: 0.2s; margin: 12px 0; font-size: 1.1rem;
        }
        .video-hd { background: var(--primary-color); color: #000; }
        .audio-mp3 { background: #fff; color: #000; }

        .footer-credits { margin-top: auto; padding: 50px 20px; text-align: center; color: #333; }
        .social-icon { font-size: 1.4rem; color: #444; margin: 0 10px; transition: 0.3s; }
        .social-icon:hover { color: var(--primary-color); }
    </style>
</head>
<body>

    <div class="main-container">
        <div class="header-section">
            <div class="flex justify-center mb-6">
                <i class="fa-brands fa-tiktok text-4xl" style="color: var(--accent-color);"></i>
            </div>
            <h1>Wizzy Sovereign</h1>
            <p>تحميل الفيديوهات من تيك توك بجودة عالية وبدون علامة مائية</p>
        </div>

        <input type="text" id="videoUrl" placeholder="الصق رابط الفيديو هنا">
        <button onclick="handleDownload()" class="btn-download">
            <i class="fa-solid fa-circle-down ml-2"></i> بدء التحميل
        </button>

        <div id="result-area">
            <img id="videoPreview" class="video-thumbnail" src="">
            <div id="videoTitle" class="text-md text-gray-500 mb-6 px-6 font-bold"></div>
            
            <div class="px-6">
                <a id="hdDownload" class="download-option video-hd" href="#">
                    <i class="fa-solid fa-file-video"></i> تحميل الفيديو (MP4 HD)
                </a>
                <a id="mp3Download" class="download-option audio-mp3" href="#">
                    <i class="fa-solid fa-music"></i> تحميل الصوت (MP3)
                </a>
            </div>
        </div>
    </div>

    <div class="footer-credits">
        <div class="flex justify-center mb-6">
            <a href="#" class="social-icon"><i class="fa-brands fa-instagram"></i></a>
            <a href="#" class="social-icon"><i class="fa-brands fa-telegram"></i></a>
            <a href="#" class="social-icon"><i class="fa-brands fa-github"></i></a>
        </div>
        <p class="text-xs uppercase tracking-widest mb-2">Designed by Wizzy Sovereign</p>
        <p class="text-[10px] font-bold">جميع الحقوق محفوظة © 2026</p>
    </div>

    <script>
        async function handleDownload() {
            const url = document.getElementById('videoUrl').value;
            if(!url) return Swal.fire({ icon: 'info', title: 'تنبيه', text: 'يرجى إدخال الرابط أولاً', background: '#0a0a0a', color: '#fff' });

            Swal.fire({ 
                title: 'جاري المعالجة', 
                text: 'يرجى الانتظار ثواني...',
                allowOutsideClick: false, 
                didOpen: () => Swal.showLoading(), 
                background: '#0a0a0a', 
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
                    
                    document.getElementById('hdDownload').href = `/proxy_file?url=${encodeURIComponent(data.hdplay || data.play)}&filename=Wizzy_Sovereign.mp4`;
                    document.getElementById('mp3Download').href = `/proxy_file?url=${encodeURIComponent(data.music)}&filename=Wizzy_Audio.mp3`;
                    
                    Swal.close();
                    window.scrollTo({ top: document.getElementById('result-area').offsetTop - 20, behavior: 'smooth' });
                } else {
                    Swal.fire({ icon: 'error', title: 'خطأ', text: 'الرابط غير صالح أو الفيديو محمي', background: '#0a0a0a', color: '#fff' });
                }
            } catch(e) {
                Swal.fire({ icon: 'error', title: 'خطأ فني', text: 'حدث خطأ في الخادم', background: '#0a0a0a', color: '#fff' });
            }
        }
    </script>
</body>
</html>
