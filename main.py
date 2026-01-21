import os
from datetime import datetime
from pyrogram import Client, filters

# --- Config ---
BOT_OWNER_NAME = "Sachin Yadav & Nitin Yadav"
API_ID = "12475131"
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"
TELEGRAM_LINK = "https://t.me/Raftaarss_don" # Apna link yaha dale

app = Client("pro_brand_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def generate_html(file_name, content):
    title = os.path.splitext(file_name)[0]
    now = datetime.now().strftime("%d %b %Y")
    lines = content.strip().split("\n")
    
    html_sections = ""
    temp_content = ""
    current_folder = "Main Lessons"
    v_count, p_count = 0, 0

    for line in lines:
        if ":" in line and ("http" in line or "https" in line):
            name, url = line.split(":", 1)
            name, url = name.strip(), url.strip()
            
            # Utkarsh Fix
            if "apps-s3-jw-prod.utkarshapp.com" in url:
                url = url.replace("apps-s3-jw-prod.utkarshapp.com", "d1q5ugnejk3zoi.cloudfront.net/ut-production-jw")

            low_url = url.lower()
            if ".pdf" in low_url:
                p_count += 1
                temp_content += f'<a class="item-link pdf" href="{url}" target="_blank" onclick="mark(this)"><i class="fas fa-file-pdf"></i> {name}</a>'
            else:
                v_count += 1
                temp_content += f'<div class="item-link video" onclick="playMedia(\'{url}\', \'{name}\', this)"><i class="fas fa-play-circle"></i> {name}</div>'
        elif line.strip():
            if temp_content:
                html_sections += f'<div class="folder" onclick="toggleF(this)"><i class="fas fa-folder"></i> {current_folder}</div><div class="f-content">{temp_content}</div>'
            current_folder = line.strip()
            temp_content = ""

    if temp_content:
        html_sections += f'<div class="folder" onclick="toggleF(this)"><i class="fas fa-folder"></i> {current_folder}</div><div class="f-content">{temp_content}</div>'

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet" />
    <link href="https://unpkg.com/@videojs/themes@1.0.1/dist/youtube/index.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        body {{ background: #0f0f0f; color: #fff; font-family: 'Roboto', sans-serif; margin: 0; padding-bottom: 50px; text-align: center; }}
        .header {{ background: #1a1a1a; padding: 20px; border-bottom: 3px solid #ff0000; }}
        .owner {{ color: #ff0000; font-weight: bold; font-size: 16px; }}
        .search-container {{ margin: 20px; }}
        .search-bar {{ width: 90%; max-width: 500px; padding: 12px 20px; border-radius: 25px; border: 1px solid #333; background: #222; color: #fff; outline: none; }}
        .player-wrap {{ width: 100%; max-width: 850px; margin: 0 auto; display: none; background: #000; position: sticky; top: 0; z-index: 999; }}
        .folder {{ background: #2a2a2a; padding: 15px; margin: 10px auto; width: 90%; max-width: 800px; border-radius: 8px; cursor: pointer; text-align: left; font-weight: bold; display: flex; align-items: center; border: 1px solid #333; }}
        .folder i {{ margin-right: 15px; color: #ff0000; }}
        .f-content {{ display: none; width: 90%; max-width: 800px; margin: 0 auto; padding: 5px 0; }}
        .item-link {{ background: #1a1a1a; color: #ddd; padding: 15px; margin: 5px 0; border-radius: 5px; display: flex; align-items: center; cursor: pointer; text-decoration: none; font-size: 14px; border-bottom: 1px solid #222; }}
        .item-link.watched {{ opacity: 0.5; border-left: 4px solid #4CAF50; }}
        .item-link i {{ margin-right: 12px; }}
        .pdf i {{ color: #ff4444; }}
        .video i {{ color: #ff0000; }}
        .footer-btn {{ background: #ff0000; color: #fff; padding: 10px 25px; text-decoration: none; border-radius: 20px; font-weight: bold; display: inline-block; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="header">
        <div class="owner">SACHIN & NITIN YADAV PRESENTS</div>
        <h2 style="margin:10px 0;">{title}</h2>
        <div style="font-size:12px; color:#888;">{now} • {v_count} Videos • {p_count} PDFs</div>
    </div>

    <div class="player-wrap" id="pBox">
        <video id="v-player" class="video-js vjs-fluid vjs-theme-youtube vjs-big-play-centered" controls preload="auto"></video>
    </div>

    <div class="search-container">
        <input type="text" class="search-bar" placeholder="🔍 Search topic..." onkeyup="search()">
    </div>

    <div id="content-list">{html_sections}</div>

    <a href="{TELEGRAM_LINK}" class="footer-btn"><i class="fab fa-telegram-plane"></i> JOIN OUR TELEGRAM</a>

    <script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
    <script>
        const player = videojs('v-player', {{ playbackRates: [0.5, 1, 1.25, 1.5, 2] }});
        
        function toggleF(el) {{
            let content = el.nextElementSibling;
            content.style.display = content.style.display === "block" ? "none" : "block";
        }}

        function mark(el) {{ el.classList.add('watched'); }}

        function playMedia(url, name, el) {{
            mark(el);
            if (url.includes("classplus") || url.includes("drm")) {{
                window.open("https://itsgolu-v1player.vercel.app/?url=" + url, '_blank');
                return;
            }}
            document.getElementById('pBox').style.display = 'block';
            let type = url.includes('.m3u8') ? 'application/x-mpegURL' : 'video/mp4';
            player.src({{ src: url, type: type }});
            player.play();
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function search() {{
            let q = document.querySelector('.search-bar').value.toLowerCase();
            document.querySelectorAll('.item-link').forEach(i => {{
                i.style.display = i.innerText.toLowerCase().includes(q) ? 'flex' : 'none';
            }});
        }}
    </script>
</body>
</html>
    """

@app.on_message(filters.command("start"))
async def start(c, m):
    await m.reply_text(f"🚀 **Ultra-Branded Bot Active!**\nOwner: {BOT_OWNER_NAME}\n\nAb aapko Watched History, Search, aur Premium YouTube player sab milega. File bhejiye!")

@app.on_message(filters.document)
async def handle(c, m):
    if not m.document.file_name.endswith(".txt"): return
    msg = await m.reply_text("💎 **Applying Professional Branding...**")
    path = await m.download()
    with open(path, "r", encoding="utf-8") as f: content = f.read()
    html = generate_html(m.document.file_name, content)
    h_path = path.replace(".txt", ".html")
    with open(h_path, "w", encoding="utf-8") as f: f.write(html)
    await m.reply_document(h_path, caption=f"👑 **Your Brand Dashboard is Ready!**\nBy: {BOT_OWNER_NAME}")
    os.remove(path); os.remove(h_path); await msg.delete()

app.run()
