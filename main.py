import os
import re
import sys
from datetime import datetime
from pyrogram import Client, filters

# ================= CONFIG =================
BOT_OWNER_NAME = "Sachin Yadav & Nitin Yadav"
API_ID = 12475131
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"
SKY_PASSWORD = "7989"  # /sky command password

OLD_DOMAINS = ["https://apps-s3-jw-prod.utkarshapp.com/", "https://apps-s3-prod.utkarshapp.com/", "https://apps-s3-video-dist.utkarshapp.com/"]
NEW_DOMAIN = "https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/"

app = Client("ultimate_final_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_mode = {}

def fix_domain(url):
    low = url.lower()
    if any(x in low for x in [".m3u8", ".mpd", ".mp4", "/m3u8"]):
        for d in OLD_DOMAINS:
            if d in url: return url.replace(d, NEW_DOMAIN)
    return url

# ================= HTML MASTER GENERATOR =================
def generate_html(file_name, content, is_protected=False):
    title = os.path.splitext(file_name)[0]
    now_date = datetime.now().strftime("%d %b %Y")
    now_time = datetime.now().strftime("%I:%M:%S %p")
    
    # Accurate Link Extraction
    raw_lines = re.findall(r"([^:\n]+):?\s*(https?://[^\s\n]+)", content)
    v_c = p_c = a_c = 0
    items_html = ""

    for name, url in raw_lines:
        url = fix_domain(url.strip())
        low_u = url.lower()
        if any(x in low_u for x in [".m3u8", ".mpd", ".mp4"]): t = "VIDEO"; v_c += 1; icon = "📽️"
        elif ".pdf" in low_u: t = "PDF"; p_c += 1; icon = "📄"
        elif any(x in low_u for x in [".m4a", ".mp3"]): t = "AUDIO"; a_c += 1; icon = "🎵"
        else: t = "OTHER"; icon = "📁"

        items_html += f'''
        <div class="list-item" data-type="{t}" onclick="openModal('{url}', '{name.strip()}', '{t}')">
            <div class="item-icon-bg">{icon}</div>
            <div class="item-details">
                <div class="item-title">{name.strip()}</div>
                <div class="item-meta">Type: {t} | Path: {title}</div>
            </div>
        </div>'''

    pass_logic = f"""
    let pass = prompt("🔐 Enter Batch Access Key ({BOT_OWNER_NAME}):");
    if(pass !== "{SKY_PASSWORD}") {{
        document.body.innerHTML = "<div style='display:flex; height:100vh; align-items:center; justify-content:center; flex-direction:column; background:#121212; color:white; font-family:sans-serif;'> <h1 style='color:#ff4d4d;'>❌ Access Denied</h1> <p style='opacity:0.7;'>Incorrect Password!</p> <button onclick='location.reload()' style='padding:10px 20px; border-radius:5px; border:none; background:#8e44ad; color:white; cursor:pointer;'>Try Again</button> </div>";
    }}
    """ if is_protected else ""

    return f"""
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <style>
        :root {{ --bg: #f8f9fa; --text: #333; --card: #fff; --purple: #8e44ad; }}
        .dark-mode {{ --bg: #121212; --text: #eee; --card: #1e1e1e; --purple: #bb86fc; }}
        body {{ font-family: sans-serif; background: var(--bg); color: var(--text); margin: 0; padding-bottom: 20px; transition: 0.3s; }}
        .header {{ background: var(--card); padding: 20px; text-align: center; border-bottom: 1px solid #eee; position: sticky; top:0; z-index:100; }}
        .dashboard {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 15px; }}
        .card {{ background: var(--card); padding: 15px; border-radius: 12px; border-left: 5px solid var(--purple); cursor: pointer; border: 1px solid #eee; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .list-item {{ background: var(--card); margin: 8px 15px; padding: 12px; border-radius: 10px; display: flex; align-items: center; border: 1px solid #eee; cursor: pointer; }}

.item-icon-bg {{ width: 45px; height: 45px; background: rgba(142,68,173,0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 12px; font-size: 20px; }}
        .modal {{ display: none; position: fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.9); z-index:999; align-items:center; justify-content:center; }}
        .m-body {{ background: var(--card); width: 95%; max-width: 650px; border-radius: 12px; overflow: hidden; position: relative; }}
        #watermark {{ position: absolute; color: rgba(255,255,255,0.2); font-size: 14px; pointer-events: none; z-index: 10; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.5); }}
        
        /* New Controls Style */
        .speed-btn-row {{ display: flex; justify-content: space-around; padding: 10px; background: #f9f9f9; border-top: 1px solid #eee; flex-wrap: wrap; gap: 5px; }}
        .speed-btn-row button {{ border: none; background: #eee; padding: 6px 12px; border-radius: 5px; cursor: pointer; font-size: 12px; font-weight: bold; color: #333; }}
        .active-speed {{ background: var(--purple) !important; color: white !important; }}
        .extra-btn {{ background: #333 !important; color: white !important; display: flex; align-items: center; gap: 5px; }}
        .fav-active {{ color: #e74c3c !important; }}
        
        .search-container {{ padding: 0 15px; margin-bottom: 10px; }}
        #searchInput {{ width: 100%; padding: 12px; border-radius: 8px; border: 1px solid #ddd; outline: none; background: var(--card); color: var(--text); }}
    </style>
</head>
<body>
    <div id="vModal" class="modal">
        <div class="m-body">
            <div id="watermark">{BOT_OWNER_NAME}</div>
            <div style="padding:12px; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #eee;">
                <b id="mT" style="font-size:12px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:70%;">Player</b>
                <div>
                    <span onclick="minimizePlayer()" style="cursor:pointer; margin-right:15px; font-size:18px;">📺</span>
                    <span onclick="closeModal()" style="cursor:pointer; font-size:24px;">&times;</span>
                </div>
            </div>
            <video id="player" playsinline controls></video>
            
            <div class="speed-btn-row">
                <button onclick="changeSpeed(0.5, this)">0.5x</button>
                <button onclick="changeSpeed(1, this)" class="active-speed">1x</button>
                <button onclick="changeSpeed(1.5, this)">1.5x</button>
                <button onclick="changeSpeed(2, this)">2x</button>
            </div>
            
            <div class="speed-btn-row" style="border-top:none; padding-top:0;">
                <button class="extra-btn" onclick="seek(-10)">⏪ 10s</button>
                <button class="extra-btn" onclick="seek(10)">10s ⏩</button>
                <button class="extra-btn" onclick="downloadVid()">⬇️ DL</button>
                <button class="extra-btn" onclick="toggleFav(this)">🤍 Fav</button>
            </div>
        </div>
    </div>

    <div class="header">
        <h1 style="font-size:18px; color:var(--purple);">{title}</h1>
        <div style="font-size:10px; color:#777; margin-top:5px;">📅 {now_date} | 🕒 {now_time} | <span onclick="document.body.classList.toggle('dark-mode')" style="cursor:pointer; color:var(--purple); font-weight:bold;">🌓 THEME</span></div>
    </div>

    <div class="dashboard">
        <div class="card" onclick="runFilter('all')"><b>{len(raw_lines)}</b><br><small>ALL ITEMS</small></div>
        <div class="card" onclick="runFilter('VIDEO')" style="border-left-color:#e74c3c;"><b style="color:#e74c3c;">{v_c}</b><br><small>VIDEOS</small></div>
        <div class="card" onclick="runFilter('PDF')" style="border-left-color:#2ecc71;"><b style="color:#2ecc71;">{p_c}</b><br><small>PDFS</small></div>
        <div class="card" onclick="runFilter('AUDIO')" style="border-left-color:#f1c40f;"><b style="color:#f1c40f;">{a_c}</b><br><small>AUDIO</small></div>
    </div>

    <div class="search-container"><input type="text" id="searchInput" placeholder="Search lessons..." onkeyup="search()"></div>
    <div id="itemList">{items_html}</div>

    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        {pass_logic}
        const player = new Plyr('#player', {{ settings: ['quality'] }});
        let hls = new Hls();
        let currentVidUrl = ""; // Store current URL for download

        function openModal(url, name, type) {{
            if(type === 'VIDEO') {{
                currentVidUrl = url; // Save URL
                document.getElementById('vModal').style.display = 'flex';
                document.getElementById('mT').innerText = name;
                if(url.includes('.m3u8')) {{
                    hls.loadSource(url); hls.attachMedia(document.getElementById('player'));
                    hls.on(Hls.Events.MANIFEST_PARSED, () => {{
                        const q = hls.levels.map(l => l.height);
                        player.config.quality = {{ default: q[0], options: q, onChange: v => hls.currentLevel = hls.levels.findIndex(l => l.height === v) }};
                    }});
                }} else {{ document.getElementById('player').src = url; }}
                player.play();
                startWatermark();
            }} else {{ window.open(url); }}
        }}

        // --- NEW FUNCTIONS START ---
        function seek(sec) {{
            player.currentTime += sec;
        }}
        
        function downloadVid() {{
            if(currentVidUrl) window.open(currentVidUrl, '_blank');
        }}

        function toggleFav(btn) {{
            if(btn.innerText.includes('🤍')) {{
                btn.innerText = '❤️ Saved';
                btn.style.color = '#e74c3c';
            }} else {{
                btn.innerText = '🤍 Fav';
                btn.style.color = 'white';
            }}
        }}
        // --- NEW FUNCTIONS END ---

        function changeSpeed(s, btn) {{
            player.speed = s;
            document.querySelectorAll('.speed-btn-row:first-of-type button').forEach(b => b.classList.remove('active-speed'));
            btn.classList.add('active-speed');
        }}

        function startWatermark() {{
            const w = document.getElementById('watermark');
            setInterval(() => {{
                w.style.top = Math.random() * 70 + 10 + "%";
                w.style.left = Math.random() * 70 + 10 + "%";
            }}, 5000);
        }}

        function minimizePlayer() {{ if (document.getElementById('player').requestPictureInPicture) document.getElementById('player').requestPictureInPicture(); }}
        function closeModal() {{ player.pause(); hls.detachMedia(); document.getElementById('vModal').style.display = 'none'; }}
        function runFilter(t) {{ document.querySelectorAll('.list-item').forEach(i => i.style.display = (t === 'all' || i.getAttribute('data-type') === t) ? 'flex' : 'none'); }}
        function search() {{
            let v = document.getElementById('searchInput').value.toLowerCase();
            document.querySelectorAll('.list-item').forEach(i => i.style.display = i.innerText.toLowerCase().includes(v) ? 'flex' : 'none');
        }}
    </script>
</body>
</html>
"""

# ================= COMMANDS =================
@app.on_message(filters.command(["start", "stop", "html", "sky", "txt"]))
async def handle_cmds(c, m):
    cmd = m.command[0]
    if cmd == "start":
        return await m.reply_text(f"👑 {BOT_OWNER_NAME} Bot Active\n\n/html - Normal Dashboard\n/sky - Password Protected\n/txt - Link Extractor\n/stop - Reset Bot")
    if cmd == "stop":
        user_mode.pop(m.from_user.id, None)
        return await m.reply_text("🛑 Process Stopped & Memory Cleared.")
    user_mode[m.from_user.id] = cmd
    await m.reply_text(f"✅ Mode Set: {cmd.upper()}\nAb .txt file bhejo!")

@app.on_message(filters.document)
async def process_file(c, m):
    uid = m.from_user.id
    mode = user_mode.get(uid)
    if not mode: return await m.reply_text("❌ Select Mode First!")
    
    path = await m.download()
    with open(path, "r", encoding="utf-8") as f: content = f.read()
    
    if mode in ["html", "sky"]:
        out = path.split('.')[0] + ".html"
        with open(out, "w", encoding="utf-8") as f:
            f.write(generate_html(m.document.file_name, content, is_protected=(mode == "sky")))
        cap = "🔒 Protected (Pass: 7989)" if mode == "sky" else "✨ Normal Dashboard"
    
    elif mode == "txt":
        links = re.findall(r"(https?://[^\s\n]+)", content)
        out = path.split('.')[0] + "_links.txt"
        with open(out, "w", encoding="utf-8") as f: f.write("\n".join(links))
        cap = "📄 Links Extracted"

    await m.reply_document(out, caption=f"{cap}\nBy: {BOT_OWNER_NAME}")
    os.remove(path); os.remove(out)

app.run()
