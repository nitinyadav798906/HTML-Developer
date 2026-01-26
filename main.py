import os
import re
from datetime import datetime
from pyrogram import Client, filters

# ================= CONFIG =================
BOT_OWNER_NAME = "Sachin Yadav & Nitin Yadav"
API_ID = 12475131
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"

OLD_DOMAINS = ["https://apps-s3-jw-prod.utkarshapp.com/", "https://apps-s3-prod.utkarshapp.com/", "https://apps-s3-video-dist.utkarshapp.com/"]
NEW_DOMAIN = "https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/"

app = Client("ultimate_option_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_mode = {}

def fix_domain(url):
    for d in OLD_DOMAINS:
        if d in url: return url.replace(d, NEW_DOMAIN)
    return url

# ================= 1. HTML TO TXT =================
def html_to_txt(html_content):
    matches = re.findall(r'playVideo\(\'(.*?)\'', html_content) or re.findall(r'window\.open\(\'(.*?)\'\)', html_content)
    names = re.findall(r'<div class="item-name".*?>(.*?)</div>', html_content)
    extracted = []
    for u, n in zip(matches, names):
        extracted.append(f"{n.strip()}: {u}")
    return "\n".join(extracted)

# ================= 2. TXT TO HTML =================
def generate_html(file_name, content):
    title = os.path.splitext(file_name)[0]
    now = datetime.now().strftime("%d %b %Y")
    lines = content.strip().split("\n")
    v_t, p_t = 0, 0
    folder_data = []
    current_folder = None

    for line in lines:
        line = line.strip()
        if not line or "http" not in line: continue
        name, url = line.split(":", 1) if ":" in line else ("Class", line)
        name, url = name.strip(), fix_domain(url.strip())
        
        if re.match(r'^(01|1)[\s\.\-]', name) or current_folder is None:
            if current_folder: folder_data.append(current_folder)
            f_name = re.sub(r'^(01|1)[\s\.\-]', '', name).strip()
            current_folder = {"name": f_name, "items": []}

        t = "video" if any(x in url.lower() for x in [".mp4", ".m3u8", ".mpd"]) else "pdf"
        if t == "video": v_t += 1
        else: p_t += 1
        current_folder["items"].append({"name": name, "url": url, "type": t})
            
    if current_folder: folder_data.append(current_folder)

    html_folders = ""
    for idx, f in enumerate(folder_data):
        html_folders += f'''
        <div class="folder" onclick="toggle('f-{idx}')">
            <span>📂 {f['name']}</span>
            <span class="count-badge">{len(f['items'])}</span>
        </div>
        <div id="f-{idx}" class="content" style="display:none;">'''
        for i in f['items']:
            icon = "🎬" if i['type']=="video" else "📄"
            if i['type']=="video":
                btn = f'''<div class="item">
                            <div class="item-name">{icon} {i["name"]}</div>
                            <div class="opt-btns">
                                <button onclick="playVideo('{i['url']}')">▶️ Play</button>
                                <button onclick="window.open('{i['url']}')">🔗 Link</button>
                            </div>
                          </div>'''
            else:
                btn = f'<div class="item" onclick="window.open(\'{i["url"]}\')">{icon} {i["name"]}</div>'
            html_folders += btn
        html_folders += "</div>"

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <style>
        body {{ font-family: 'Poppins', sans-serif; background: #f8f9fa; margin: 0; padding-bottom: 70px; }}
        .header {{ background: linear-gradient(135deg, #007bff, #00d2d3); color: white; padding: 25px 15px; text-align: center; border-radius: 0 0 25px 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
        #player-container {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 3000; }}
        .close-p {{ position: absolute; top: 15px; right: 20px; color: white; font-size: 35px; cursor: pointer; z-index: 3001; }}
        .folder {{ background: white; margin: 12px; padding: 18px; border-radius: 12px; font-weight: bold; display: flex; justify-content: space-between; align-items: center; border-bottom: 3px solid #eee; }}
        .count-badge {{ background: #007bff; color: white; padding: 2px 10px; border-radius: 20px; font-size: 11px; }}
        .item {{ background: white; margin: 8px 15px; padding: 12px; border-radius: 10px; border-left: 5px solid #007bff; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .opt-btns {{ display: flex; gap: 10px; margin-top: 8px; }}
        .opt-btns button {{ flex: 1; padding: 8px; border: none; border-radius: 5px; background: #f0f2f5; font-weight: bold; cursor: pointer; }}
        .item-name {{ font-size: 13px; font-weight: 600; }}
        .search-box {{ width: 85%; padding: 12px; border: none; border-radius: 10px; margin: -20px auto 10px; display: block; box-shadow: 0 4px 10px rgba(0,0,0,0.1); outline: none; }}
    </style>
</head>
<body>
    <div id="player-container"><span class="close-p" onclick="closePlayer()">&times;</span><video id="player" playsinline controls></video></div>
    <div class="header">
        <h2 style="margin:0;">{title}</h2>
        <p style="font-size:12px; margin:5px 0;">🎥 {v_t} Videos | 📄 {p_t} PDFs</p>
        <p style="font-size:10px; opacity:0.8;">Owner: {BOT_OWNER_NAME} | {now}</p>
    </div>
    <input type="text" id="q" class="search-box" placeholder="Search lessons..." onkeyup="src()">
    {html_folders}
    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        const player = new Plyr('#player');
        function playVideo(url) {{
            document.getElementById('player-container').style.display = 'block';
            if (url.includes('.m3u8')) {{ const hls = new Hls(); hls.loadSource(url); hls.attachMedia(document.getElementById('player')); }}
            else {{ document.getElementById('player').src = url; }}
            player.play();
        }}
        function closePlayer() {{ player.pause(); document.getElementById('player-container').style.display = 'none'; }}
        function toggle(id) {{ var e = document.getElementById(id); e.style.display = e.style.display === 'none' ? 'block' : 'none'; }}
        function src() {{ 
            var v = document.getElementById('q').value.toLowerCase(); 
            document.querySelectorAll('.item').forEach(i => i.style.display = i.innerText.toLowerCase().includes(v) ? 'block' : 'none'); 
        }}
    </script>
</body>
</html>
"""

# ================= COMMANDS =================
@app.on_message(filters.command("start"))
async def start(c, m):
    await m.reply_text(f"🚀 **{BOT_OWNER_NAME} Bot Active**\n\nCommands:\n/html - TXT to HTML\n/txt - HTML to TXT\n/domain - Only Change Domain")

@app.on_message(filters.command(["html", "txt", "domain"]))
async def mode(c, m):
    user_mode[m.from_user.id] = m.command[0]
    await m.reply_text(f"✅ Mode Switched: **{m.command[0].upper()}**")

@app.on_message(filters.document)
async def handle(c, m):
    mode = user_mode.get(m.from_user.id, "html")
    path = await m.download()
    
    if mode == "txt":
        with open(path, "r", encoding="utf-8") as f: data = html_to_txt(f.read())
        out = path.replace(".html", ".txt")
        with open(out, "w", encoding="utf-8") as f: f.write(data)
    elif mode == "domain":
        with open(path, "r", encoding="utf-8") as f: lines = f.readlines()
        with open(path, "w", encoding="utf-8") as f:
            for l in lines: f.write(fix_domain(l))
        out = path
    else:
        with open(path, "r", encoding="utf-8") as f: html = generate_html(m.document.file_name, f.read())
        out = path.replace(".txt", ".html")
        with open(out, "w", encoding="utf-8") as f: f.write(html)

    await m.reply_document(out, caption=f"✨ Processed by {BOT_OWNER_NAME}")
    os.remove(path)
    if out != path: os.remove(out)

app.run()
