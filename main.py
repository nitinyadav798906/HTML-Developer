import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

# Config
API_ID = "12475131"
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "7889074753:AAH66Cltd_20v9YtxOT8ounMEkNyQIv3NxE"
CHANNEL_USERNAME = "Sachin yadav Nitin yadav" 

app = Client("ultra_aesthetic_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def extract_names_and_urls(file_content):
    lines = file_content.strip().split("\n")
    data = []
    for line in lines:
        if ":" in line:
            parts = line.split(":", 1)
            data.append((parts[0].strip(), parts[1].strip()))
    return data

def categorize_urls(urls):
    videos, pdfs, others = [], [], []
    for name, url in urls:
        new_url = url
        low_url = url.lower()
        if "apps-s3-jw-prod.utkarshapp.com" in url:
            new_url = url.replace("apps-s3-jw-prod.utkarshapp.com", "d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/")

        if any(x in low_url for x in ["drm", "classplus", "tencent", "1681", "/cc/", "videos.classplusapp.com"]):
            videos.append((name, f"https://itsgolu-v1player.vercel.app/?url={new_url}"))
        elif any(ext in low_url for ext in [".m3u8", ".mp4", ".webm", ".mkv", ".mpd"]):
            videos.append((name, new_url))
        elif ".pdf" in low_url:
            pdfs.append((name, new_url))
        else:
            others.append((name, new_url))
    return videos, pdfs, others

def generate_html(file_name, videos, pdfs, others):
    title = os.path.splitext(file_name)[0]
    
    video_html = "".join([f'<div class="card video-card" onclick="playVideo(\'{u}\', \'{n}\')"><div class="play-icon"><i class="fas fa-play"></i></div><div class="card-info"><div class="card-title">{n}</div><div class="card-tag">Video Lecture</div></div></div>' for n, u in videos])
    pdf_html = "".join([f'<a class="card pdf-card" href="{u}" target="_blank"><div class="pdf-icon"><i class="fas fa-file-pdf"></i></div><div class="card-info"><div class="card-title">{n}</div><div class="card-tag">PDF Document</div></div></a>' for n, u in pdfs])

    return f"""
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet" />
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        
        :root {{ 
            --bg: #0a0e17; --glass: rgba(255, 255, 255, 0.05); --primary: #00f2fe; 
            --text: #ffffff; --card-bg: #161b22; --accent: #4facef;
        }}
        [data-theme="light"] {{
            --bg: #f0f2f5; --glass: rgba(0, 0, 0, 0.05); --primary: #2563eb;
            --text: #1f2937; --card-bg: #ffffff; --accent: #3b82f6;
        }}

        body {{ background: var(--bg); color: var(--text); font-family: 'Poppins', sans-serif; margin: 0; transition: all 0.4s ease; overflow-x: hidden; }}
        
        .navbar {{ 
            background: var(--glass); backdrop-filter: blur(10px); padding: 20px; 
            text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1); sticky; top: 0; z-index: 1000;
        }}

        #clock {{ font-size: 14px; color: var(--primary); letter-spacing: 2px; font-weight: 600; }}
        .header-title {{ margin: 10px 0; font-size: 24px; font-weight: 600; background: linear-gradient(to right, var(--primary), var(--accent)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}

        .theme-switch {{ position: absolute; right: 25px; top: 35px; cursor: pointer; font-size: 22px; color: var(--primary); }}

        .video-wrapper {{ width: 95%; max-width: 900px; margin: 30px auto; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); }}

        .tab-container {{ display: flex; justify-content: center; gap: 15px; margin-bottom: 30px; }}
        .tab-btn {{ 
            padding: 12px 30px; background: var(--card-bg); border-radius: 50px; cursor: pointer; 
            font-weight: 600; transition: 0.3s; border: 1px solid rgba(255,255,255,0.1); color: var(--text);
        }}
        .tab-btn.active {{ background: var(--primary); color: #000; box-shadow: 0 0 20px var(--primary); }}

        .content-section {{ width: 90%; max-width: 850px; margin: 0 auto; display: none; animation: fadeIn 0.5s ease; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}

        .card {{ 
            background: var(--card-bg); margin-bottom: 15px; padding: 15px; border-radius: 15px; 
            display: flex; align-items: center; cursor: pointer; transition: 0.3s; 
            text-decoration: none; color: inherit; border: 1px solid rgba(255,255,255,0.05);
        }}
        .card:hover {{ transform: scale(1.02); border-color: var(--primary); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }}

        .play-icon, .pdf-icon {{ 
            width: 50px; height: 50px; border-radius: 12px; display: flex; 
            align-items: center; justify-content: center; margin-right: 20px; font-size: 20px;
        }}
        .play-icon {{ background: rgba(0, 242, 254, 0.1); color: var(--primary); }}
        .pdf-icon {{ background: rgba(239, 68, 68, 0.1); color: #ef4444; }}

        .card-info {{ display: flex; flex-direction: column; }}
        .card-title {{ font-weight: 600; font-size: 16px; margin-bottom: 4px; }}
        .card-tag {{ font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px; }}

        .footer {{ text-align: center; padding: 40px; color: #666; font-size: 13px; }}

        /* VideoJS Customization */
        .video-js {{ border-radius: 20px; }}
        .vjs-big-play-centered .vjs-big-play-button {{ background-color: var(--primary) !important; border-radius: 50% !important; width: 2em !important; height: 2em !important; line-height: 2em !important; margin-top: -1em !important; margin-left: -1em !important; }}
    </style>
</head>
<body>
    <div class="navbar">
        <div id="clock">00:00:00 AM</div>
        <div class="header-title">{title}</div>
        <div class="theme-switch" onclick="toggleTheme()"><i class="fas fa-moon"></i></div>
    </div>

    <div class="video-wrapper">
        <video id="main-player" class="video-js vjs-fluid vjs-big-play-centered" controls preload="auto"></video>
    </div>

    <div class="tab-container">
        <div class="tab-btn active" onclick="switchTab('videos', this)">Videos</div>
        <div class="tab-btn" onclick="switchTab('pdfs', this)">PDFs</div>
    </div>

    <div id="videos" class="content-section" style="display:block;">{video_html}</div>
    <div id="pdfs" class="content-section">{pdf_html}</div>

    <div class="footer">
        Designed with Style by Sachin Yadav & Nitin Yadav<br>© 2026 High Speed Player
    </div>

    <script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
    <script>
        // Clock
        function tick() {{
            document.getElementById('clock').innerText = new Date().toLocaleTimeString();
        }}
        setInterval(tick, 1000);

        // Theme Toggle
        function toggleTheme() {{
            const root = document.documentElement;
            const icon = document.querySelector('.theme-switch i');
            if(root.getAttribute('data-theme') === 'dark') {{
                root.setAttribute('data-theme', 'light');
                icon.className = 'fas fa-sun';
            }} else {{
                root.setAttribute('data-theme', 'dark');
                icon.className = 'fas fa-moon';
            }}
        }}

        // Player
        const player = videojs('main-player', {{
            playbackRates: [0.5, 1, 1.25, 1.5, 2, 2.5, 3]
        }});

        function playVideo(url, name) {{
            if (url.includes('vercel.app')) {{ window.open(url, '_blank'); return; }}
            let type = url.includes('.m3u8') ? 'application/x-mpegURL' : (url.includes('.webm') ? 'video/webm' : 'video/mp4');
            player.src({{ src: url, type: type }});
            player.play();
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function switchTab(id, btn) {{
            document.querySelectorAll('.content-section').forEach(s => s.style.display = 'none');
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(id).style.display = 'block';
            btn.classList.add('active');
        }}
    </script>
</body>
</html>
    """

@app.on_message(filters.command("start"))
async def start(c, m):
    await m.reply_text("✨ **Ultra Aesthetic Bot Ready**\n\nSend me your `.txt` file and I'll create a premium dashboard for you.")

@app.on_message(filters.document)
async def handle(c, m):
    if not m.document.file_name.endswith(".txt"): return
    status = await m.reply_text("🪄 **Creating Magic...**")
    path = await m.download()
    
    with open(path, "r", encoding="utf-8") as f: content = f.read()
    v, p, o = categorize_urls(extract_names_and_urls(content))
    html_code = generate_html(m.document.file_name, v, p, o)
    
    h_path = path.replace(".txt", ".html")
    with open(h_path, "w", encoding="utf-8") as f: f.write(html_code)

    await m.reply_document(h_path, caption=f"💎 **Premium Dashboard Generated**\n\n🎬 Videos: {len(v)}\n📄 PDFs: {len(p)}\n\nEnjoy the smooth experience!")
    await status.delete()
    os.remove(path); os.remove(h_path)

if __name__ == "__main__":
    app.run()
