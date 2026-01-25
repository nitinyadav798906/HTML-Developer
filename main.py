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
user_mode = {}

# ================= DOMAIN REPLACER =================
def replace_video_domains(url: str):
    low = url.lower()
    if any(x in low for x in [".mp4", ".m3u8", ".mpd", "/m3u8"]):
        for d in OLD_DOMAINS:
            if d in url:
                url = url.replace(d, NEW_DOMAIN)
    return url

# ================= HTML GENERATOR =================
def generate_html(file_name, content):
    title = os.path.splitext(file_name)[0]
    now_full = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
    lines = content.strip().split("\n")

    v_t, p_t, o_t = 0, 0, 0
    folder_data = []
    current_folder = {"name": "Main Batch", "items": []}

    for line in lines:
        line = line.strip()
        if not line: continue
        if "http" in line:
            name, url = line.split(":", 1) if ":" in line else ("Link", line)
            name, url = name.strip(), url.strip()
            low = url.lower()
            if any(x in low for x in [".mp4", ".m3u8", ".mpd"]): 
                t = "video"; v_t += 1; url = replace_video_domains(url)
            elif ".pdf" in low: t = "pdf"; p_t += 1
            else: t = "other"; o_t += 1
            current_folder["items"].append({"name": name, "url": url, "type": t})
        else:
            if current_folder["items"]: folder_data.append(current_folder)
            current_folder = {"name": line, "items": []}
    if current_folder["items"]: folder_data.append(current_folder)

    html_folders = ""
    for idx, f in enumerate(folder_data):
        html_folders += f'''
        <div class="folder-box">
            <div class="folder-head" onclick="toggle('f-{idx}')">📂 {f['name']} ({len(f['items'])})</div>
            <div id="f-{idx}" class="folder-content" style="display:none;">'''
        for i in f['items']:
            func = f"playV('{i['url']}','{i['name']}')" if i['type']=="video" else f"window.open('{i['url']}')"
            icon = "🎬" if i['type']=="video" else "📄" if i['type']=="pdf" else "🔗"
            html_folders += f'<div class="item" data-type="{i["type"]}" onclick="{func}">{icon} {i["name"]}</div>'
        html_folders += "</div></div>"

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet">
    <style>
        :root {{ --bg: #fff; --text: #000; --item: #eee; --card: #000; }}
        .dark-mode {{ --bg: #121212; --text: #fff; --item: #222; --card: #1a1a1a; }}
        body {{ font-family: sans-serif; background: var(--bg); color: var(--text); margin: 0; transition: 0.3s; }}
        .welcome {{ text-align: center; padding: 40px 10px; }}
        .info-box {{ background: var(--card); color: #fff; padding: 25px; border-radius: 15px; width: 85%; margin: 20px auto; }}
        .btn {{ padding: 12px 25px; border-radius: 8px; border: none; color: #fff; font-weight: bold; width: 230px; margin: 10px; cursor: pointer; }}
        .top-bar {{ background: #1a1a1a; color: yellow; padding: 10px; text-align: center; font-size: 12px; }}
        .filters {{ display:flex; justify-content:center; gap:8px; margin: 15px 0; flex-wrap: wrap; }}
        .f-btn {{ background: #00bcd4; color: #fff; border: none; padding: 10px 18px; border-radius: 20px; cursor: pointer; font-weight: bold; }}
        .search-bar {{ width: 85%; padding: 12px; border: 2px solid #007bff; border-radius: 25px; margin: 10px auto; display: block; outline: none; }}
        .folder-head {{ background: #ccc; color: #000; padding: 15px; text-align: left; font-weight: bold; margin: 10px; border-radius: 10px; cursor: pointer; }}
        .item {{ background: var(--item); padding: 12px; border-radius: 8px; margin: 6px 15px; cursor: pointer; font-size: 13px; font-weight: 500; border: 1px solid #ddd; }}
        .player {{ position: sticky; top: 0; z-index: 100; background: #000; display: none; }}
    </style>
</head>
<body>
    <div id="welcome" class="welcome">
        <h1 style="color:green; font-size: 50px;">Welcome</h1>
        <div class="info-box">
            <h2>{title}</h2>
            <p style="color:orange; font-weight:bold;">📥 Created By : Tushar</p>
            <p style="font-size:12px;">📅 Created On : {now_full}</p>
        </div>
        <button class="btn" style="background:red;" onclick="start()">Open Your Batch</button><br>
        <button class="btn" style="background:#007bff;" onclick="dark()">Switch to Dark Mode</button>
    </div>

    <div id="main" style="display:none;">
        <div id="p-box" class="player"><video id="vid" class="video-js vjs-fluid" controls preload="auto"></video></div>
        <div class="top-bar">📅 Date & Time : {now_full}</div>
        <div style="text-align:center; padding-top:10px;">
            <button class="btn" style="width:auto; padding:8px 20px; font-size:12px;" onclick="dark()">Switch to Dark Mode</button>
            <div style="color:#007bff; font-weight:bold; margin:10px;">Videos: {v_t} | PDFs: {p_t} | Others: {o_t}</div>
            
            <div class="filters">
                <button class="f-btn" onclick="fil('video')">Videos</button>
                <button class="f-btn" onclick="fil('pdf')">PDFs</button>
                <button class="f-btn" onclick="fil('other')">Others</button>
            </div>
            
            <input type="text" id="q" class="search-bar" placeholder="Search videos / pdfs / others..." onkeyup="src()">
            <img src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b" style="width:95%; border-radius:12px; margin:10px 0;">
        </div>
        {html_folders}
        <a href="{TELEGRAM_LINK}" style="color:red; display:block; text-align:center; padding:30px; font-weight:bold; text-decoration:none;">JOIN TELEGRAM</a>
    </div>

    <script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
    <script>
        const p = videojs('vid');
        function start() {{ document.getElementById('welcome').style.display='none'; document.getElementById('main').style.display='block'; window.scrollTo(0,0); }}
        function dark() {{ document.body.classList.toggle('dark-mode'); }}
        function toggle(id) {{ let e=document.getElementById(id); e.style.display=e.style.display==='none'?'block':'none'; }}
        function playV(u, n) {{ 
            document.getElementById('p-box').style.display='block'; 
            p.src({{src: u, type: u.includes('m3u8') ? 'application/x-mpegURL' : 'video/mp4'}}); 
            p.play(); window.scrollTo(0,0); 
        }}
        function fil(t) {{ 
            document.querySelectorAll('.item').forEach(i => i.style.display = i.dataset.type===t ? 'block':'none');
            document.querySelectorAll('.folder-content').forEach(c => c.style.display='block');
        }}
        function src() {{ 
            let v=document.getElementById('q').value.toLowerCase(); 
            document.querySelectorAll('.item').forEach(i => i.style.display = i.innerText.toLowerCase().includes(v)?'block':'none');
        }}
    </script>
</body>
</html>
"""

# ================= COMMANDS & HANDLERS =================
@app.on_message(filters.command("start"))
async def start_cmd(c, m):
    user_mode[m.from_user.id] = "normal"
    await m.reply_text("🚀 **Bot Active!**\n- /domain : Domain Change Mode\n- /normal : HTML Mode")

@app.on_message(filters.command("domain"))
async def domain_cmd(c, m):
    user_mode[m.from_user.id] = "domain"
    await m.reply_text("🔁 **Domain Mode ON**\nAb .txt file bhejo, main video links badal kar TXT hi dunga.")

@app.on_message(filters.document)
async def handle_file(c, m):
    if not m.document.file_name.endswith(".txt"): return
    uid = m.from_user.id
    path = await m.download()

    if user_mode.get(uid) == "domain":
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(replace_video_domains(line))
        await m.reply_document(path, caption="✅ Video domains replaced (TXT).")
        os.remove(path); return

    with open(path, "r", encoding="utf-8") as f:
        html = generate_html(m.document.file_name, f.read())
    h_path = path.replace(".txt", ".html")
    with open(h_path, "w", encoding="utf-8") as f: f.write(html)
    await m.reply_document(h_path, caption=f"👑 **Batch HTML Ready**\nOwner: {BOT_OWNER_NAME}")
    os.remove(path); os.remove(h_path)

app.run()
