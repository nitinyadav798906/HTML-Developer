import os
import re
import json
from datetime import datetime
from pyrogram import Client, filters

# ================= CONFIGURATION =================
BOT_OWNER_NAME = "Sachin & Nitin"
API_ID = 12475131
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"
SKY_PASSWORD = "7989"

OLD_DOMAINS = ["https://apps-s3-jw-prod.utkarshapp.com/", "https://apps-s3-prod.utkarshapp.com/", "https://apps-s3-video-dist.utkarshapp.com/"]
NEW_DOMAIN = "https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/"

app = Client("ultimate_gesture_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_mode = {}

def fix_domain(url):
    low = url.lower()
    if any(x in low for x in [".m3u8", ".mpd", ".mp4", "/m3u8"]):
        for d in OLD_DOMAINS:
            if d in url: return url.replace(d, NEW_DOMAIN)
    return url

# ================= HTML GENERATOR =================
def generate_html(file_name, content, is_protected=False):
    title = os.path.splitext(file_name)[0]
    raw_lines = re.findall(r"([^:\n]+):?\s*(https?://[^\s\n]+)", content)
    v_c = p_c = a_c = i_c = 0
    items_html = ""
    playlist_data = []

    for idx, (name, url) in enumerate(raw_lines):
        url = fix_domain(url.strip())
        name = name.strip()
        low_u = url.lower()
        if any(x in low_u for x in [".m3u8", ".mpd", ".mp4"]): t = "VIDEO"; v_c += 1; icon = "🎥"
        elif ".pdf" in low_u: t = "PDF"; p_c += 1; icon = "📑"
        elif any(x in low_u for x in [".jpg", ".jpeg", ".png", ".webp"]): t = "IMAGE"; i_c += 1; icon = "🖼️"
        elif any(x in low_u for x in [".m4a", ".mp3"]): t = "AUDIO"; a_c += 1; icon = "🎧"
        else: t = "OTHER"; icon = "📂"
        playlist_data.append({"url": url, "name": name, "type": t})

        items_html += f'''
        <div class="card item-card" id="item-{idx}" data-type="{t}" onclick="openContent({idx})">
            <div class="card-icon">{icon}</div>
            <div class="card-info">
                <div class="card-title">{name}</div>
                <div class="card-meta">
                    <span class="badge badge-{t}">{t}</span>
                    <span id="dur-{idx}" class="duration-txt"></span>
                </div>
                <div class="progress-bg"><div class="progress-fill" id="prog-{idx}" style="width: 0%"></div></div>
            </div>
            <div class="status-icon" id="status-{idx}"></div>
        </div>'''

    js_playlist = json.dumps(playlist_data)
    login_html = ""
    security_script = "document.getElementById('app-wrapper').style.display = 'block';" 
    
    if is_protected:
        security_script = "document.getElementById('login-screen').style.display = 'flex';"
        login_html = f"""
        <div id="login-screen">
            <div class="lamp-container" onclick="toggleLampUI()">
                <div class="lamp"><div class="lamp-shade"></div><div class="lamp-stick"></div><div class="lamp-base"></div><div class="pull-chain"></div></div>
                <div class="light-glow"></div>
            </div>
            <div class="login-box" id="loginBox">
                <h2 style="color:var(--primary)">🔒 Secured File</h2>
                <p>Created by {BOT_OWNER_NAME}</p>
                <input type="password" id="passInput" placeholder="Enter Access Key">
                <button onclick="checkPass()">Unlock Dashboard</button>
                <p id="errMsg" style="color:red; font-size:12px; margin-top:10px;"></p>
            </div>
        </div>"""

    return f"""
<!DOCTYPE html>
<html lang="en" data-theme="blue">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {{ --bg: #f3f4f6; --card-bg: #fff; --text: #1f2937; --border: #e5e7eb; }}
        [data-theme="blue"] {{ --primary: #2563eb; --light: #eff6ff; }}
        [data-theme="dark"] {{ --primary: #475569; --light: #f8fafc; --bg: #0f172a; --card-bg: #1e293b; --text: #f1f5f9; --border: #334155; }}
        #login-screen {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #121417; z-index: 5000; display: none; justify-content: center; align-items: center; gap:40px; flex-wrap:wrap; transition: 0.6s; }}
        .lamp-container {{ cursor: pointer; position: relative; }}
        .lamp-shade {{ width: 100px; height: 50px; background: #fff; border-radius: 50px 50px 0 0; position: relative; z-index: 2; }}
        .lamp-stick {{ width: 6px; height: 110px; background: #fff; margin: 0 auto; }}
        .lamp-base {{ width: 75px; height: 12px; background: #fff; border-radius: 10px 10px 0 0; margin: 0 auto; }}
        .light-glow {{ position: absolute; top: 20px; left: 50%; transform: translateX(-50%); width: 280px; height: 280px; background: radial-gradient(circle, rgba(255,255,200,0.3) 0%, transparent 70%); opacity: 0; transition: 0.5s; pointer-events: none; }}
        .login-box {{ background: rgba(255,255,255,0.05); padding: 30px; border-radius: 16px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); text-align: center; width: 90%; max-width: 320px; opacity: 0.2; transition: 0.5s; color:white; }}
        .login-box.active {{ opacity: 1; }}
        * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
        body {{ font-family: 'Poppins', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding-bottom: 80px; transition: 0.3s; }}
        #app-wrapper {{ display: none; }} 
        .header {{ background: var(--card-bg); padding: 15px; position: sticky; top: 0; z-index: 50; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-bottom: 1px solid var(--border); }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; padding: 15px; }}
        .stat-box {{ background: var(--card-bg); padding: 10px; border-radius: 12px; text-align: center; border: 1px solid var(--border); cursor: pointer; }}
        .item-card {{ background: var(--card-bg); margin-bottom: 10px; border-radius: 12px; padding: 12px; display: flex; align-items: center; border: 1px solid var(--border); cursor: pointer; }}
        .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 2000; align-items: center; justify-content: center; flex-direction: column; }}
        .modal-content {{ width: 100%; max-width: 900px; position: relative; background: #000; display: flex; flex-direction: column; }}
        .player-header {{ display: flex; justify-content: space-between; padding: 12px 15px; color: white; background: rgba(0,0,0,0.9); z-index: 20; cursor: move; }}
        .controls-row {{ display: flex; gap: 10px; justify-content: center; padding: 15px; background: #111; flex-wrap: wrap; width: 100%; }}
        .c-btn {{ background: #333; color: white; border: 1px solid #444; padding: 8px 16px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer; }}
        #volIndicator {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; color: white; display: none; z-index: 30; }}
        #toast {{ position: fixed; bottom: 50px; left: 50%; transform: translateX(-50%); background: #333; color: white; padding: 8px 16px; border-radius: 20px; font-size: 12px; opacity: 0; transition: 0.3s; z-index: 3000; }}
        body.minimized .modal-content {{ width: 300px !important; position: fixed; bottom: 80px; right: 20px; border-radius: 12px; overflow: hidden; }}
    </style>
</head>
<body>
    {login_html}
    <div id="app-wrapper">
        <div class="header"> <h2 style="margin:0; font-size:16px;">{title}</h2> </div>
        <div class="stats-grid">
            <div class="stat-box" onclick="filterList('all')"><span>{len(raw_lines)}</span> All</div>
            <div class="stat-box" onclick="filterList('FAV')" style="color:#ef4444;"><span id="favCount">0</span> Fav ❤️</div>
            <div class="stat-box" onclick="filterList('VIDEO')"><span>{v_c}</span> Video</div>
        </div>
        <div class="list-container" style="padding:15px;"> <div id="playlistContainer">{items_html}</div> </div>

        <div id="vModal" class="modal">
            <div class="modal-content" id="modalContent">
                <div class="player-header" id="dragHandle">
                    <span id="playerTitle">Player</span>
                    <div><span onclick="toggleMinimize()" style="cursor:pointer; margin-right:15px;">📉</span><span onclick="closeModal()" style="cursor:pointer;">✕</span></div>
                </div>
                <div id="mediaBox" style="position:relative; background:#000;">
                    <div id="volIndicator">Vol: 100%</div>
                    <video id="player" playsinline controls style="width:100%; display:none;"></video>
                    <iframe id="pdfFrame" style="display:none; width:100%; height:80vh; border:none;"></iframe>
                </div>
                <div class="controls-row" id="vidControls" style="display:none;">
                    <button class="c-btn" onclick="player.currentTime -= 10">⏪ 10s</button>
                    <button class="c-btn" onclick="player.currentTime += 10">10s ⏩</button>
                    <button class="c-btn" style="background:var(--primary)" onclick="playNext()">Next ⏭️</button>
                    <button class="c-btn" id="favBtn" onclick="toggleFav()">❤️ Favorite</button>
                </div>
            </div>
        </div>
        <div id="toast"></div>
    </div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        const playlist = {js_playlist}; let currentIndex = -1; let isMinimized = false;
        const player = new Plyr('#player', {{ quality: {{ default: 1080, options: [4320, 2160, 1080, 720, 480] }} }});

        function toggleLampUI() {{
            const screen = document.getElementById('login-screen');
            const box = document.getElementById('loginBox');
            gsap.to(screen, {{ backgroundColor: "#1c1f24", duration: 0.6 }});
            box.classList.add('active'); document.querySelector('.light-glow').style.opacity = "1";
        }}

        function checkPass() {{
            if(document.getElementById('passInput').value === "{SKY_PASSWORD}") {{
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('app-wrapper').style.display = 'block';
            }} else alert("Incorrect Password");
        }}
        {security_script}

        function openContent(idx) {{
            currentIndex = idx; const item = playlist[idx]; document.getElementById('vModal').style.display = 'flex';
            document.getElementById('playerTitle').innerText = item.name;
            const vid = document.getElementById('player'); const pdf = document.getElementById('pdfFrame');
            vid.style.display = pdf.style.display = 'none'; document.getElementById('vidControls').style.display = 'none';
            if(item.type === 'VIDEO') {{
                vid.style.display = 'block'; document.getElementById('vidControls').style.display = 'flex';
                if(item.url.includes('.m3u8')) {{ const hls = new Hls(); hls.loadSource(item.url); hls.attachMedia(vid); }}
                else vid.src = item.url; player.play(); updateFavBtn();
            }} else if(item.type === 'PDF') {{ pdf.style.display = 'block'; pdf.src = "https://docs.google.com/gview?embedded=true&url=" + encodeURIComponent(item.url); }}
        }}

        function toggleFav() {{
            const url = playlist[currentIndex].url;
            if(localStorage.getItem('fav_' + url)) localStorage.removeItem('fav_' + url);
            else localStorage.setItem('fav_' + url, 'true');
            updateFavBtn(); updateFavCount(); showToast("Fav Updated");
        }}

        function updateFavBtn() {{
            const url = playlist[currentIndex].url;
            document.getElementById('favBtn').style.color = localStorage.getItem('fav_' + url) ? "#ef4444" : "white";
        }}

        function updateFavCount() {{
            let c = 0; playlist.forEach(i => {{ if(localStorage.getItem('fav_' + i.url)) c++; }});
            document.getElementById('favCount').innerText = c;
        }}

        function toggleMinimize() {{ isMinimized = !isMinimized; document.body.classList.toggle('minimized', isMinimized); }}
        function closeModal() {{ player.pause(); document.getElementById('vModal').style.display = 'none'; }}
        function showToast(m) {{ const t = document.getElementById('toast'); t.innerText = m; t.style.opacity = '1'; setTimeout(() => t.style.opacity = '0', 2000); }}
        
        // Volume Gesture
        let touchStartY = 0; document.getElementById('mediaBox').addEventListener('touchstart', e => touchStartY = e.touches[0].clientY);
        document.getElementById('mediaBox').addEventListener('touchmove', e => {{
            if(e.touches[0].clientX > window.innerWidth / 2) {{
                e.preventDefault(); let delta = (touchStartY - e.touches[0].clientY) / 200;
                player.volume = Math.min(1, Math.max(0, player.volume + delta));
                const vInd = document.getElementById('volIndicator'); vInd.style.display = 'block'; vInd.innerText = 'Vol: ' + Math.round(player.volume * 100) + '%';
                clearTimeout(window.vTimer); window.vTimer = setTimeout(() => vInd.style.display='none', 1000);
            }}
        }});
        updateFavCount();
    </script>
</body>
</html>
"""

# ================= TELEGRAM HANDLER (FIXED COMMANDS) =================
@app.on_message(filters.command(["start", "stop", "html", "sky", "txt"]))
async def handle_cmds(c, m):
    cmd = m.command[0]
    
    if cmd == "start":
        return await m.reply_text(f"🔥 Pro Player Bot Started\n\n/html - Normal Dashboard\n/sky - Secured Lamp UI\n/txt - Link Extractor\n/stop - Reset Mode")
        
    if cmd == "stop":
        user_mode.pop(m.from_user.id, None)
        return await m.reply_text("🛑 Mode Reset Success!")

    # Set Mode
    user_mode[m.from_user.id] = cmd
    await m.reply_text(f"✅ Mode: {cmd.upper()} Selected\nAb apni .txt ya .html file bhejein!")

@app.on_message(filters.document)
async def process_file(c, m):
    uid = m.from_user.id
    mode = user_mode.get(uid)
    
    if not mode:
        return await m.reply_text("⚠️ Pehle koi command select karein (jaise /html ya /sky)!")

    msg = await m.reply_text("🔄 Processing...")
    path = await m.download()
    
    # Check File Content
    with open(path, "r", encoding="utf-8", errors="ignore") as f: 
        content = f.read()

    # Mode Logic
    if mode in ["html", "sky"]:
        html_data = generate_html(m.document.file_name, content, is_protected=(mode=="sky"))
        out_path = path.rsplit('.', 1)[0] + "_Dashboard.html"
        with open(out_path, "w", encoding="utf-8") as f: 
            f.write(html_data)
        await m.reply_document(out_path, caption="🔥 Pro Player Ready!")
        
    elif mode == "txt":
        links = re.findall(r"(https?://[^\s\n]+)", content)
        out_path = path.rsplit('.', 1)[0] + "_links.txt"
        with open(out_path, "w", encoding="utf-8") as f: 
            f.write("\n".join(links))
        await m.reply_document(out_path, caption=f"📄 Extracted {len(links)} Links")

    await msg.delete()
    if os.path.exists(path): os.remove(path)
    if 'out_path' in locals() and os.path.exists(out_path): os.remove(out_path)

print("🔥 Bot Started with Correct Commands...")
app.run()
