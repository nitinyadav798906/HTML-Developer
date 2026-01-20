import os
from pyrogram import Client, filters

# Config
BOT_OWNER_NAME = "Sachin Yadav & Nitin Yadav"
API_ID = "12475131"
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"

app = Client("classplus_fix_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

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
        low_url = url.lower()
        # Classplus & DRM Fix Logic
        if any(x in low_url for x in ["classplus", "drm", "tencent", "1681", "p-v.top"]):
            # Inhe special external player par bhej rahe hain
            special_url = f"https://itsgolu-v1player.vercel.app/?url={url}"
            videos.append((name, special_url))
        elif any(ext in low_url for ext in [".m3u8", ".mp4", ".webm", ".mkv", ".m4a", ".aac"]):
            videos.append((name, url))
        elif ".pdf" in low_url:
            pdfs.append((name, url))
        else:
            others.append((name, url))
    return videos, pdfs, others

def generate_html(file_name, videos, pdfs, others):
    title = os.path.splitext(file_name)[0]
    
    video_list = "".join([f'<div class="folder-item" onclick="playMedia(\'{u}\', \'{n}\')"><i class="fas fa-play-circle"></i> <span>{n}</span></div>' for n, u in videos])
    pdf_list = "".join([f'<a class="folder-item" href="{u}" target="_blank"><i class="fas fa-file-pdf"></i> <span>{n}</span></a>' for n, u in pdfs])

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet" />
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600&display=swap');
        body {{ background: #0a0c10; color: white; font-family: 'Outfit', sans-serif; margin: 0; text-align: center; }}
        .navbar {{ background: #161b22; padding: 20px; border-bottom: 3px solid #00e5ff; }}
        .owner {{ color: #00e5ff; font-weight: 600; font-size: 14px; }}
        .player-box {{ width: 95%; max-width: 800px; margin: 20px auto; border-radius: 12px; overflow: hidden; display: none; border: 1px solid #30363d; }}
        .folder-item {{ background: #f0f6ff; color: #1c2128; padding: 15px; margin: 10px auto; width: 90%; max-width: 750px; border-radius: 12px; display: flex; align-items: center; cursor: pointer; font-weight: 600; text-decoration: none; border-left: 6px solid #00e5ff; }}
        .folder-item i {{ margin-right: 15px; color: #00e5ff; font-size: 20px; }}
        .search-bar {{ width: 85%; padding: 12px; margin: 20px 0; border-radius: 25px; border: none; background: #161b22; color: white; border: 1px solid #30363d; }}
    </style>
</head>
<body>
    <div class="navbar">
        <div class="owner">Created By : {BOT_OWNER_NAME}</div>
        <h2>{title}</h2>
    </div>

    <div class="player-box" id="pBox">
        <video id="v-player" class="video-js vjs-fluid vjs-big-play-centered" controls preload="auto"></video>
    </div>

    <input type="text" class="search-bar" placeholder="🔍 Search Lessons..." onkeyup="search()">

    <div id="videos">{video_list}</div>
    <div id="pdfs">{pdf_list}</div>

    <script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
    <script>
        const player = videojs('v-player');

        function playMedia(url, name) {{
            // Utkarsh Fix
            if (url.includes("apps-s3-jw-prod.utkarshapp.com")) {{
                url = url.replace("apps-s3-jw-prod.utkarshapp.com", "d1q5ugnejk3zoi.cloudfront.net/ut-production-jw");
            }}

            // Classplus/External Player Fix
            if (url.includes("vercel.app") || url.includes("v1player")) {{
                window.open(url, '_blank');
                return;
            }}

            document.getElementById('pBox').style.display = 'block';
            let type = url.includes('.m3u8') ? 'application/x-mpegURL' : (url.includes('.m4a') ? 'audio/mp4' : 'video/mp4');
            player.src({{ src: url, type: type }});
            player.play();
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function search() {{
            let q = document.querySelector('.search-bar').value.toLowerCase();
            document.querySelectorAll('.folder-item').forEach(item => {{
                item.style.display = item.innerText.toLowerCase().includes(q) ? 'flex' : 'none';
            }});
        }}
    </script>
</body>
</html>
    """

@app.on_message(filters.command("start"))
async def start(c, m):
    await m.reply_text(f"🚀 **{BOT_OWNER_NAME}'s Pro Bot Active!**\nSend me your .txt file. (ek dum chup🖕)")

@app.on_message(filters.document)
async def handle(c, m):
    if not m.document.file_name.endswith(".txt"): return
    msg = await m.reply_text("⚡ Processing...")
    path = await m.download()
    with open(path, "r", encoding="utf-8") as f: content = f.read()
    v, p, o = categorize_urls(extract_names_and_urls(content))
    html = generate_html(m.document.file_name, v, p, o)
    h_path = path.replace(".txt", ".html")
    with open(h_path, "w", encoding="utf-8") as f: f.write(html)
    await m.reply_document(h_path, caption=f"✅ **Fixed Dashboard Ready!**\nBy: {BOT_OWNER_NAME}")
    os.remove(path); os.remove(h_path)

app.run()
