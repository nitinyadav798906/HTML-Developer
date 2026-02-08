import os
import re
import json
import random
from datetime import datetime
from pyrogram import Client, filters

# ================= CONFIGURATION =================
BOT_OWNER_NAME = "Sachin & Nitin"
TELEGRAM_LINK = "https://t.me/Raftaarss_don"  # Telegram Channel Link
API_ID = 12345678  # Apna API ID dalein
API_HASH = "your_api_hash"  # Apna API Hash dalein
BOT_TOKEN = "your_bot_token"  # Apna Bot Token dalein
SKY_PASSWORD = "7989"

app = Client("ultimate_final_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_mode = {}

# ================= HTML GENERATOR =================
def generate_html(file_name, content, is_protected=False):
    title = os.path.splitext(file_name)[0]
    raw_lines = re.findall(r"([^:\n]+):?\s*(https?://[^\s\n]+)", content)
    
    v_c = p_c = a_c = i_c = 0
    items_html = ""
    playlist_data = []

    # 4K Nature Wallpapers
    nature_bgs = [
        "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?q=80&w=2074&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?q=80&w=2071&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1501854140884-074cf2b2c3af?q=80&w=2076&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e?q=80&w=2074&auto=format&fit=crop"
    ]

    for idx, (name, url) in enumerate(raw_lines):
        name = name.strip()
        url = url.strip()
        low_u = url.lower()
        
        # Category Logic
        if any(x in low_u for x in [".m3u8", ".mpd", ".mp4", ".mkv"]): t = "VIDEO"; v_c += 1; icon = "🎥"
        elif ".pdf" in low_u: t = "PDF"; p_c += 1; icon = "📑"
        elif any(x in low_u for x in [".jpg", ".jpeg", ".png", ".webp"]): t = "IMAGE"; i_c += 1; icon = "🖼️"
        elif any(x in low_u for x in [".m4a", ".mp3", ".wav"]): t = "AUDIO"; a_c += 1; icon = "🎧"
        else: t = "OTHER"; icon = "📂"

        bg_img = random.choice(nature_bgs)
        playlist_data.append({"url": url, "name": name, "type": t, "bg": bg_img})

        items_html += f'''
        <div class="card item-card" id="item-{idx}" data-type="{t}" onclick="openCinema({idx})">
            <div class="card-icon">{icon}</div>
            <div class="card-info">
                <div class="card-title">{name}</div>
                <div class="card-meta">
                    <span class="badge badge-{t}">{t}</span>
                </div>
            </div>
            <div class="status-icon" id="status-{idx}"></div>
        </div>'''

    js_playlist = json.dumps(playlist_data)

    # LOGIN LOGIC
    login_html = ""
    security_script = "document.getElementById('app-wrapper').style.display = 'block';" 
    if is_protected:
        security_script = "document.getElementById('login-screen').style.display = 'flex';"
        login_html = f"""
        <div id="login-screen">
            <div class="login-box">
                <h3 style="color:#3b82f6; margin-top:0;">🔒 Secured Access</h3>
                <input type="password" id="passInput" placeholder="Enter Password">
                <button onclick="checkPass()">Unlock</button>
                <p id="errMsg" style="color:red;font-size:12px; margin-top:10px;"></p>
            </div>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    
    <style>
        :root {{ 
            --bg: #0f172a; --card-bg: #1e293b; --text: #f8fafc; --primary: #3b82f6; --border: #334155; 
            --red-glow: 0 0 25px #ff0000; 
        }}
        [data-theme="light"] {{
            --bg: #f3f4f6; --card-bg: #ffffff; --text: #1f2937; --primary: #2563eb; --border: #e5e7eb;
            --red-glow: 0 0 15px #ff0000;
        }}

        body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding-bottom: 80px; transition: 0.3s; }}
        * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
        
        #app-wrapper {{ display: none; }} 

        /* LOGIN */
        #login-screen {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: var(--bg); z-index: 9999; display: none; justify-content: center; align-items: center; }}
        .login-box {{ background: var(--card-bg); padding: 30px; border-radius: 12px; text-align: center; border: 1px solid var(--border); width: 85%; max-width: 320px; }}
        .login-box input {{ width: 100%; padding: 12px; margin: 10px 0; border-radius: 6px; border: 1px solid var(--border); background: var(--bg); color: var(--text); outline: none; }}
        .login-box button {{ width: 100%; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }}

        /* HEADER */
        .header {{ 
            background: var(--card-bg); padding: 15px; position: sticky; top: 0; z-index: 50; 
            border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center;
        }}
        .tg-btn {{ 
            background: #229ED9; color: white; padding: 6px 14px; border-radius: 20px; 
            text-decoration: none; font-size: 12px; font-weight: bold; display: flex; align-items: center; gap: 5px; 
        }}
        .theme-toggle {{ cursor: pointer; font-size: 20px; margin-left: 10px; }}

        /* FILTERS */
        .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; padding: 10px 15px; }}
        .stat-box {{ 
            background: var(--card-bg); padding: 10px; border-radius: 8px; text-align: center; 
            border: 1px solid var(--border); cursor: pointer; transition: 0.2s; 
        }}
        .stat-num {{ font-size: 14px; font-weight: bold; display: block; }}
        .stat-label {{ font-size: 10px; opacity: 0.7; text-transform: uppercase; }}

        /* LIST */
        .list-container {{ padding: 0 15px; }}
        .item-card {{ 
            background: var(--card-bg); margin-bottom: 8px; border-radius: 10px; padding: 12px; 
            display: flex; align-items: center; border: 1px solid var(--border); cursor: pointer; 
        }}
        .item-card.active-playing {{ border: 1px solid var(--primary); background: rgba(37,99,235,0.1); }}
        .card-icon {{ width: 40px; height: 40px; background: rgba(100,100,100,0.1); border-radius: 8px; display: flex; justify-content: center; align-items: center; margin-right: 12px; font-size: 18px; }}
        .card-info {{ flex-grow: 1; min-width: 0; }}
        .card-title {{ font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .badge {{ font-size: 9px; padding: 2px 6px; border-radius: 4px; font-weight: bold; margin-right: 5px; background: rgba(100,100,100,0.1); }}
        .badge-VIDEO {{ color: #ef4444; }} .badge-PDF {{ color: #10b981; }} .badge-AUDIO {{ color: #3b82f6; }}
        .item-card.watched .status-icon::after {{ content: '✅'; margin-left: 10px; }}

        /* === 1. NATURE CINEMA POPUP === */
        .cinema-modal {{
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #000; z-index: 3000;
        }}
        .bg-layer {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-size: cover; background-position: center; opacity: 0.7;
            mask-image: linear-gradient(to bottom, black 30%, transparent 100%);
            -webkit-mask-image: linear-gradient(to bottom, black 30%, transparent 100%);
        }}
        .cinema-content {{
            position: absolute; bottom: 0; width: 100%; padding: 25px;
            background: linear-gradient(to top, #000 10%, transparent);
            display: flex; flex-direction: column; gap: 15px; color: white;
        }}
        .c-title {{ font-size: 24px; font-weight: 800; margin: 0; text-shadow: 0 2px 10px black; }}
        .action-btn {{
            width: 100%; padding: 14px; border-radius: 8px; font-size: 15px; font-weight: 700;
            border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;
        }}
        .btn-play {{ background: white; color: black; }}
        .btn-fav {{ background: rgba(255,255,255,0.15); color: white; border: 1px solid rgba(255,255,255,0.3); backdrop-filter: blur(5px); }}

        /* === 2. RED BAR PLAYER UI === */
        .player-modal {{
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #000; z-index: 4000; flex-direction: column;
        }}
        
        /* The Red Gesture Bar */
        .red-bar-container {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%; 
            pointer-events: none; z-index: 50; display: flex; justify-content: center; align-items: center;
        }}
        .red-bar {{
            width: 8px; height: 0%; background: #ff0000;
            box-shadow: var(--red-glow); opacity: 0; transition: height 0.1s, opacity 0.2s;
            border-radius: 10px;
        }}
        .gesture-val {{
            position: absolute; color: white; font-weight: bold; font-size: 24px; 
            text-shadow: 0 2px 10px black; opacity: 0; top: 40%;
        }}

        /* Controls */
        .player-header {{ 
            position: absolute; top: 0; width: 100%; padding: 15px; z-index: 60;
            background: linear-gradient(to bottom, rgba(0,0,0,0.8), transparent);
            display: flex; justify-content: space-between; color: white;
        }}
        .center-controls {{
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            display: flex; gap: 40px; align-items: center; z-index: 60;
        }}
        .c-icon {{ font-size: 40px; color: white; opacity: 0.9; cursor: pointer; text-shadow: 0 2px 5px black; }}
        
        .video-box {{ width: 100%; flex-grow: 1; display: flex; justify-content: center; align-items: center; position: relative; }}
        
        .bottom-controls {{
            background: #0f0f0f; padding: 15px; display: flex; justify-content: center; gap: 10px;
            border-top: 1px solid #333; z-index: 60; flex-wrap: wrap;
        }}
        .b-btn {{
            background: #222; color: white; border: none; padding: 10px 16px; border-radius: 8px;
            font-size: 13px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 6px;
        }}
        .b-btn-blue {{ background: #2563eb; }}
        
        .lock-icon {{ position: absolute; bottom: 30px; right: 30px; color: white; font-size: 22px; z-index: 60; padding: 12px; background: rgba(0,0,0,0.5); border-radius: 50%; cursor: pointer; }}

        .pdf-frame {{ width: 100%; height: 100%; border: none; background: white; }}
        .img-view {{ width: 100%; height: 100%; object-fit: contain; }}
        
        .footer-credit {{ text-align: center; font-size: 11px; color: #666; margin-top: 20px; opacity: 0.7; }}
    </style>
</head>
<body>
    {login_html}

    <div id="app-wrapper">
        <div class="header">
            <div>
                <h3 style="margin:0; color:var(--primary); font-size:16px;">{title}</h3>
                <small style="font-size:10px; color:#888;">{len(raw_lines)} Files</small>
            </div>
            <div style="display:flex; align-items:center; gap:10px;">
                <a href="{TELEGRAM_LINK}" target="_blank" class="tg-btn">✈ Join Telegram</a>
                <span class="theme-toggle" onclick="toggleTheme()">🌓</span>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-box" onclick="filterList('all')"><span class="stat-num">{len(raw_lines)}</span>All</div>
            <div class="stat-box" onclick="filterList('VIDEO')" style="color:#ef4444"><span class="stat-num">{v_c}</span>Video</div>
            <div class="stat-box" onclick="filterList('PDF')" style="color:#10b981"><span class="stat-num">{p_c}</span>PDF</div>
            <div class="stat-box" onclick="filterList('IMAGE')" style="color:#d97706"><span class="stat-num">{i_c}</span>Img</div>
        </div>

        <div class="list-container">
            <input type="text" id="searchInput" placeholder="Search..." onkeyup="searchList()" style="width:100%; padding:12px; border-radius:8px; border:1px solid var(--border); background:var(--card-bg); color:var(--text); margin-bottom:15px; outline:none;">
            <div id="playlistContainer">{items_html}</div>
            <div class="footer-credit">Created by {BOT_OWNER_NAME}</div>
        </div>
    </div>

    <div id="cinemaModal" class="cinema-modal">
        <div onclick="closeCinema()" style="position:absolute; top:20px; left:20px; color:white; font-size:24px; z-index:50; cursor:pointer;">✕</div>
        <div class="bg-layer" id="bgLayer"></div>
        <div class="cinema-content">
            <div style="flex-grow:1;"></div>
            <h1 class="c-title" id="mTitle">Title Here</h1>
            <div style="display:flex; gap:10px; font-size:12px; opacity:0.8;">
                <span style="background:rgba(255,255,255,0.2); padding:2px 6px; border-radius:4px;">HD</span>
                <span>2025</span>
                <span id="mType">Video</span>
            </div>
            
            <button class="action-btn btn-play" onclick="startPlayer()">▶ Watch Now</button>
            <button class="action-btn btn-fav" onclick="toggleFavPopup()" id="favBtn">❤️ Add to Favorites</button>
        </div>
    </div>

    <div id="playerModal" class="player-modal">
        <div class="red-bar-container">
            <div class="red-bar" id="redBar"></div>
            <div class="gesture-val" id="gestureVal">50%</div>
        </div>

        <div class="player-header">
            <span id="pTitle" style="max-width:80%; overflow:hidden; white-space:nowrap; text-overflow:ellipsis;">Player</span>
            <span onclick="closePlayer()" style="font-size:24px; cursor:pointer;">✕</span>
        </div>

        <div class="video-box" id="gestureArea">
            <div class="center-controls" id="centerControls">
                <div class="c-icon" onclick="seek(-10)">⏮</div>
                <div class="c-icon" onclick="togglePlay()" style="font-size:60px;">▶</div>
                <div class="c-icon" onclick="seek(10)">⏭</div>
            </div>
            
            <div class="lock-icon" onclick="toggleLock()">🔓</div>

            <video id="player" playsinline controls style="width:100%; max-height:100%;"></video>
            <iframe id="pdfFrame" class="pdf-frame" style="display:none;"></iframe>
            <img id="imgView" class="img-view" style="display:none;">
        </div>

        <div class="bottom-controls" id="extControls">
            <button class="b-btn" onclick="seek(-10)">⏪ 10s</button>
            <button class="b-btn" onclick="seek(10)">10s ⏩</button>
            <button class="b-btn b-btn-blue" onclick="playNext()">Next ⏭</button>
            <button class="b-btn" onclick="downloadCurrent()">⬇ DL</button>
            <button class="b-btn" onclick="toggleFavPlayer()" id="pFavBtn">❤️ Fav</button>
        </div>
    </div>

    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        // THEME LOGIC
        function toggleTheme() {{
            const html = document.documentElement;
            if(html.getAttribute('data-theme') === 'dark') {{
                html.setAttribute('data-theme', 'light');
            }} else {{
                html.setAttribute('data-theme', 'dark');
            }}
        }}

        function checkPass() {{
            if(document.getElementById('passInput').value === "{SKY_PASSWORD}") {{
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('app-wrapper').style.display = 'block';
            }} else document.getElementById('errMsg').innerText = "Incorrect!";
        }}
        {security_script}

        const playlist = {js_playlist};
        let currentIndex = -1;
        let hls = new Hls();
        let isLocked = false;
        
        const player = new Plyr('#player', {{
            controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'settings', 'fullscreen'],
            hideControls: true 
        }});

        function openCinema(idx) {{
            const item = playlist[idx];
            currentIndex = idx;
            
            document.getElementById('bgLayer').style.backgroundImage = `url('${{item.bg}}')`;
            document.getElementById('mTitle').innerText = item.name;
            document.getElementById('mType').innerText = item.type;
            
            updateFavBtn('favBtn');
            document.getElementById('cinemaModal').style.display = 'block';
        }}

        function closeCinema() {{ document.getElementById('cinemaModal').style.display = 'none'; }}

        function startPlayer() {{
            document.getElementById('cinemaModal').style.display = 'none';
            document.getElementById('playerModal').style.display = 'flex';
            document.getElementById('pTitle').innerText = playlist[currentIndex].name;
            updateFavBtn('pFavBtn');
            
            const item = playlist[currentIndex];
            const v = document.getElementById('player');
            const p = document.getElementById('pdfFrame');
            const i = document.getElementById('imgView');
            const c = document.getElementById('centerControls');
            const b = document.getElementById('extControls');

            v.style.display='none'; p.style.display='none'; i.style.display='none';
            c.style.display='none'; b.style.display='none';

            if(item.type === 'VIDEO' || item.type === 'AUDIO') {{
                v.style.display='block'; c.style.display='flex'; b.style.display='flex';
                if(Hls.isSupported() && item.url.includes('.m3u8')) {{
                    hls.loadSource(item.url); hls.attachMedia(v);
                }} else {{ v.src = item.url; }}
                player.play();
            }} else if(item.type === 'PDF') {{
                p.style.display='block';
                p.src = "https://docs.google.com/gview?embedded=true&url=" + encodeURIComponent(item.url);
            }} else if(item.type === 'IMAGE') {{
                i.style.display='block'; i.src = item.url;
            }} else {{
                window.open(item.url, '_blank'); closePlayer();
            }}
        }}

        function closePlayer() {{
            player.pause();
            document.getElementById('playerModal').style.display = 'none';
        }}

        // RED BAR GESTURES
        let startY = 0;
        let startVal = 0;
        const area = document.getElementById('gestureArea');
        const redBar = document.getElementById('redBar');
        const gVal = document.getElementById('gestureVal');

        area.addEventListener('touchstart', (e) => {{
            if(isLocked) return;
            startY = e.touches[0].clientY;
            if(e.touches[0].clientX > window.innerWidth / 2) startVal = player.volume;
            else startVal = 100; 
        }});

        area.addEventListener('touchmove', (e) => {{
            if(isLocked) return;
            e.preventDefault();
            const delta = startY - e.touches[0].clientY;
            const percent = delta / 3; 
            
            redBar.style.opacity = '1';
            gVal.style.opacity = '1';

            if(e.touches[0].clientX > window.innerWidth / 2) {{
                // Volume
                let v = startVal + (delta/200);
                if(v>1) v=1; if(v<0) v=0;
                player.volume = v;
                redBar.style.height = (v*100) + "%";
                gVal.innerText = Math.round(v*100) + "%";
            }} else {{
                // Brightness
                let b = 100 + percent;
                if(b<20) b=20; if(b>150) b=150;
                document.getElementById('playerModal').style.filter = `brightness(${{b}}%)`;
                redBar.style.height = ((b-20)/1.3) + "%";
                gVal.innerText = Math.round(b) + "%";
            }}
        }});

        area.addEventListener('touchend', () => {{
            setTimeout(() => {{ 
                redBar.style.opacity='0'; gVal.style.opacity='0'; 
            }}, 500);
        }});

        // CONTROLS
        function togglePlay() {{ player.togglePlay(); }}
        function seek(s) {{ player.currentTime += s; }}
        function playNext() {{ if(currentIndex+1 < playlist.length) openCinema(currentIndex+1); }}
        function downloadCurrent() {{ window.open(playlist[currentIndex].url, '_blank'); }}
        
        function toggleLock() {{
            isLocked = !isLocked;
            const icon = document.querySelector('.lock-icon');
            icon.innerText = isLocked ? "🔒" : "🔓";
            document.getElementById('centerControls').style.display = isLocked ? "none" : "flex";
            document.getElementById('extControls').style.opacity = isLocked ? "0.5" : "1";
            document.getElementById('extControls').style.pointerEvents = isLocked ? "none" : "auto";
        }}

        // FAVORITES LOGIC
        function toggleFavPopup() {{ toggleFav('favBtn'); }}
        function toggleFavPlayer() {{ toggleFav('pFavBtn'); }}

        function toggleFav(btnId) {{
            const url = playlist[currentIndex].url;
            if(localStorage.getItem('fav_'+url)) {{
                localStorage.removeItem('fav_'+url);
            }} else {{
                localStorage.setItem('fav_'+url, 'true');
            }}
            updateFavBtn(btnId);
        }}

        function updateFavBtn(btnId) {{
            const url = playlist[currentIndex].url;
            const btn = document.getElementById(btnId);
            if(localStorage.getItem('fav_'+url)) {{
                btn.innerText = "❤️ Saved"; btn.style.background = "white"; btn.style.color = "black";
            }} else {{
                btn.innerText = "❤️ Add to Favorites"; btn.style.background = "rgba(255,255,255,0.15)"; btn.style.color = "white";
            }}
        }}

        function filterList(t) {{
            document.querySelectorAll('.item-card').forEach(e => e.style.display = (t==='all' || e.getAttribute('data-type')===t) ? 'flex' : 'none');
        }}
        function searchList() {{
            const v = document.getElementById('searchInput').value.toLowerCase();
            document.querySelectorAll('.item-card').forEach(e => e.style.display = e.innerText.toLowerCase().includes(v) ? 'flex' : 'none');
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
        return await m.reply_text(f"🔥 **Ultimate Bot Ready**\n\n/html - Generate\n/sky - Secured\n/txt - Links")
    if cmd == "stop":
        user_mode.pop(m.from_user.id, None)
        return await m.reply_text("🛑 Reset.")
    user_mode[m.from_user.id] = cmd
    await m.reply_text(f"✅ Mode: {cmd.upper()}\nFile bhejo!")

@app.on_message(filters.document)
async def process_file(c, m):
    uid = m.from_user.id
    mode = user_mode.get(uid)
    if not mode: return await m.reply_text("⚠️ Select mode!")
    
    msg = await m.reply_text("🔄 Processing...")
    path = await m.download()
    with open(path, "r", encoding="utf-8", errors="ignore") as f: content = f.read()
    
    out_path = path + ".html"
    cap = ""

    if mode in ["html", "sky"]:
        html_data = generate_html(m.document.file_name, content, is_protected=(mode=="sky"))
        out_path = path.rsplit('.', 1)[0] + "_Ultimate.html"
        with open(out_path, "w", encoding="utf-8") as f: f.write(html_data)
        cap = "🔥 **Final Dashboard Created**\nFeatures: 4K Cinema, Red Gestures, Telegram Link, Categories."
    
    elif mode == "txt":
        links = re.findall(r"(https?://[^\s\n]+)", content)
        out_path = path.rsplit('.', 1)[0] + "_links.txt"
        with open(out_path, "w", encoding="utf-8") as f: f.write("\n".join(links))
        cap = f"📄 Extracted {len(links)} Links"

    await m.reply_document(out_path, caption=cap)
    await msg.delete()
    if os.path.exists(path): os.remove(path)
    if os.path.exists(out_path): os.remove(out_path)

print("🔥 Ultimate Bot Started...")
app.run()
