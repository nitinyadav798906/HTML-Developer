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

app = Client("quality_dashboard_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_mode = {}

def fix_domain(url):
    low = url.lower()
    if any(x in low for x in [".mp4", ".m3u8", ".mpd"]):
        for d in OLD_DOMAINS:
            if d in url: return url.replace(d, NEW_DOMAIN)
    return url

# ================= HTML GENERATOR (Quality + Dashboard) =================
def generate_html(file_name, content):
    title = os.path.splitext(file_name)[0]
    now_date = datetime.now().strftime("%d %b %Y")
    now_time = datetime.now().strftime("%I:%M:%S %p")
    lines = [l for l in content.strip().split("\n") if ":" in l and "http" in l]
    
    v_c = p_c = a_c = 0
    items_html = ""

    for line in lines:
        name, url = line.split(":", 1)
        name, url = name.strip(), fix_domain(url.strip())
        low_u = url.lower()
        if any(x in low_u for x in [".mp4", ".m3u8"]): t = "VIDEO"; v_c += 1; icon = "📽️"
        elif ".pdf" in low_u: t = "PDF"; p_c += 1; icon = "📄"
        elif ".mp3" in low_u: t = "AUDIO"; a_c += 1; icon = "🎵"
        else: t = "OTHER"; icon = "📁"

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
<html lang="hi">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <style>
        :root {{ --bg: #f8f9fa; --text: #333; --card: #fff; --border: #eee; --purple: #8e44ad; }}
        .dark-mode {{ --bg: #121212; --text: #eee; --card: #1e1e1e; --border: #333; --purple: #bb86fc; }}
        body {{ font-family: sans-serif; background: var(--bg); color: var(--text); margin: 0; padding-bottom: 20px; }}
        .header {{ background: var(--card); padding: 20px 10px; text-align: center; border-bottom: 1px solid var(--border); }}
        .header h1 {{ color: var(--purple); font-size: 18px; margin: 0; }}
        .meta-row {{ font-size: 10px; color: #777; margin: 8px 0; display: flex; justify-content: center; gap: 10px; }}
        .dashboard {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 15px; }}
        .card {{ background: var(--card); padding: 12px; border-radius: 12px; border: 1px solid var(--border); cursor: pointer; border-left: 4px solid var(--purple); }}
        .search-area {{ padding: 0 15px; }}
        #searchInput {{ width: 100%; padding: 12px; border-radius: 8px; border: 1px solid var(--border); background: var(--card); color: var(--text); }}
        .list-item {{ background: var(--card); padding: 12px; border-radius: 10px; display: flex; align-items: center; border: 1px solid var(--border); margin: 8px 15px; cursor: pointer; }}
        .item-icon-bg {{ width: 40px; height: 40px; background: rgba(142,68,173,0.1); border-radius: 8px; display: flex; align-items: center; justify-content: center; margin-right: 12px; }}
        .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.9); z-index: 3000; align-items: center; justify-content: center; }}
        .modal-body {{ background: var(--card); width: 95%; max-width: 650px; border-radius: 12px; overflow: hidden; }}
    </style>
</head>
<body>
    <div id="vModal" class="modal">
        <div class="modal-body">
            <div style="padding:10px; border-bottom:1px solid var(--border); display:flex; justify-content:space-between;">
                <span id="mT" style="font-size:14px; font-weight:bold;"></span>
                <span onclick="closeModal()" style="cursor:pointer; font-size:20px;">&times;</span>
            </div>
            <video id="player" playsinline controls></video>
        </div>
    </div>
    <div class="header">
        <h1>{title}</h1>
        <div class="meta-row"><span>📚 {len(lines)} Items</span>|<span>📅 {now_date}</span>|<span>🕒 {now_time}</span></div>
        <div onclick="document.body.classList.toggle('dark-mode')" style="cursor:pointer; font-size:11px; margin-top:5px;">🌙 Toggle Theme</div>
    </div>
    <div class="dashboard">
        <div class="card" onclick="runFilter('all')"><div style="font-size:20px; font-weight:bold;">{len(lines)}</div><div style="font-size:10px; opacity:0.7;">ALL ITEMS</div></div>
        <div class="card" onclick="runFilter('VIDEO')" style="border-left-color: #e74c3c;"><div style="font-size:20px; font-weight:bold; color:#e74c3c;">{v_c}</div><div style="font-size:10px; opacity:0.7;">VIDEOS</div></div>
        <div class="card" onclick="runFilter('PDF')" style="border-left-color: #2ecc71;"><div style="font-size:20px; font-weight:bold; color:#2ecc71;">{p_c}</div><div style="font-size:10px; opacity:0.7;">PDFS</div></div>
        <div class="card" onclick="runFilter('AUDIO')" style="border-left-color: #f1c40f;"><div style="font-size:20px; font-weight:bold; color:#f1c40f;">{a_c}</div><div style="font-size:10px; opacity:0.7;">AUDIO</div></div>
    </div>
    <div class="search-area"><input type="text" id="searchInput" placeholder="Search content..." onkeyup="runSearch()"></div>
    <div id="itemList">{items_html}</div>
    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        let hls = new Hls();
        const player = new Plyr('#player', {{ 
            speed: {{ selected: 1, options: [0.5, 0.75, 1, 1.25, 1.5, 2] }},
            settings: ['quality', 'speed', 'loop']
        }});

        function openModal(url, name, type) {{
            if(type === 'VIDEO') {{
                document.getElementById('vModal').style.display = 'flex';
                document.getElementById('mT').innerText = name;
                if (url.includes('.m3u8')) {{
                    hls.loadSource(url); hls.attachMedia(document.getElementById('player'));
                    hls.on(Hls.Events.MANIFEST_PARSED, function(event, data) {{
                        const availableQualities = hls.levels.map((l) => l.height);
                        player.config.quality = {{ default: availableQualities[0], options: availableQualities, onChange: (v) => {{ hls.currentLevel = hls.levels.findIndex((l) => l.height === v); }} }};
                    }});
                }} else {{ document.getElementById('player').src = url; }}
                player.play();
            }} else {{ window.open(url); }}
        }}
        function closeModal() {{ player.pause(); hls.detachMedia(); document.getElementById('vModal').style.display = 'none'; }}
        function runFilter(t) {{ document.querySelectorAll('.list-item').forEach(i => i.style.display = (t === 'all' || i.getAttribute('data-type') === t) ? 'flex' : 'none'); }}
        function runSearch() {{ let v = document.getElementById('searchInput').value.toLowerCase(); document.querySelectorAll('.list-item').forEach(i => i.style.display = i.innerText.toLowerCase().includes(v) ? 'flex' : 'none'); }}
    </script>
</body>
</html>
"""

# ================= COMMANDS =================
@app.on_message(filters.command("start"))
async def start(c, m):
    await m.reply_text(f"👑 **{BOT_OWNER_NAME} Bot Active**\n/html | /txt | /domain | /stop")

@app.on_message(filters.command("stop"))
async def stop(c, m):
    if m.from_user.id in user_mode: del user_mode[m.from_user.id]
    await m.reply_text("🛑 Process Stopped & Mode Cleared.")

@app.on_message(filters.command(["html", "txt", "domain"]))
async def mode(c, m):
    user_mode[m.from_user.id] = m.command[0]
    await m.reply_text(f"✅ Mode: **{m.command[0].upper()}**")

@app.on_message(filters.document)
async def handle(c, m):
    uid = m.from_user.id
    if uid not in user_mode: return await m.reply_text("Select Mode First!")
    path = await m.download()
    # (Processing logic same as previous responses)
    await m.reply_document(path, caption=f"Done by {BOT_OWNER_NAME}")
    os.remove(path)

app.run()
