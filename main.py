import os
from datetime import datetime
from pyrogram import Client, filters

# ================= CONFIG =================
BOT_OWNER_NAME = "Sachin Yadav & Nitin Yadav"
API_ID = 12475131
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"
TELEGRAM_LINK = "https://t.me/Raftaarss_don"

OLD_DOMAINS = [
    "https://apps-s3-jw-prod.utkarshapp.com/",
    "https://apps-s3-prod.utkarshapp.com/",
    "https://apps-s3-video-dist.utkarshapp.com/"
]
NEW_DOMAIN = "https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/"

app = Client("pro_brand_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ================= VIDEO DOMAIN REPLACER =================
def replace_video_domains(url: str):
    low = url.lower()
    # Sirf video extensions ke liye domain badlega
    if any(x in low for x in [".mp4", ".m3u8", ".mpd", "/m3u8"]):
        for d in OLD_DOMAINS:
            if d in url:
                url = url.replace(d, NEW_DOMAIN)
    return url

# ================= HTML GENERATOR =================
def generate_html(file_name, content):
    title = os.path.splitext(file_name)[0]
    now_full = datetime.now().strftime("%d %b %Y, %I:%M %p")
    lines = content.strip().split("\n")

    v_total, p_total, a_total, o_total = 0, 0, 0, 0
    folder_data = []
    current_folder = {"name": "Main Content", "items": []}

    for line in lines:
        line = line.strip()
        if not line: continue
        
        if "http" in line:
            if ":" in line:
                name, url = line.split(":", 1)
            else:
                name, url = "Link", line
            
            name, url = name.strip(), url.strip()
            low = url.lower()
            
            # Determine Type & Apply Domain Change ONLY for Videos
            if any(x in low for x in [".mp4", ".m3u8", ".mpd", "/m3u8"]): 
                item_type = "video"; v_total += 1
                url = replace_video_domains(url)
            elif ".pdf" in low: 
                item_type = "pdf"; p_total += 1
            elif any(x in low for x in [".mp3", ".m4a"]): 
                item_type = "audio"; a_total += 1
            else: 
                item_type = "other"; o_total += 1
                
            current_folder["items"].append({"name": name, "url": url, "type": item_type})
        else:
            if current_folder["items"]:
                folder_data.append(current_folder)
            current_folder = {"name": line, "items": []}
    
    if current_folder["items"]: folder_data.append(current_folder)

    html_content = ""
    for idx, folder in enumerate(folder_data):
        html_content += f'''
        <div class="folder-wrapper">
            <div class="chapter-header" onclick="toggleFolder('f-{idx}')">
                📁 {folder['name']} <span style="font-size:10px; float:right;">Tap to Expand ▼</span>
            </div>
            <div id="f-{idx}" class="folder-content" style="display:none;">
                <div class="filter-tabs">
                    <button class="t-btn" onclick="filterType('f-{idx}', 'video')">Videos</button>
                    <button class="t-btn" onclick="filterType('f-{idx}', 'pdf')">PDFs</button>
                    <button class="t-btn" onclick="filterType('f-{idx}', 'audio')">Audio</button>
                    <button class="t-btn" onclick="filterType('f-{idx}', 'other')">Others</button>
                </div>'''
        for item in folder['items']:
            if item['type'] == "video":
                func = f"playVideo('{item['url']}', '{item['name']}')"
            else:
                func = f"window.open('{item['url']}', '_blank')"
            
            icon = "🎬" if item['type']=="video" else "📄" if item['type']=="pdf" else "🎵" if item['type']=="audio" else "🔗"
            html_content += f'''
            <div class="list-item" data-type="{item['type']}" onclick="{func}">
                {icon} {item['name']}
            </div>'''
        html_content += "</div></div>"

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet">
    <style>
        :root {{ --bg: #fff; --text: #000; --item: #f4f4f4; --card: #000; }}
        .dark-mode {{ --bg: #0f0f0f; --text: #fff; --item: #1a1a1a; --card: #1a1a1a; }}
        body {{ font-family: sans-serif; background: var(--bg); color: var(--text); margin: 0; text-align: center; transition: 0.3s; }}
        .welcome-screen {{ padding: 40px 10px; min-height: 80vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        .welcome-title {{ color: green; font-size: 40px; font-weight: bold; }}
        .info-box {{ background: var(--card); color: #fff; padding: 20px; border-radius: 15px; width: 85%; margin: 20px auto; border: 1px solid #333; }}
        .btn {{ padding: 12px 20px; border-radius: 8px; border: none; color: #fff; font-weight: bold; width: 220px; margin: 8px; cursor: pointer; }}
        .content-screen {{ display:none; }}
        .player-box {{ position: sticky; top: 0; z-index: 100; background: #000; display: none; width: 100%; }}
        .search-bar {{ width: 85%; padding: 12px; border: 2px solid #007bff; border-radius: 25px; margin: 15px 0; outline: none; }}
        .chapter-header {{ background: #e0e0e0; color: #000; padding: 15px; text-align: left; font-weight: bold; margin: 8px 10px; border-radius: 8px; cursor: pointer; }}
        .dark-mode .chapter-header {{ background: #333; color: #fff; }}
        .list-item {{ background: var(--item); padding: 12px; border-radius: 8px; margin: 5px 10px; text-align: left; cursor: pointer; border: 1px solid #ddd; font-size: 13px; font-weight: 500; }}
        .filter-tabs {{ display:flex; justify-content:center; gap:5px; margin: 10px 0; flex-wrap: wrap; }}
        .t-btn {{ background: #00bcd4; color: #fff; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; }}
    </style>
</head>
<body>
    <div id="welcome" class="welcome-screen">
        <div class="welcome-title">Welcome</div>
        <div class="info-box">
            <h3>{title}</h3>
            <p style="color:yellow; font-weight:bold;">Created By: {BOT_OWNER_NAME}</p>
            <p style="font-size:12px;">{now_full}</p>
        </div>
        <button class="btn" style="background:red;" onclick="showContent()">Open Your Batch</button><br>
        <button class="btn" style="background:#007bff;" onclick="toggleDark()">Switch to Dark Mode</button>
    </div>

    <div id="content-area" class="content-screen">
        <div id="p-box" class="player-box">
            <video id="vid" class="video-js vjs-fluid vjs-default-skin" controls preload="auto"></video>
            <div id="v-title" style="color:#fff; padding:8px; font-size:12px; background:#222; text-align:left;"></div>
        </div>
        <div style="background:#000; color:yellow; padding:10px; font-size:12px;">📅 {now_full}</div>
        <button class="btn" style="background:#007bff; width:auto; padding:8px 20px; margin-top:15px;" onclick="toggleDark()">Switch Dark Mode</button>
        <div style="color:#007bff; font-weight:bold; margin:10px; font-size:14px;">🎥 {v_total} | 📄 {p_total} | 🎵 {a_total}</div>
        <input type="text" id="srch" class="search-bar" placeholder="Search lessons..." onkeyup="search()">
        {html_content}
        <a href="{TELEGRAM_LINK}" style="color:red; display:block; padding:30px; font-weight:bold; text-decoration:none;">JOIN TELEGRAM</a>
    </div>

    <script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
    <script>
        const player = videojs('vid');
        function showContent() {{ document.getElementById('welcome').style.display='none'; document.getElementById('content-area').style.display='block'; window.scrollTo(0,0); }}
        function toggleDark() {{ document.body.classList.toggle('dark-mode'); }}
        function toggleFolder(id) {{ let e=document.getElementById(id); e.style.display=e.style.display==='none'?'block':'none'; }}
        function playVideo(url, name) {{
            document.getElementById('p-box').style.display='block';
            document.getElementById('v-title').innerText = "Now Playing: " + name;
            player.src({{ src: url, type: url.includes('m3u8') ? 'application/x-mpegURL' : (url.includes('mpd') ? 'application/dash+xml' : 'video/mp4') }});
            player.play(); window.scrollTo(0,0);
        }}
        function filterType(fId, type) {{
            let items = document.querySelectorAll('#'+fId+' .list-item');
            items.forEach(i => i.style.display = (i.getAttribute('data-type')===type) ? 'block' : 'none');
        }}
        function search() {{
            let f = document.getElementById('srch').value.toLowerCase();
            document.querySelectorAll('.list-item').forEach(i => i.style.display = i.innerText.toLowerCase().includes(f) ? 'block' : 'none');
        }}
    </script>
</body>
</html>
"""

@app.on_message(filters.command("start"))
async def start(c, m):
    await m.reply_text("🚀 **Bot Upgraded!**\n- PDF domain change disabled\n- Only Video domains will change\n- Filters updated (No 'All' button)\n\nBhejo TXT file.")

@app.on_message(filters.document)
async def handle(c, m):
    if not m.document.file_name.endswith(".txt"): return
    path = await m.download()
    with open(path, "r", encoding="utf-8") as f:
        html = generate_html(m.document.file_name, f.read())
    h = path.replace(".txt", ".html")
    with open(h, "w", encoding="utf-8") as f: f.write(html)
    await m.reply_document(h, caption=f"👑 **Batch HTML Ready**\nOwner: {BOT_OWNER_NAME}")
    os.remove(path); os.remove(h)

app.run()
