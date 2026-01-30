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

app = Client("ultimate_login_fix", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
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

    # === NEW LOGIN SYSTEM ===
    # Default: Content Hidden, Login Screen Hidden (unless protected)
    login_html = ""
    security_script = "document.getElementById('app-wrapper').style.display = 'block';" # Default Unlocked
    
    if is_protected:
        # Show Login Screen by default, Hide App
        security_script = """
        document.getElementById('login-screen').style.display = 'flex';
        """
        login_html = f"""
        <div id="login-screen">
            <div class="login-box">
                <h3>🔒 Restricted Access</h3>
                <p>Please enter the access key to view this content.</p>
                <input type="password" id="passInput" placeholder="Enter Password">
                <button onclick="checkPass()">Unlock</button>
                <p id="errMsg" style="color:#ef4444; font-size:12px; margin-top:10px;"></p>
            </div>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {{ --bg: #f3f4f6; --card-bg: #ffffff; --primary: #2563eb; --text: #1f2937; }}
        body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding-bottom: 80px; }}
        
        #app-wrapper {{ display: none; }} /* Hidden by default for security */

        /* LOGIN SCREEN STYLES */
        #login-screen {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #f3f4f6; z-index: 5000; display: none; justify-content: center; align-items: center; }}
        .login-box {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; width: 90%; max-width: 350px; }}
        .login-box h3 {{ margin-top: 0; color: #1f2937; }}
        .login-box input {{ width: 100%; padding: 12px; margin: 15px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; outline: none; }}
        .login-box button {{ width: 100%; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }}
        .login-box button:hover {{ opacity: 0.9; }}

        /* HEADER */
        .header {{ background: #fff; padding: 15px; position: sticky; top: 0; z-index: 50; box-shadow: 0 1px 3px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: center; }}
        .header h2 {{ margin: 0; font-size: 16px; color: var(--primary); }}
        
        /* STATS */
        .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; padding: 15px; }}
        .stat-box {{ background: #fff; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #e5e7eb; cursor: pointer; }}
        .stat-num {{ font-size: 14px; font-weight: bold; display: block; }}
        .stat-label {{ font-size: 10px; color: #6b7280; }}

        /* LIST */
        .list-container {{ padding: 0 15px; }}
        .item-card {{ background: #fff; margin-bottom: 10px; border-radius: 10px; padding: 12px; display: flex; align-items: center; border: 1px solid #e5e7eb; cursor: pointer; transition: 0.2s; }}
        .item-card:hover {{ border-color: var(--primary); }}
        .item-card.active-playing {{ border: 2px solid var(--primary); background: #eff6ff; }}
        
        .card-icon {{ width: 40px; height: 40px; background: #f9fafb; border-radius: 8px; display: flex; justify-content: center; align-items: center; font-size: 18px; margin-right: 12px; }}
        .card-info {{ flex-grow: 1; min-width: 0; }}
        .card-title {{ font-size: 14px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .badge {{ font-size: 9px; padding: 2px 6px; border-radius: 4px; font-weight: bold; margin-right: 5px; background: #eee; }}
        .badge-VIDEO {{ background: #fee2e2; color: #ef4444; }}
        .badge-PDF {{ background: #dcfce7; color: #10b981; }}
        .progress-bg {{ height: 3px; background: #e5e7eb; margin-top: 6px; width: 100%; }}
        .progress-fill {{ height: 100%; background: var(--primary); width: 0%; }}
        .item-card.watched .status-icon::after {{ content: '✅'; margin-left: 10px; }}

        /* PLAYER MODAL */
        .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 1000; align-items: center; justify-content: center; flex-direction: column; transition: 0.3s; }}
        .modal-content {{ width: 100%; max-width: 900px; position: relative; transition: 0.3s; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
        
        .player-header {{ 
            display: flex; justify-content: space-between; padding: 15px; color: white;
            background: linear-gradient(to bottom, rgba(0,0,0,0.9), transparent);
            position: absolute; top: 0; width: 100%; z-index: 20; 
        }}
        #playerTitle {{ font-weight: bold; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; max-width: 70%; text-shadow: 1px 1px 3px black; }}
        .win-btn {{ cursor: pointer; font-size: 20px; color: #fff; text-shadow: 0 0 5px black; margin-left: 15px; }}

        .media-box {{ width: 100%; background: #000; display: flex; justify-content: center; align-items: center; min-height: 250px; }}
        .pdf-frame {{ width: 100%; height: 80vh; border: none; background: #fff; }}
        .view-img {{ max-width: 100%; max-height: 80vh; object-fit: contain; }}

        .controls-row {{ 
            display: flex; gap: 10px; justify-content: center; padding: 15px; 
            background: #000; flex-wrap: wrap; width: 100%;
        }}
        .c-btn {{ 
            background: #222; color: white; border: 1px solid #333; padding: 8px 16px; 
            border-radius: 8px; font-size: 13px; font-weight: 600; cursor: pointer; 
            display: flex; align-items: center; gap: 6px; 
        }}
        .c-btn:hover {{ background: #333; }}
        .c-btn.primary {{ background: var(--primary); border-color: var(--primary); }}

        /* MINIMIZED MODE */
        body.minimized .modal {{ background: transparent !important; pointer-events: none; justify-content: flex-end; align-items: flex-end; padding: 20px; }}
        body.minimized .modal-content {{ pointer-events: auto; width: 300px !important; border: 1px solid #444; border-radius: 12px; overflow: hidden; margin-bottom: 60px; }}
        body.minimized .controls-row {{ display: none; }}
        body.minimized .pdf-frame, body.minimized .view-img {{ display: none !important; }}
        body.minimized #playerTitle {{ font-size: 12px; }}
        body.minimized .player-header {{ padding: 8px; background: rgba(0,0,0,0.8); }}

        #watermark {{ position: absolute; top: 10%; right: 5%; opacity: 0.3; color: white; font-weight: bold; pointer-events: none; z-index: 20; }}
        #toast {{ position: fixed; bottom: 50px; left: 50%; transform: translateX(-50%); background: rgba(30,30,30,0.9); color: white; padding: 10px 20px; border-radius: 30px; font-size: 12px; opacity: 0; transition: 0.3s; z-index: 2000; }}
    </style>
</head>
<body>
    {login_html}

    <div id="app-wrapper">
        <div class="header">
            <div><h2>{title}</h2><small style="color:#666">{len(raw_lines)} Items</small></div>
            <div onclick="if(confirm('Reset Data?')) {{ localStorage.clear(); location.reload(); }}" style="cursor:pointer;">🗑️</div>
        </div>

        <div class="stats-grid">
            <div class="stat-box" onclick="filterList('all')"><span class="stat-num">{len(raw_lines)}</span>All</div>
            <div class="stat-box" onclick="filterList('VIDEO')" style="color:#ef4444"><span class="stat-num">{v_c}</span>Video</div>
            <div class="stat-box" onclick="filterList('PDF')" style="color:#10b981"><span class="stat-num">{p_c}</span>PDF</div>
            <div class="stat-box" onclick="filterList('IMAGE')" style="color:#d97706"><span class="stat-num">{i_c}</span>Img</div>
        </div>

        <div class="list-container" style="margin-top:10px;">
            <input type="text" id="searchInput" placeholder="🔍 Search..." onkeyup="searchList()" style="width:100%; padding:10px; border:1px solid #ddd; border-radius:8px; margin-bottom:10px;">
            <div id="playlistContainer">{items_html}</div>
        </div>

        <div id="vModal" class="modal">
            <div class="modal-content">
                <div class="player-header">
                    <div id="playerTitle">Player</div>
                    <div>
                        <span class="win-btn" onclick="toggleMinimize()" title="Minimize">📉</span>
                        <span class="win-btn" onclick="closeModal()" title="Close">✕</span>
                    </div>
                </div>

                <div class="media-box">
                    <div id="watermark">{BOT_OWNER_NAME}</div>
                    <div id="vidContainer" style="width:100%; position:relative; display:none;">
                        <video id="player" playsinline controls style="width:100%;"></video>
                    </div>
                    <iframe id="pdfFrame" class="pdf-frame" style="display:none;"></iframe>
                    <img id="imgView" class="view-img" style="display:none;">
                </div>

                <div class="controls-row" id="vidControls" style="display:none;">
                    <button class="c-btn" onclick="seek(-10)">⏪ 10s</button>
                    <button class="c-btn" onclick="seek(10)">10s ⏩</button>
                    <button class="c-btn primary" onclick="playNext()">Next ⏭️</button>
                    <button class="c-btn" onclick="downloadCurrent()">⬇️ DL</button>
                    <button class="c-btn" onclick="toggleFav(this)">🤍 Fav</button>
                </div>
            </div>
        </div>
        <div id="toast">Alert</div>
    </div>

    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        // LOGIN LOGIC
        function checkPass() {{
            const input = document.getElementById('passInput').value;
            const errMsg = document.getElementById('errMsg');
            if(input === "{SKY_PASSWORD}") {{
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('app-wrapper').style.display = 'block';
            }} else {{
                errMsg.innerText = "❌ Incorrect Password!";
            }}
        }}

        // AUTO EXECUTE IF NOT PROTECTED
        {security_script}

        const playlist = {js_playlist};
        let currentIndex = -1;
        let hls = new Hls();
        let isMinimized = false;
        
        const player = new Plyr('#player', {{
            controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'volume', 'settings', 'fullscreen'],
            settings: ['quality', 'speed']
        }});

        window.onload = () => {{
            playlist.forEach((item, i) => {{
                if(localStorage.getItem('watched_' + item.url)) {{
                    document.getElementById(`item-${{i}}`).classList.add('watched');
                    const fill = document.getElementById(`prog-${{i}}`);
                    if(fill) fill.style.width = '100%';
                }}
            }});
        }};

        function openContent(index) {{
            const item = playlist[index];
            currentIndex = index;
            
            document.querySelectorAll('.item-card').forEach(el => el.classList.remove('active-playing'));
            document.getElementById(`item-${{index}}`).classList.add('active-playing');
            
            if(isMinimized) toggleMinimize();

            const modal = document.getElementById('vModal');
            document.getElementById('playerTitle').innerText = item.name;
            modal.style.display = 'flex';
            
            document.getElementById('vidContainer').style.display = 'none';
            document.getElementById('pdfFrame').style.display = 'none';
            document.getElementById('imgView').style.display = 'none';
            document.getElementById('vidControls').style.display = 'none';

            if(item.type === 'VIDEO' || item.type === 'AUDIO') {{
                setupVideo(item);
            }} 
            else if (item.type === 'PDF') {{
                document.getElementById('pdfFrame').style.display = 'block';
                document.getElementById('pdfFrame').src = "https://docs.google.com/gview?embedded=true&url=" + encodeURIComponent(item.url);
            }} 
            else if (item.type === 'IMAGE') {{
                document.getElementById('imgView').style.display = 'block';
                document.getElementById('imgView').src = item.url;
            }} 
            else {{
                window.open(item.url, '_blank');
                closeModal();
            }}
        }}

        function setupVideo(item) {{
            const vidContainer = document.getElementById('vidContainer');
            vidContainer.style.display = 'block';
            document.getElementById('vidControls').style.display = 'flex';
            
            if (Hls.isSupported() && item.url.includes('.m3u8')) {{
                hls.loadSource(item.url); hls.attachMedia(document.getElementById('player'));
            }} else {{ document.getElementById('player').src = item.url; }}
            
            const lastTime = localStorage.getItem('prog_' + item.url);
            player.once('canplay', () => {{
                if(lastTime) player.currentTime = parseFloat(lastTime);
                player.play();
            }});
            startWatermark();
        }}

        function toggleMinimize() {{
            isMinimized = !isMinimized;
            if(isMinimized) document.body.classList.add('minimized');
            else document.body.classList.remove('minimized');
        }}

        player.on('timeupdate', () => {{
            const url = playlist[currentIndex].url;
            const pct = (player.currentTime / player.duration) * 100;
            localStorage.setItem('prog_' + url, player.currentTime);
            if(pct > 90) {{
                localStorage.setItem('watched_' + url, 'true');
                document.getElementById(`item-${{currentIndex}}`).classList.add('watched');
            }}
            const fill = document.getElementById(`prog-${{currentIndex}}`);
            if(fill && !isNaN(pct)) fill.style.width = `${{pct}}%`;
        }});

        player.on('ended', () => {{ showToast("Next..."); setTimeout(playNext, 1000); }});

        function seek(s) {{ player.currentTime += s; }}
        function playNext() {{ if(currentIndex + 1 < playlist.length) openContent(currentIndex + 1); }}
        function downloadCurrent() {{ window.open(playlist[currentIndex].url, '_blank'); }}
        function toggleFav(btn) {{
            if(btn.innerText.includes('🤍')) {{ btn.innerHTML = '❤️ Fav'; btn.style.color = '#ef4444'; }} 
            else {{ btn.innerHTML = '🤍 Fav'; btn.style.color = 'white'; }}
        }}
        
        function closeModal() {{
            player.pause(); if(hls) hls.detachMedia();
            document.getElementById('vModal').style.display = 'none';
            document.getElementById('pdfFrame').src = "";
            document.body.classList.remove('minimized');
            isMinimized = false;
        }}

        function filterList(type) {{
            document.querySelectorAll('.item-card').forEach(el => {{
                el.style.display = (type === 'all' || el.getAttribute('data-type') === type) ? 'flex' : 'none';
            }});
        }}
        function searchList() {{
            const val = document.getElementById('searchInput').value.toLowerCase();
            document.querySelectorAll('.item-card').forEach(el => {{
                el.style.display = el.innerText.toLowerCase().includes(val) ? 'flex' : 'none';
            }});
        }}
        function showToast(msg) {{
            const t = document.getElementById('toast'); t.innerText = msg; t.style.opacity = '1';
            setTimeout(() => t.style.opacity = '0', 2000);
        }}
        function startWatermark() {{
            const w = document.getElementById('watermark');
            setInterval(() => {{ w.style.top = Math.random()*80+10+"%"; w.style.left = Math.random()*80+10+"%"; }}, 5000);
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
        return await m.reply_text(f"🛠️ **Login Page Fixed**\n\n/html - Normal\n/sky - Login Protected \n/txt - Links")
    if cmd == "stop":
        user_mode.pop(m.from_user.id, None)
        return await m.reply_text("🛑 Reset.")
    user_mode[m.from_user.id] = cmd
    await m.reply_text(f"✅ Mode: {cmd.upper()}\nFile bhejo!")

@app.on_message(filters.document)
async def process_file(c, m):
    uid = m.from_user.id
    mode = user_mode.get(uid)
    if not mode: return await m.reply_text("⚠️ Mode Select Karo!")
    
    msg = await m.reply_text("🔄 Processing...")
    path = await m.download()
    with open(path, "r", encoding="utf-8", errors="ignore") as f: content = f.read()
    
    out_path = path + ".html"
    cap = ""

    if mode in ["html", "sky"]:
        html_data = generate_html(m.document.file_name, content, is_protected=(mode=="sky"))
        out_path = path.rsplit('.', 1)[0] + "_FixedLogin.html"
        with open(out_path, "w", encoding="utf-8") as f: f.write(html_data)
        cap = "✅ **Blank Screen Fixed**\nUse Password: 7989"
    
    elif mode == "txt":
        links = re.findall(r"(https?://[^\s\n]+)", content)
        out_path = path.rsplit('.', 1)[0] + "_links.txt"
        with open(out_path, "w", encoding="utf-8") as f: f.write("\n".join(links))
        cap = f"📄 Extracted {len(links)} Links"

    await m.reply_document(out_path, caption=cap)
    await msg.delete()
    if os.path.exists(path): os.remove(path)
    if os.path.exists(out_path): os.remove(out_path)

print("✅ Login Fix Bot Started...")
app.run()
