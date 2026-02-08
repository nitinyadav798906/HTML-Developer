import os
import re
import json
import random
from datetime import datetime
from pyrogram import Client, filters

# ================= CONFIGURATION =================
BOT_OWNER_NAME = "Sachin & Nitin"
TELEGRAM_LINK = "https://t.me/Raftaarss_don" 
API_ID = 12475131
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"
SKY_PASSWORD = "7989"

app = Client("ultimate_settings_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ================= HTML GENERATOR =================
def generate_html(file_name, content, is_protected=False):
    title = os.path.splitext(file_name)[0]
    raw_lines = re.findall(r"([^:\n]+):?\s*(https?://[^\s\n]+)", content)
    
    v_c = p_c = a_c = i_c = 0
    items_html = ""
    playlist_data = []

    # Random Posters
    posters = [
        "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?w=500&q=80",
        "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&q=80", 
        "https://images.unsplash.com/photo-1616530940355-351fabd9524b?w=500&q=80"
    ]

    for idx, (name, url) in enumerate(raw_lines):
        name = name.strip()
        url = url.strip()
        low_u = url.lower()
        
        if any(x in low_u for x in [".m3u8", ".mpd", ".mp4", ".mkv"]): 
            t = "VIDEO"; v_c += 1; icon = "🎥"
        elif ".pdf" in low_u: 
            t = "PDF"; p_c += 1; icon = "📄"
        elif any(x in low_u for x in [".jpg", ".jpeg", ".png", ".webp"]): 
            t = "IMAGE"; i_c += 1; icon = "🖼️"
        elif any(x in low_u for x in [".m4a", ".mp3", ".wav"]): 
            t = "AUDIO"; a_c += 1; icon = "🎧"
        else: 
            t = "OTHER"; icon = "📂"

        poster = random.choice(posters)
        rating = round(random.uniform(7.5, 9.8), 1)
        playlist_data.append({"url": url, "name": name, "type": t, "poster": poster, "rating": rating})

        items_html += f'''
        <div class="list-item" id="item-{idx}" data-type="{t}" onclick="openCinema({idx})">
            <div class="item-icon-box">{icon}</div>
            <div class="item-info">
                <div class="item-title">{name}</div>
                <div class="item-meta">
                    <span class="meta-tag tag-{t}">{t}</span>
                    <span class="star-rating">★ {rating}</span>
                </div>
            </div>
        </div>'''

    js_playlist = json.dumps(playlist_data)

    # SECURE LOGIN
    login_html = ""
    security_script = "document.getElementById('app-wrapper').style.display = 'block';" 
    if is_protected:
        security_script = "document.getElementById('login-screen').style.display = 'flex';"
        login_html = f"""
        <div id="login-screen">
            <div class="login-box">
                <h3 style="color:var(--primary); margin:0 0 15px 0;">🔒 Secured Access</h3>
                <input type="password" id="passInput" placeholder="Enter Password">
                <button onclick="checkPass()">Unlock</button>
                <p id="errMsg" style="color:red;font-size:12px; margin-top:10px;"></p>
            </div>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html lang="en" data-color="blue">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* --- 7 COLOR THEMES --- */
        :root {{ 
            --bg: #0f172a; --card-bg: #1e293b; --text: #f8fafc; --text-sec: #94a3b8; 
            --border: #334155; --primary: #3b82f6; 
        }}
        
        [data-color="blue"] {{ --primary: #3b82f6; }}
        [data-color="red"] {{ --primary: #ef4444; }}
        [data-color="green"] {{ --primary: #22c55e; }}
        [data-color="purple"] {{ --primary: #a855f7; }}
        [data-color="orange"] {{ --primary: #f97316; }}
        [data-color="pink"] {{ --primary: #ec4899; }}
        [data-color="cyan"] {{ --primary: #06b6d4; }}

        body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding-bottom: 80px; transition: 0.3s; }}
        * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
        
        #app-wrapper {{ display: none; }} 

        /* LOGIN */
        #login-screen {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: var(--bg); z-index: 9999; display: none; justify-content: center; align-items: center; }}
        .login-box {{ background: var(--card-bg); padding: 25px; border-radius: 12px; width: 85%; max-width: 300px; border: 1px solid var(--border); text-align: center; }}
        .login-box input {{ width: 100%; padding: 12px; margin-bottom: 15px; border-radius: 6px; border: 1px solid var(--border); background: var(--bg); color: var(--text); outline: none; }}
        .login-box button {{ width: 100%; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }}

        /* HEADER */
        .header {{ background: var(--card-bg); padding: 15px; position: sticky; top: 0; z-index: 50; border-bottom: 1px solid var(--border); }}
        .h-top {{ display: flex; justify-content: space-between; align-items: center; }}
        .h-title {{ margin: 0; font-size: 16px; color: white; }}
        .tg-link {{ color: var(--primary); text-decoration: none; font-size: 12px; font-weight: bold; }}

        /* THEME DOTS */
        .theme-row {{ display: flex; gap: 10px; margin-top: 12px; overflow-x: auto; padding-bottom: 5px; }}
        .t-dot {{ width: 20px; height: 20px; border-radius: 50%; cursor: pointer; border: 2px solid transparent; transition: 0.2s; flex-shrink: 0; }}
        .t-dot:hover {{ transform: scale(1.2); }}
        .t-dot.active {{ border-color: white; transform: scale(1.1); }}

        /* STATS BOXES */
        .stats-container {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; padding: 15px; }}
        .stat-card {{ background: white; padding: 10px 5px; border-radius: 8px; text-align: center; cursor: pointer; box-shadow: 0 1px 3px rgba(0,0,0,0.2); transition: 0.2s; }}
        .stat-card:active {{ transform: scale(0.95); }}
        .stat-num {{ font-size: 15px; font-weight: 800; display: block; color: #333; }}
        .stat-label {{ font-size: 10px; font-weight: 600; text-transform: uppercase; margin-top: 2px; color: #666; }}
        
        /* LIST STYLE */
        .list-container {{ padding: 0 15px; }}
        .search-bar {{ width: 100%; padding: 12px; border-radius: 8px; border: 1px solid var(--border); background: var(--card-bg); color: var(--text); outline: none; margin-bottom: 10px; }}
        .list-item {{ background: var(--card-bg); margin-bottom: 8px; border-radius: 8px; padding: 12px; display: flex; align-items: center; border: 1px solid var(--border); cursor: pointer; }}
        .item-icon-box {{ width: 40px; height: 40px; background: rgba(255,255,255,0.05); border-radius: 8px; display: flex; justify-content: center; align-items: center; margin-right: 12px; font-size: 18px; }}
        .item-info {{ flex-grow: 1; min-width: 0; }}
        .item-title {{ font-size: 13px; font-weight: 600; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 4px; }}
        .item-meta {{ display: flex; align-items: center; gap: 8px; }}
        .meta-tag {{ font-size: 9px; padding: 2px 6px; border-radius: 4px; font-weight: bold; background: rgba(255,255,255,0.1); color: var(--primary); }}
        .star-rating {{ font-size: 11px; color: #f59e0b; font-weight: bold; }}

        /* CINEMA MODAL */
        .cinema-modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 3000; }}
        .bg-layer {{ position: absolute; top: 0; left: 0; width: 100%; height: 60%; background-size: cover; background-position: center; mask-image: linear-gradient(to bottom, black 20%, transparent 100%); -webkit-mask-image: linear-gradient(to bottom, black 20%, transparent 100%); opacity: 0.5; }}
        .cinema-content {{ position: absolute; bottom: 0; width: 100%; height: 60%; padding: 20px; background: linear-gradient(to top, #000 20%, transparent); display: flex; flex-direction: column; justify-content: flex-end; align-items: center; gap: 15px; }}
        .c-poster {{ width: 120px; height: 180px; border-radius: 8px; object-fit: cover; box-shadow: 0 5px 20px black; border: 1px solid rgba(255,255,255,0.2); }}
        .c-title {{ font-size: 20px; font-weight: 800; color: white; text-align: center; margin: 0; }}
        .action-btn {{ width: 100%; padding: 14px; border-radius: 8px; font-size: 15px; font-weight: 700; border: none; cursor: pointer; }}
        .btn-main {{ background: var(--primary); color: white; }}
        .btn-sub {{ background: rgba(255,255,255,0.1); color: white; border: 1px solid rgba(255,255,255,0.2); }}

        /* PLAYER */
        .player-overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: black; z-index: 4000; flex-direction: column; }}
        .red-bar-box {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 50; display: flex; justify-content: center; align-items: center; }}
        .red-bar {{ width: 50px; height: 0%; background: linear-gradient(to top, rgba(255,0,0,0.8), transparent); box-shadow: 0 0 40px #ff0000; opacity: 0; transition: height 0.1s; border-radius: 20px; }}
        .player-mid {{ flex-grow: 1; position: relative; display: flex; align-items: center; justify-content: center; }}
        .bottom-controls {{ background: #000; padding: 15px; display: flex; justify-content: center; gap: 10px; border-top: 1px solid #222; flex-wrap: wrap; z-index: 60; }}
        .ctrl-btn {{ background: #222; color: white; border: none; padding: 10px 18px; border-radius: 6px; font-size: 13px; font-weight: 600; cursor: pointer; }}
        .ctrl-next {{ background: var(--primary); color: white; }}
        
        /* SETTINGS MENU */
        .settings-menu {{ 
            position: absolute; top: 60px; right: 20px; background: rgba(20,20,20,0.95); 
            border: 1px solid #333; border-radius: 8px; padding: 15px; z-index: 100;
            display: none; flex-direction: column; gap: 10px; width: 200px;
            backdrop-filter: blur(10px);
        }}
        .sm-item {{ display: flex; flex-direction: column; gap: 5px; }}
        .sm-label {{ font-size: 12px; color: #aaa; text-transform: uppercase; }}
        .sm-select {{ 
            background: #333; color: white; border: none; padding: 8px; border-radius: 4px; font-size: 14px;
        }}

        .pdf-frame {{ width: 100%; height: 100%; border: none; background: white; }}
        .img-view {{ width: 100%; height: 100%; object-fit: contain; }}
        .footer {{ text-align: center; padding: 20px; color: #555; font-size: 11px; }}
    </style>
</head>
<body>
    {login_html}

    <div id="app-wrapper">
        <div class="header">
            <div class="h-top">
                <div>
                    <h3 class="h-title">{title}</h3>
                    <div style="font-size:11px; color:#888;">{len(raw_lines)} Files</div>
                </div>
                <a href="{TELEGRAM_LINK}" target="_blank" class="tg-link">✈ Join Telegram</a>
            </div>
            
            <div class="theme-row">
                <div class="t-dot" style="background:#3b82f6" onclick="setTheme('blue')"></div>
                <div class="t-dot" style="background:#ef4444" onclick="setTheme('red')"></div>
                <div class="t-dot" style="background:#22c55e" onclick="setTheme('green')"></div>
                <div class="t-dot" style="background:#a855f7" onclick="setTheme('purple')"></div>
                <div class="t-dot" style="background:#f97316" onclick="setTheme('orange')"></div>
                <div class="t-dot" style="background:#ec4899" onclick="setTheme('pink')"></div>
                <div class="t-dot" style="background:#06b6d4" onclick="setTheme('cyan')"></div>
            </div>
        </div>

        <div class="stats-container">
            <div class="stat-card" onclick="filterList('all')">
                <span class="stat-num">{len(raw_lines)}</span><span class="stat-label">All</span>
            </div>
            <div class="stat-card" onclick="filterList('VIDEO')">
                <span class="stat-num" style="color:#ef4444">{v_c}</span><span class="stat-label" style="color:#ef4444">Video</span>
            </div>
            <div class="stat-card" onclick="filterList('PDF')">
                <span class="stat-num" style="color:#10b981">{p_c}</span><span class="stat-label" style="color:#10b981">PDF</span>
            </div>
            <div class="stat-card" onclick="filterList('IMAGE')">
                <span class="stat-num" style="color:#f59e0b">{i_c}</span><span class="stat-label" style="color:#f59e0b">Img</span>
            </div>
        </div>

        <div class="list-container">
            <input type="text" class="search-bar" id="searchInput" placeholder="Search..." onkeyup="searchList()">
            <div id="playlistContainer">{items_html}</div>
            <div class="footer">Credits: {BOT_OWNER_NAME}</div>
        </div>
    </div>

    <div id="cinemaModal" class="cinema-modal">
        <div onclick="closeCinema()" style="position:absolute; top:20px; left:20px; color:white; font-size:24px; z-index:60; cursor:pointer;">✕</div>
        <div class="bg-layer" id="bgLayer"></div>
        <div class="cinema-content">
            <img src="" class="c-poster" id="cPoster">
            <h1 class="c-title" id="cTitle">Movie Title</h1>
            <div style="display:flex; gap:10px; font-size:12px; opacity:0.8;">
                <span style="background:rgba(255,255,255,0.2); padding:2px 6px; border-radius:4px;">HD</span>
                <span id="cRating">⭐ 9.0</span>
                <span>2025</span>
            </div>
            <div style="width:100%; display:flex; flex-direction:column; gap:10px;">
                <button class="action-btn btn-main" onclick="startPlayer()">▶ Watch Now</button>
                <button class="action-btn btn-sub" onclick="toggleFav('favBtn')" id="favBtn">+ Add to Favorites</button>
            </div>
        </div>
    </div>

    <div id="playerOverlay" class="player-overlay">
        <div class="red-bar-box"><div class="red-bar" id="redBar"></div></div>
        
        <div style="position:absolute; top:0; width:100%; padding:15px; display:flex; justify-content:space-between; z-index:50; background:linear-gradient(to bottom, rgba(0,0,0,0.8), transparent); align-items:center;">
            <div style="display:flex; align-items:center; gap:15px; width:80%;">
                <span style="color:white; font-weight:600; font-size:14px; overflow:hidden; white-space:nowrap; text-overflow:ellipsis;" id="pTitle">Player</span>
            </div>
            <div style="display:flex; align-items:center; gap:15px;">
                <span onclick="toggleSettings()" style="color:white; font-size:20px; cursor:pointer;">⚙️</span>
                <span onclick="closePlayer()" style="color:white; font-size:24px; cursor:pointer;">✕</span>
            </div>
        </div>

        <div id="settingsMenu" class="settings-menu">
            <div class="sm-item">
                <div class="sm-label">Speed</div>
                <select class="sm-select" onchange="changeSpeed(this.value)">
                    <option value="0.5">0.5x</option>
                    <option value="1" selected>Normal</option>
                    <option value="1.5">1.5x</option>
                    <option value="2">2x</option>
                </select>
            </div>
            <div class="sm-item">
                <div class="sm-label">Quality</div>
                <select class="sm-select" id="qualitySelect" onchange="changeQuality(this.value)">
                    <option value="-1">Auto</option>
                </select>
            </div>
        </div>

        <div class="player-mid" id="gestureArea">
            <video id="player" playsinline controls style="width:100%; max-height:100%;"></video>
            <iframe id="pdfFrame" class="pdf-frame" style="display:none;"></iframe>
            <img id="imgView" class="img-view" style="display:none;">
        </div>

        <div class="bottom-controls">
            <button class="ctrl-btn" onclick="seek(-10)">⏪ 10s</button>
            <button class="ctrl-btn" onclick="seek(10)">10s ⏩</button>
            <button class="ctrl-btn ctrl-next" onclick="playNext()">Next ⏭</button>
            <button class="ctrl-btn" onclick="downloadCurrent()">⬇ DL</button>
            <button class="ctrl-btn" onclick="toggleFav('pFavBtn')" id="pFavBtn">🤍 Fav</button>
        </div>
    </div>

    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        // THEME LOGIC
        function setTheme(color) {{
            document.documentElement.setAttribute('data-color', color);
            localStorage.setItem('themeColor', color);
        }}
        
        // Restore Theme
        const savedTheme = localStorage.getItem('themeColor') || 'blue';
        setTheme(savedTheme);

        function checkPass() {{
            if(document.getElementById('passInput').value === "{SKY_PASSWORD}") {{
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('app-wrapper').style.display = 'block';
            }} else document.getElementById('errMsg').innerText = "Incorrect Password!";
        }}
        {security_script}

        const playlist = {js_playlist};
        let currentIndex = -1;
        let hls = new Hls();
        
        const player = new Plyr('#player', {{
            controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'settings', 'fullscreen'],
            hideControls: true 
        }});

        function openCinema(idx) {{
            const item = playlist[idx];
            currentIndex = idx;
            document.getElementById('bgLayer').style.backgroundImage = `url('${{item.poster}}')`;
            document.getElementById('cPoster').src = item.poster;
            document.getElementById('cTitle').innerText = item.name;
            document.getElementById('cRating').innerText = "⭐ " + item.rating;
            
            updateFavBtn('favBtn');
            document.getElementById('cinemaModal').style.display = 'block';
        }}

        function closeCinema() {{ document.getElementById('cinemaModal').style.display = 'none'; }}

        function startPlayer() {{
            document.getElementById('cinemaModal').style.display = 'none';
            document.getElementById('playerOverlay').style.display = 'flex';
            document.getElementById('pTitle').innerText = playlist[currentIndex].name;
            updateFavBtn('pFavBtn');
            
            const item = playlist[currentIndex];
            const v = document.getElementById('player');
            const p = document.getElementById('pdfFrame');
            const i = document.getElementById('imgView');

            v.style.display='none'; p.style.display='none'; i.style.display='none';
            document.getElementById('settingsMenu').style.display = 'none'; // Reset menu

            if(item.type === 'VIDEO' || item.type === 'AUDIO') {{
                v.style.display='block';
                if(Hls.isSupported() && item.url.includes('.m3u8')) {{
                    hls.loadSource(item.url); hls.attachMedia(v);
                    hls.on(Hls.Events.MANIFEST_PARSED, () => {{
                        const qSel = document.getElementById('qualitySelect');
                        qSel.innerHTML = '<option value="-1">Auto</option>';
                        hls.levels.forEach((l, idx) => {{
                            qSel.innerHTML += `<option value="${{idx}}">${{l.height}}p</option>`;
                        }});
                    }});
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
            document.getElementById('playerOverlay').style.display = 'none';
        }}

        // SETTINGS LOGIC
        function toggleSettings() {{
            const menu = document.getElementById('settingsMenu');
            menu.style.display = (menu.style.display === 'flex') ? 'none' : 'flex';
        }}
        function changeSpeed(val) {{ player.speed = parseFloat(val); }}
        function changeQuality(val) {{ hls.currentLevel = parseInt(val); }}

        // RED BAR GESTURES
        let startY = 0;
        const area = document.getElementById('gestureArea');
        const redBar = document.getElementById('redBar');

        area.addEventListener('touchstart', (e) => {{ startY = e.touches[0].clientY; }});
        area.addEventListener('touchmove', (e) => {{
            e.preventDefault();
            const delta = startY - e.touches[0].clientY;
            redBar.style.opacity = '1';
            let h = Math.abs(delta) * 0.5;
            if(h > 100) h = 100;
            redBar.style.height = h + "%";
            
            if(e.touches[0].clientX > window.innerWidth / 2) {{
                player.volume = Math.min(Math.max(player.volume + (delta/500), 0), 1);
            }}
        }});
        area.addEventListener('touchend', () => {{ redBar.style.opacity = '0'; }});

        // CONTROLS
        function seek(s) {{ player.currentTime += s; }}
        function playNext() {{ if(currentIndex+1 < playlist.length) openCinema(currentIndex+1); }}
        function downloadCurrent() {{ window.open(playlist[currentIndex].url, '_blank'); }}
        
        function toggleFav(btnId) {{
            const url = playlist[currentIndex].url;
            if(localStorage.getItem('fav_'+url)) localStorage.removeItem('fav_'+url);
            else localStorage.setItem('fav_'+url, 'true');
            updateFavBtn(btnId);
        }}

        function updateFavBtn(btnId) {{
            const url = playlist[currentIndex].url;
            const btn = document.getElementById(btnId);
            const isFav = localStorage.getItem('fav_'+url);
            if(btnId === 'favBtn') btn.innerText = isFav ? "✓ Added" : "+ Add to Favorites";
            else btn.innerText = isFav ? "❤️ Saved" : "🤍 Fav";
        }}

        function filterList(t) {{
            document.querySelectorAll('.list-item').forEach(e => e.style.display = (t==='all' || e.getAttribute('data-type')===t) ? 'flex' : 'none');
        }}
        function searchList() {{
            const v = document.getElementById('searchInput').value.toLowerCase();
            document.querySelectorAll('.list-item').forEach(e => e.style.display = e.innerText.toLowerCase().includes(v) ? 'flex' : 'none');
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
        return await m.reply_text(f"⚙️ **Bot Ready with Settings**\n\n/html - Generate\n/sky - Secured\n/txt - Links")
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
        out_path = path.rsplit('.', 1)[0] + "_Settings.html"
        with open(out_path, "w", encoding="utf-8") as f: f.write(html_data)
        cap = "⚙️ **Player with Settings Created**\nSpeed & Quality Options Added!"
    
    elif mode == "txt":
        links = re.findall(r"(https?://[^\s\n]+)", content)
        out_path = path.rsplit('.', 1)[0] + "_links.txt"
        with open(out_path, "w", encoding="utf-8") as f: f.write("\n".join(links))
        cap = f"📄 Extracted {len(links)} Links"

    await m.reply_document(out_path, caption=cap)
    await msg.delete()
    if os.path.exists(path): os.remove(path)
    if os.path.exists(out_path): os.remove(out_path)

print("⚙️ Settings Bot Started...")
app.run()
