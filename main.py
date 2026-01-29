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

app = Client("dashboard_final_pro", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_mode = {}

def fix_domain(url):
    low = url.lower()
    if any(x in low for x in [".m3u8", ".mpd", ".mp4", "/m3u8", "/mpd"]):
        for d in OLD_DOMAINS:
            if d in url: return url.replace(d, NEW_DOMAIN)
    return url

# ================= HTML GENERATOR =================
def generate_html(file_name, content):
    title = os.path.splitext(file_name)[0]
    now_date = datetime.now().strftime("%d %b %Y")
    now_time = datetime.now().strftime("%I:%M:%S %p")
    
    # Accurate Link & Name Extraction
    raw_lines = re.findall(r"([^:\n]+):?\s*(https?://[^\s\n]+)", content)
    if not raw_lines: 
        raw_lines = [(f"Item {i+1}", l) for i, l in enumerate(re.findall(r"https?://[^\s\n]+", content))]

    v_c = p_c = a_c = o_c = 0
    items_html = ""

    for name, url in raw_lines:
        url = fix_domain(url.strip())
        low_u = url.lower()
        
        # Proper Extension Logic
        if any(x in low_u for x in [".m3u8", ".mpd", ".mp4"]): 
            t = "VIDEO"; v_c += 1; icon = "📽️"
        elif ".pdf" in low_u: 
            t = "PDF"; p_c += 1; icon = "📄"
        elif any(x in low_u for x in [".m4a", ".mp3", ".wav"]): 
            t = "AUDIO"; a_c += 1; icon = "🎵"
        else: 
            t = "OTHER"; o_c += 1; icon = "📁"

        items_html += f'''
        <div class="list-item" data-type="{t}" onclick="openModal('{url}', '{name.strip()}', '{t}')">
            <div class="item-icon-bg">{icon}</div>
            <div class="item-details">
                <div class="item-title">{name.strip()}</div>
                <div class="item-meta">Type: {t} | Ext: {url.split('.')[-1].split('?')[0].upper()}</div>
            </div>
        </div>'''

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
        .header {{ background: var(--card); padding: 20px; text-align: center; border-bottom: 1px solid #eee; }}
        .dashboard {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding: 15px; }}
        .card {{ background: var(--card); padding: 15px; border-radius: 12px; border-left: 5px solid var(--purple); cursor: pointer; border: 1px solid #eee; }}
        .card:active {{ transform: scale(0.95); }}
        .list-item {{ background: var(--card); margin: 8px 15px; padding: 12px; border-radius: 10px; display: flex; align-items: center; cursor: pointer; border: 1px solid #eee; }}
        .modal {{ display: none; position: fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.9); z-index:999; align-items:center; justify-content:center; }}
        .m-body {{ background: var(--card); width: 95%; max-width: 600px; border-radius: 12px; overflow: hidden; }}
    </style>
</head>
<body>
    <div id="vModal" class="modal">
        <div class="m-body">
            <div style="padding:10px; display:flex; justify-content:space-between; border-bottom:1px solid #eee;">
                <b id="mT" style="font-size:14px;"></b><span onclick="closeModal()" style="cursor:pointer; font-size:24px;">&times;</span>
            </div>
            <video id="player" playsinline controls></video>
        </div>
    </div>
    <div class="header">
        <h1 style="font-size:18px; color:var(--purple);">{title}</h1>
        <div style="font-size:10px; color:#777;">📅 {now_date} | 🕒 {now_time} | 🌙 <span onclick="document.body.classList.toggle('dark-mode')" style="cursor:pointer; color:var(--purple); font-weight:bold;">DARK MODE</span></div>
    </div>
    <div class="dashboard">
        <div class="card" onclick="runFilter('all')"><b>{len(raw_lines)}</b><br><small>ALL ITEMS</small></div>
        <div class="card" onclick="runFilter('VIDEO')" style="border-left-color:#e74c3c;"><b style="color:#e74c3c;">{v_c}</b><br><small>VIDEOS</small></div>
        <div class="card" onclick="runFilter('PDF')" style="border-left-color:#2ecc71;"><b style="color:#2ecc71;">{p_c}</b><br><small>PDFS</small></div>
        <div class="card" onclick="runFilter('AUDIO')" style="border-left-color:#f1c40f;"><b style="color:#f1c40f;">{a_c}</b><br><small>AUDIO</small></div>
    </div>
    <div style="padding: 0 15px;"><input type="text" id="srIn" placeholder="Search by title..." onkeyup="search()" style="width:100%; padding:10px; border-radius:8px; border:1px solid #eee; outline:none;"></div>
    <div id="itemList">{items_html}</div>
    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        const player = new Plyr('#player', {{ settings: ['quality', 'speed'] }});
        let hls = new Hls();
        function runFilter(t) {{
            document.querySelectorAll('.list-item').forEach(i => i.style.display = (t === 'all' || i.getAttribute('data-type') === t) ? 'flex' : 'none');
        }}
        function search() {{
            let v = document.getElementById('srIn').value.toLowerCase();
            document.querySelectorAll('.list-item').forEach(i => i.style.display = i.innerText.toLowerCase().includes(v) ? 'flex' : 'none');
        }}
        function openModal(url, name, type) {{
            if(type === 'VIDEO') {{
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
            }} else {{ window.open(url); }}
        }}
        function closeModal() {{ player.pause(); hls.detachMedia(); document.getElementById('vModal').style.display = 'none'; }}
    </script>
</body>
</html>
"""

# ================= COMMANDS =================
@app.on_message(filters.command(["start", "stop", "html", "txt", "domain"]))
async def commands(c, m):
    cmd = m.command[0]
    if cmd == "stop":
        user_mode.pop(m.from_user.id, None)
        return await m.reply_text("🛑 Process Stopped.")
    if cmd in ["html", "txt", "domain"]:
        user_mode[m.from_user.id] = cmd
        return await m.reply_text(f"✅ Mode: **{cmd.upper()}**")
    await m.reply_text("👑 **Professional Dashboard Bot**\n/html | /txt | /domain | /stop")

@app.on_message(filters.document)
async def process_file(c, m):
    uid = m.from_user.id
    mode = user_mode.get(uid)
    if not mode: return await m.reply_text("❌ First Select Mode! (/html, /txt)")
    
    path = await m.download()
    with open(path, "r", encoding="utf-8") as f: content = f.read()
    
    if mode == "html":
        # Force HTML generation
        out = path.split('.')[0] + ".html"
        with open(out, "w", encoding="utf-8") as f: f.write(generate_html(m.document.file_name, content))
        await m.reply_document(out, caption=f"✨ Dashboard by {BOT_OWNER_NAME}")
    
    elif mode == "txt":
        # Extract links only for TXT
        links = re.findall(r"(https?://[^\s\n]+)", content)
        out = path.split('.')[0] + ".txt"
        with open(out, "w", encoding="utf-8") as f: f.write("\n".join(links))
        await m.reply_document(out, caption="📄 Links Extracted")
        
    os.remove(path)
    if os.path.exists(out): os.remove(out)

app.run()
