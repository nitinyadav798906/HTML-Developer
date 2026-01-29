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

app = Client("ultimate_dashboard_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_mode = {}

def fix_domain(url):
    low = url.lower()
    if any(x in low for x in [".mp4", ".m3u8", ".mpd", "/m3u8"]):
        for d in OLD_DOMAINS:
            if d in url: return url.replace(d, NEW_DOMAIN)
    return url

# ================= 1. HTML TO TXT (Don't Remove) =================
def html_to_txt(html_content):
    matches = re.findall(r"onclick=\"openModal\('(.*?)',", html_content) or re.findall(r"window\.open\('(.*?)'\)", html_content)
    names = re.findall(r'<div class="item-title">(.*?)</div>', html_content)
    extracted = [f"{n.strip()}: {u}" for u, n in zip(names, matches)]
    return "\n".join(extracted)

# ================= 2. TXT TO HTML (Final Dashboard) =================
def generate_html(file_name, content):
    title = os.path.splitext(file_name)[0]
    now_date = datetime.now().strftime("%d %b %Y")
    now_time = datetime.now().strftime("%I:%M:%S %p")
    lines = [l for l in content.strip().split("\n") if ":" in l and "http" in l]
    
    v_c = p_c = a_c = o_c = 0
    items_html = ""

    for idx, line in enumerate(lines):
        name, url = line.split(":", 1)
        name, url = name.strip(), fix_domain(url.strip())
        low_u = url.lower()
        
        if any(x in low_u for x in [".mp4", ".m3u8", ".mpd"]): t = "VIDEO"; v_c += 1; icon = "🎥"
        elif ".pdf" in low_u: t = "PDF"; p_c += 1; icon = "📄"
        elif any(x in low_u for x in [".mp3", ".wav"]): t = "AUDIO"; a_c += 1; icon = "🎵"
        else: t = "OTHER"; o_c += 1; icon = "📁"

        items_html += f'''
        <div class="list-item" data-type="{t}" onclick="openModal('{url}', '{name}', '{t}')">
            <div class="item-icon-bg">{icon}</div>
            <div class="item-details">
                <div class="item-title">{name}</div>
                <div class="item-meta">Type: {t} | Path: {title}</div>
            </div>
        </div>'''

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <style>
        :root {{ --bg: #f8f9fa; --text: #333; --card: #fff; --border: #eee; --primary: #8e44ad; }}
        .dark-mode {{ --bg: #121212; --text: #eee; --card: #1e1e1e; --border: #333; --primary: #bb86fc; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; transition: 0.3s; padding-bottom: 20px; }}
        .header {{ background: var(--card); padding: 25px 15px; border-bottom: 1px solid var(--border); text-align: center; }}
        .header h1 {{ font-size: 20px; color: var(--primary); margin: 0 0 10px; }}
        .header-meta {{ font-size: 11px; color: #7f8c8d; display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; }}
        .controls {{ display: flex; justify-content: center; align-items: center; gap: 20px; margin-top: 15px; }}
        .switch {{ position: relative; display: inline-block; width: 45px; height: 22px; }}
        .switch input {{ opacity: 0; width: 0; height: 0; }}
        .slider {{ position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #ccc; transition: .4s; border-radius: 34px; }}
        .slider:before {{ position: absolute; content: ""; height: 16px; width: 16px; left: 4px; bottom: 3px; background-color: white; transition: .4s; border-radius: 50%; }}
        input:checked + .slider {{ background-color: var(--primary); }}
        input:checked + .slider:before {{ transform: translateX(21px); }}
        
        .dashboard {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding: 15px; }}
        .card {{ background: var(--card); padding: 15px; border-radius: 12px; border: 1px solid var(--border); box-shadow: 0 4px 6px rgba(0,0,0,0.02); }}
        .card-num {{ font-size: 22px; font-weight: bold; margin-bottom: 4px; }}
        .card-label {{ font-size: 10px; color: #95a5a6; text-transform: uppercase; font-weight: bold; }}
        
        .search-bar {{ padding: 0 15px 10px; }}
        #srcInput {{ width: 100%; padding: 12px; border-radius: 10px; border: 1px solid var(--border); background: var(--card); color: var(--text); outline: none; box-sizing: border-box; }}
        
        .list-section {{ padding: 0 15px; }}
        .list-item {{ background: var(--card); margin-bottom: 10px; padding: 15px; border-radius: 12px; display: flex; align-items: center; border: 1px solid var(--border); cursor: pointer; transition: 0.2s; }}
        .list-item:active {{ transform: scale(0.98); }}
        .item-icon-bg {{ width: 45px; height: 45px; background: rgba(142, 68, 173, 0.1); border-radius: 10px; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-size: 22px; }}
        .item-details {{ overflow: hidden; }}
        .item-title {{ font-size: 14px; font-weight: 600; white-space: nowrap; text-overflow: ellipsis; overflow: hidden; }}
        .item-meta {{ font-size: 11px; color: #95a5a6; margin-top: 4px; }}

        .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 2000; align-items: center; justify-content: center; }}
        .modal-content {{ background: var(--card); width: 95%; max-width: 650px; border-radius: 15px; overflow: hidden; position: relative; }}
        .close-btn {{ position: absolute; top: 10px; right: 15px; font-size: 28px; cursor: pointer; color: var(--text); z-index: 2001; opacity: 0.7; }}
        .player-info {{ padding: 15px; font-size: 12px; line-height: 1.6; border-top: 1px solid var(--border); }}
    </style>
</head>
<body>
    <div id="videoModal" class="modal">
        <div class="modal-content">
            <span class="close-btn" onclick="closeModal()">&times;</span>
            <video id="player" playsinline controls></video>
            <div class="player-info" id="pInfo"></div>
        </div>
    </div>

    <div class="header">
        <h1>{title}</h1>
        <div class="header-meta">
            <span>📚 {len(lines)} Items</span> | <span>📅 {now_date}</span> | <span>🕒 {now_time}</span>
        </div>
        <div class="controls">
            <span>🌙 Dark Mode</span>
            <label class="switch"><input type="checkbox" onchange="toggleMode()"><span class="slider"></span></label>
        </div>
    </div>

    <div class="dashboard">
        <div class="card"><div class="card-num">{len(lines)}</div><div class="card-label">All Items</div></div>
        <div class="card" style="border-top: 3px solid #e74c3c;"><div class="card-num" style="color:#e74c3c;">{v_c}</div><div class="card-label">Videos</div></div>
        <div class="card" style="border-top: 3px solid #2ecc71;"><div class="card-num" style="color:#2ecc71;">{p_c}</div><div class="card-label">PDFs</div></div>
        <div class="card" style="border-top: 3px solid #f1c40f;"><div class="card-num" style="color:#f1c40f;">{a_c}</div><div class="card-label">Audio</div></div>
    </div>

    <div class="search-bar">
        <input type="text" id="srcInput" placeholder="Search by title..." onkeyup="search()">
    </div>

    <div class="list-section">
        <h3 style="margin-left: 5px; font-size: 16px;">All Content</h3>
        <div id="itemList">{items_html}</div>
    </div>

    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        const player = new Plyr('#player', {{ speed: {{ selected: 1, options: [0.5, 0.75, 1, 1.25, 1.5, 2] }} }});
        function toggleMode() {{ document.body.classList.toggle('dark-mode'); }}
        function search() {{
            let v = document.getElementById('srcInput').value.toLowerCase();
            document.querySelectorAll('.list-item').forEach(i => {{
                i.style.display = i.innerText.toLowerCase().includes(v) ? 'flex' : 'none';
            }});
        }}
        function openModal(url, name, type) {{
            if(type === 'VIDEO') {{
                document.getElementById('videoModal').style.display = 'flex';
                if (url.includes('.m3u8')) {{
                    const hls = new Hls(); hls.loadSource(url); hls.attachMedia(document.getElementById('player'));
                }} else {{ document.getElementById('player').src = url; }}
                document.getElementById('pInfo').innerHTML = `<b>Title:</b> ${{name}}<br><b>Type:</b> ${{type}}<br><b>Path:</b> {title}`;
                player.play();
            }} else {{ window.open(url); }}
        }}
        function closeModal() {{ player.pause(); document.getElementById('videoModal').style.display = 'none'; }}
    </script>
</body>
</html>
"""

# ================= COMMANDS =================
@app.on_message(filters.command("start"))
async def start(c, m):
    await m.reply_text(f"👑 **{BOT_OWNER_NAME} Bot Active**\n\n/html - Professional Dashboard\n/txt - Link Extractor\n/domain - Video Domain Changer")

@app.on_message(filters.command(["html", "txt", "domain"]))
async def mode(c, m):
    user_mode[m.from_user.id] = m.command[0]
    await m.reply_text(f"✅ Mode Set: **{m.command[0].upper()}**")

@app.on_message(filters.document)
async def handle(c, m):
    mode = user_mode.get(m.from_user.id, "html")
    path = await m.download()
    if mode == "txt":
        with open(path, "r", encoding="utf-8") as f: data = html_to_txt(f.read())
        out = path.replace(".html", ".txt")
    elif mode == "domain":
        with open(path, "r", encoding="utf-8") as f: lines = f.readlines()
        with open(path, "w", encoding="utf-8") as f:
            for l in lines:
                if ":" in l:
                    nm, url = l.split(":", 1)
                    f.write(f"{nm}: {fix_domain(url.strip())}\n")
                else: f.write(l)
        out = path
    else:
        with open(path, "r", encoding="utf-8") as f: html = generate_html(m.document.file_name, f.read())
        out = path.replace(".txt", ".html")
        with open(out, "w", encoding="utf-8") as f: f.write(html)
    await m.reply_document(out, caption=f"✨ Done by {BOT_OWNER_NAME}")
    os.remove(path)

app.run()
