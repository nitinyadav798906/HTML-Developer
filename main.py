import os
import re
from datetime import datetime
from pyrogram import Client, filters

# ================= CONFIG =================
BOT_OWNER_NAME = "Sachin Yadav & Nitin Yadav"
API_ID = 12475131
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"
TELEGRAM_LINK = "https://t.me/Raftaarss_don"

OLD_DOMAINS = ["https://apps-s3-jw-prod.utkarshapp.com/", "https://apps-s3-prod.utkarshapp.com/", "https://apps-s3-video-dist.utkarshapp.com/"]
NEW_DOMAIN = "https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/"

app = Client("pro_brand_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_mode = {} 

def replace_video_domains(url: str):
    low = url.lower()
    if any(x in low for x in [".mp4", ".m3u8", ".mpd", "/m3u8"]):
        for d in OLD_DOMAINS:
            if d in url: url = url.replace(d, NEW_DOMAIN)
    return url

# ================= SMART HTML GENERATOR =================
def generate_html(file_name, content):
    title = os.path.splitext(file_name)[0]
    now_full = datetime.now().strftime("%d %b %Y, %I:%M %p")
    lines = content.strip().split("\n")
    
    v_t, p_t, o_t = 0, 0, 0
    folder_data = []
    current_folder = None

    for line in lines:
        line = line.strip()
        if not line or "http" not in line: continue
        
        name, url = line.split(":", 1) if ":" in line else ("Class", line)
        name, url = name.strip(), url.strip()
        
        # Check if name starts with 1 or 01 to create a NEW folder
        # Regex to detect "1.", "01.", "1 " etc.
        if re.match(r'^(01|1)[\s\.\-]', name) or current_folder is None:
            if current_folder: folder_data.append(current_folder)
            # Remove the '01' part to make folder name clean or keep it as you like
            folder_name = re.sub(r'^(01|1)[\s\.\-]', '', name).strip()
            current_folder = {"name": folder_name, "items": []}

        low = url.lower()
        if any(x in low for x in [".mp4", ".m3u8", ".mpd"]): 
            t = "video"; v_t += 1; url = replace_video_domains(url)
        elif ".pdf" in low: t = "pdf"; p_t += 1
        else: t = "other"; o_t += 1
        
        current_folder["items"].append({"name": name, "url": url, "type": t})
            
    if current_folder: folder_data.append(current_folder)

    html_folders = ""
    for idx, f in enumerate(folder_data):
        count = len(f['items'])
        html_folders += f'''
        <div class="folder-box">
            <div class="folder-head" onclick="toggle('f-{idx}')">
                📁 {f['name']} <span style="float:right; font-size:12px;">{count} Classes</span>
            </div>
            <div id="f-{idx}" class="folder-content" style="display:none;">'''
        for i in f['items']:
            icon = "🎬" if i['type']=="video" else "📄" if i['type']=="pdf" else "🔗"
            html_folders += f'<div class="item" onclick="window.open(\'{i["url"]}\')">{icon} {i["name"]}</div>'
        html_folders += "</div></div>"

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <style>
        :root {{ --bg: #f5f6fa; --text: #2f3640; --item: #ffffff; --accent: #007bff; }}
        .dark-mode {{ --bg: #1e272e; --text: #f5f6fa; --item: #2f3640; --accent: #00d2d3; }}
        body {{ font-family: sans-serif; background: var(--bg); color: var(--text); margin: 0; transition: 0.3s; }}
        .welcome {{ text-align: center; padding: 50px 20px; }}
        .card {{ background: #000; color: #fff; padding: 25px; border-radius: 15px; width: 85%; margin: 0 auto 20px; }}
        .btn {{ padding: 12px 24px; border-radius: 25px; border: none; color: #fff; font-weight: bold; width: 240px; margin: 8px; cursor: pointer; }}
        .sticky-header {{ position: sticky; top: 0; z-index: 100; background: var(--item); padding: 12px; border-bottom: 2px solid var(--accent); }}
        .search-bar {{ width: 90%; padding: 12px; border: 1px solid #ccc; border-radius: 10px; margin: 10px auto; display: block; }}
        .folder-head {{ background: var(--item); padding: 15px; border-radius: 10px; font-weight: bold; cursor: pointer; margin: 10px; border: 1px solid #ddd; }}
        .item {{ background: var(--item); padding: 12px; border-radius: 8px; margin: 8px 15px; cursor: pointer; font-size: 13px; border-left: 5px solid var(--accent); }}
    </style>
</head>
<body>
    <div id="welcome" class="welcome">
        <h1 style="color:#44bd32;">Welcome</h1>
        <div class="card">
            <h2>{title}</h2>
            <p style="color:yellow;">👑 Owner: {BOT_OWNER_NAME}</p>
        </div>
        <button class="btn" style="background:#e84118;" onclick="start()">Open Your Batch</button><br>
        <button class="btn" style="background:#0097e6;" onclick="dark()">Switch Dark Mode</button>
    </div>

    <div id="main" style="display:none;">
        <div class="sticky-header">
            <div style="display:flex; justify-content:space-between; align-items:center; padding:0 10px;">
                <b style="color:var(--accent);">Study Materials</b>
                <span onclick="openSet()" style="cursor:pointer; font-size:20px;">⚙️</span>
            </div>
            <input type="text" id="q" class="search-bar" placeholder="Search classes..." onkeyup="src()">
        </div>
        
        <div style="text-align:center; padding: 15px; font-weight:bold; color:var(--accent);">
            🎥 {v_t} Videos | 📄 {p_t} PDFs
        </div>

        {html_folders}
        <div style="text-align:center; padding: 20px; opacity:0.5; font-size:12px;">Created by {BOT_OWNER_NAME}</div>
    </div>

    <script>
        function start() {{ document.getElementById('welcome').style.display='none'; document.getElementById('main').style.display='block'; }}
        function dark() {{ document.body.classList.toggle('dark-mode'); }}
        function toggle(id) {{ let e=document.getElementById(id); e.style.display=e.style.display==='none'?'block':'none'; }}
        function src() {{ 
            let v=document.getElementById('q').value.toLowerCase(); 
            document.querySelectorAll('.item').forEach(i => i.style.display = i.innerText.toLowerCase().includes(v)?'block':'none');
        }}
    </script>
</body>
</html>
"""

# [Command handlers and standard processing code remains same]
app.run()
