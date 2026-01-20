import os
from pyrogram import Client, filters

# Config
BOT_OWNER_NAME = "Sachin & Nitin Yadav"
API_ID = "12475131"
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"

app = Client("ultra_pro_max_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

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
        if any(ext in low_url for ext in [".m3u8", ".mp4", ".webm", ".mkv", ".mpd", "v1player", "hlscast"]):
            videos.append((name, url))
        elif ".pdf" in low_url:
            pdfs.append((name, url))
        else:
            others.append((name, url))
    return videos, pdfs, others

def generate_html(file_name, videos, pdfs, others):
    title = os.path.splitext(file_name)[0]
    
    video_list = "".join([f'<div class="folder-item" onclick="playVideo(\'{u}\', \'{n}\')"><i class="fas fa-play-circle"></i> <span>{n}</span></div>' for n, u in videos])
    pdf_list = "".join([f'<a class="folder-item" href="{u}" target="_blank"><i class="fas fa-file-pdf"></i> <span>{n}</span></a>' for n, u in pdfs])
    other_list = "".join([f'<a class="folder-item" href="{u}" target="_blank"><i class="fas fa-link"></i> <span>{n}</span></a>' for n, u in others])

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
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        :root {{ --bg: #121212; --text: #ffffff; --primary: #00bcd4; --accent: #ff9800; --card: #1e1e1e; }}
        [data-theme="light"] {{ --bg: #f5f5f5; --text: #000000; --primary: #00796b; --card: #ffffff; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Roboto', sans-serif; margin: 0; text-align: center; }}
        .header {{ padding: 20px; }}
        .created-by {{ color: var(--accent); font-weight: bold; }}
        .theme-btn {{ background: var(--accent); border: none; padding: 10px 20px; border-radius: 8px; color: #000; font-weight: bold; cursor: pointer; margin: 15px 0; }}
        .stats {{ color: var(--primary); font-weight: bold; margin: 10px 0; }}
        .tab-bar {{ display: flex; justify-content: center; gap: 8px; margin: 15px 0; flex-wrap: wrap; }}
        .tab {{ background: var(--primary); border: none; padding: 10px 18px; border-radius: 12px; color: white; font-weight: bold; cursor: pointer; }}
        .search-container {{ width: 90%; margin: 10px auto; }}
        .search-container input {{ width: 100%; padding: 12px; border-radius: 25px; border: 1px solid #444; background: var(--card); color: var(--text); outline: none; }}
        .player-section {{ width: 95%; max-width: 800px; margin: 0 auto 20px auto; border-radius: 12px; overflow: hidden; display: none; }}
        .list-container {{ width: 95%; max-width: 850px; margin: 0 auto; display: none; }}
        .folder-item {{ background: #ccc; color: #000; padding: 12px; margin-bottom: 8px; border-radius: 8px; display: flex; align-items: center; text-decoration: none; font-weight: bold; cursor: pointer; text-align: left; }}
        .folder-item i {{ margin-right: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <div class="created-by">Created By : {BOT_OWNER_NAME}</div>
    </div>

    <button class="theme-btn" onclick="toggleTheme()">Switch to Light Mode</button>

    <div class="stats">
        Videos : {len(videos)} | PDFs : {len(pdfs)} | Others : {len(others)}
    </div>

    <div class="tab-bar">
        <button class="tab" onclick="showTab('videos')">Videos</button>
        <button class="tab" onclick="showTab('pdfs')">PDFs</button>
        <button class="tab" onclick="showTab('others')">Others</button>
    </div>

    <div class="player-section" id="playerBox">
        <video id="vjs-player" class="video-js vjs-fluid vjs-big-play-centered" controls preload="auto"></video>
    </div>

    <div id="videos" class="list-container" style="display:block;">{video_list}</div>
    <div id="pdfs" class="list-container">{pdf_list}</div>
    <div id="others" class="list-container">{other_list}</div>

    <script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
    <script>
        const player = videojs('vjs-player');

        function playVideo(url, name) {{
            // Automatic Utkarsh URL Change Logic
            let finalUrl = url;
            if (url.includes("apps-s3-jw-prod.utkarshapp.com")) {{
                finalUrl = url.replace("apps-s3-jw-prod.utkarshapp.com", "d1q5ugnejk3zoi.cloudfront.net/ut-production-jw");
            }}

            document.getElementById('playerBox').style.display = 'block';
            let type = finalUrl.includes('.m3u8') ? 'application/x-mpegURL' : 'video/mp4';
            player.src({{ src: finalUrl, type: type }});
            player.play();
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function showTab(id) {{
            document.querySelectorAll('.list-container').forEach(c => c.style.display = 'none');
            document.getElementById(id).style.display = 'block';
        }}

        function toggleTheme() {{
            const root = document.documentElement;
            root.setAttribute('data-theme', root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
        }}
    </script>
</body>
</html>
    """

@app.on_message(filters.document)
async def handle(c, m):
    if not m.document.file_name.endswith(".txt"): return
    path = await m.download()
    with open(path, "r", encoding="utf-8") as f: content = f.read()
    v, p, o = categorize_urls(extract_names_and_urls(content))
    html_code = generate_html(m.document.file_name, v, p, o)
    h_path = path.replace(".txt", ".html")
    with open(h_path, "w", encoding="utf-8") as f: f.write(html_code)
    await m.reply_document(h_path, caption=f"✅ **Utkarsh Auto-Fix Enabled!**\nBy: {BOT_OWNER_NAME}")
    os.remove(path); os.remove(h_path)

app.run()
