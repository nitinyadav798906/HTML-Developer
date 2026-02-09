import os
import re
import json
import random
from pyrogram import Client, filters

# ================= CONFIGURATION =================
BOT_OWNER_NAME = "Sachin & Nitin"
TELEGRAM_LINK = "https://t.me/Raftaarss_don" 
API_ID = 12475131
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"
SKY_PASSWORD = "7989"

app = Client("ultimate_final_ver", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ================= HTML GENERATOR =================
def generate_html(file_name, content, is_protected=False):
    title = os.path.splitext(file_name)[0]
    raw_lines = re.findall(r"([^:\n]+):?\s*(https?://[^\s\n]+)", content)
    
    v_c = p_c = a_c = i_c = 0
    items_html = ""
    playlist_data = []

    # 4K Nature Posters
    posters = [
        "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=500&q=80",
        "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=500&q=80",
        "https://images.unsplash.com/photo-1501854140884-074cf2b2c3af?w=500&q=80"
    ]

    for idx, (name, url) in enumerate(raw_lines):
        name = name.strip()
        url = url.strip()
        low_u = url.lower()
        
        # CATEGORIES
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
        playlist_data.append({"url": url, "name": name, "type": t, "poster": poster})

        items_html += f'''
        <div class="list-item" id="item-{idx}" data-type="{t}" onclick="openCinema({idx})">
            <div class="item-icon-box">{icon}</div>
            <div class="item-info">
                <div class="item-title">{name}</div>
                <div class="item-meta">
                    <span class="meta-tag tag-{t}">{t}</span>
                    <span class="fav-indicator" id="list-fav-{idx}" style="display:none; color:var(--primary);">❤️</span>
                </div>
            </div>
        </div>'''

    js_playlist = json.dumps(playlist_data)

    # LOGIN SCREEN
    login_html = ""
    security_script = "document.getElementById('app-wrapper').style.display = 'block';" 
    if is_protected:
        security_script = "document.getElementById('login-screen').style.display = 'flex';"
        login_html = f"""
        <div id="login-screen">
            <div class="login-box">
                <h3 style="color:var(--primary); margin-top:0;">🔒 Secured</h3>
                <input type="password" id="passInput" placeholder="Enter Password">
                <button onclick="checkPass()">Unlock</button>
                <p id="errMsg" style="color:red;font-size:12px; margin-top:10px;"></p>
            </div>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html lang="en" data-theme="dark" data-color="blue">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
        /* CONFIG */
        :root {{ --red: #ef4444; --green: #10b981; --orange: #f59e0b; }}
        
        /* THEMES */
        [data-theme="dark"] {{ --bg: #0f172a; --card-bg: #1e293b; --text: #f8fafc; --text-sec: #94a3b8; --border: #334155; --modal-bg: #000; }}
        [data-theme="light"] {{ --bg: #f8fafc; --card-bg: #ffffff; --text: #1e293b; --text-sec: #64748b; --border: #e2e8f0; --modal-bg: #fff; }}
        
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
        .h-top {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
        .h-title {{ margin: 0; font-size: 16px; font-weight: 700; color: var(--primary); }}
        .right-actions {{ display: flex; align-items: center; gap: 12px; }}
        .tg-link {{ color: white; background: var(--primary); text-decoration: none; font-size: 11px; font-weight: bold; padding: 5px 12px; border-radius: 20px; }}
        .mode-btn {{ cursor: pointer; font-size: 18px; }}

        .theme-row {{ display: flex; gap: 8px; overflow-x: auto; padding-bottom: 5px; }}
        .t-dot {{ width: 22px; height: 22px; border-radius: 50%; cursor: pointer; border: 2px solid transparent; transition: 0.2s; flex-shrink: 0; }}
        .t-dot:hover {{ transform: scale(1.2); }}

        /* FILTERS */
        .stats-container {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; padding: 15px; }}
        .stat-card {{ background: var(--card-bg); padding: 10px 5px; border-radius: 8px; text-align: center; cursor: pointer; border: 1px solid var(--border); transition: 0.2s; }}
        .stat-num {{ font-size: 14px; font-weight: 800; display: block; }}
        .stat-label {{ font-size: 9px; font-weight: 600; text-transform: uppercase; margin-top: 2px; color: var(--text-sec); }}
        
        .sc-fav {{ color: var(--red); border-color: var(--red); }}
        .sc-vid {{ color: var(--primary); }}
        .sc-aud {{ color: var(--orange); }}
        .sc-pdf {{ color: var(--green); }}

        /* LIST */
        .list-container {{ padding: 0 15px; }}
        .search-box {{ display: flex; align-items: center; background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; margin-bottom: 10px; }}
        .search-bar {{ width: 100%; padding: 12px; border: none; background: transparent; color: var(--text); outline: none; }}
        .clear-search {{ padding: 0 12px; cursor: pointer; display: none; color: var(--text-sec); }}
        
        .list-item {{ background: var(--card-bg); margin-bottom: 8px; border-radius: 8px; padding: 12px; display: flex; align-items: center; border: 1px solid var(--border); cursor: pointer; }}
        .item-icon-box {{ width: 40px; height: 40px; background: rgba(100,100,100,0.1); border-radius: 8px; display: flex; justify-content: center; align-items: center; margin-right: 12px; font-size: 18px; }}
        .item-info {{ flex-grow: 1; min-width: 0; }}
        .item-title {{ font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 4px; }}
        .item-meta {{ display: flex; align-items: center; gap: 8px; }}
        .meta-tag {{ font-size: 9px; padding: 2px 6px; border-radius: 4px; font-weight: bold; background: rgba(100,100,100,0.1); }}
        .tag-VIDEO {{ color: var(--primary); }} .tag-PDF {{ color: var(--green); }} .tag-AUDIO {{ color: var(--orange); }}

        /* PLAYER OVERLAY & UI */
        .cinema-modal, .player-overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 3000; }}
        .player-overlay {{ z-index: 4000; background: black; flex-direction: column; }}
        
        .bg-layer {{ position: absolute; top: 0; left: 0; width: 100%; height: 60%; background-size: cover; background-position: center; mask-image: linear-gradient(to bottom, black 20%, transparent 100%); opacity: 0.6; }}
        .cinema-content {{ position: absolute; bottom: 0; width: 100%; height: 60%; padding: 20px; background: linear-gradient(to top, #000 20%, transparent); display: flex; flex-direction: column; justify-content: flex-end; align-items: center; gap: 15px; }}
        .c-poster {{ width: 120px; height: 180px; border-radius: 8px; object-fit: cover; box-shadow: 0 5px 20px black; border: 1px solid rgba(255,255,255,0.2); }}
        .c-title {{ font-size: 20px; font-weight: 800; color: white; text-align: center; margin: 0; }}
        .action-btn {{ width: 100%; padding: 14px; border-radius: 8px; font-size: 15px; font-weight: 700; border: none; cursor: pointer; }}
        .btn-main {{ background: var(--primary); color: white; }}
        .btn-sub {{ background: rgba(255,255,255,0.15); color: white; border: 1px solid rgba(255,255,255,0.2); backdrop-filter: blur(5px); }}

        /* WATERMARK */
        .watermark {{ position: absolute; top: 15px; right: 60px; color: rgba(255,255,255,0.4); font-weight: 900; font-size: 16px; pointer-events: none; z-index: 55; text-shadow: 0 2px 5px black; }}
        
        /* RED BAR & GESTURES */
        .red-bar-box {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 50; display: flex; justify-content: center; align-items: center; }}
        .red-bar {{ width: 50px; height: 0%; background: linear-gradient(to top, rgba(255,0,0,0.8), transparent); box-shadow: 0 0 40px #ff0000; opacity: 0; transition: height 0.1s; border-radius: 20px; }}
        .gesture-val {{ position: absolute; color: white; font-weight: bold; font-size: 30px; opacity: 0; z-index: 60; top: 40%; left: 50%; transform: translateX(-50%); text-shadow: 0 0 10px black; }}

        .player-header {{ position: absolute; top: 0; width: 100%; padding: 15px; display: flex; justify-content: space-between; z-index: 50; background: linear-gradient(to bottom, rgba(0,0,0,0.8), transparent); align-items: center; }}
        .player-mid {{ flex-grow: 1; position: relative; display: flex; align-items: center; justify-content: center; width: 100%; }}
        .bottom-controls {{ background: #000; padding: 15px; display: flex; justify-content: center; gap: 8px; border-top: 1px solid #222; flex-wrap: wrap; z-index: 60; }}
        .ctrl-btn {{ background: #222; color: white; border: none; padding: 8px 14px; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; }}
        .ctrl-next {{ background: var(--primary); color: white; }}
        
        .settings-menu {{ position: absolute; top: 60px; right: 20px; background: rgba(20,20,20,0.95); border: 1px solid #333; border-radius: 8px; padding: 15px; z-index: 100; display: none; flex-direction: column; gap: 10px; width: 220px; backdrop-filter: blur(10px); }}
        .sm-item {{ display: flex; flex-direction: column; gap: 5px; }}
        .sm-label {{ font-size: 12px; color: #aaa; text-transform: uppercase; }}
        .sm-select {{ background: #333; color: white; border: none; padding: 8px; border-radius: 4px; font-size: 14px; }}
        
        /* CLEAN BOX */
        .clean-btn {{ background: #ef4444; color: white; border: none; padding: 8px; width: 100%; border-radius: 4px; font-weight: bold; cursor: pointer; margin-top: 5px; }}
        
        .lock-icon {{ position: absolute; bottom: 30px; right: 20px; color: white; background: rgba(255,255,255,0.2); padding: 12px; border-radius: 50%; cursor: pointer; z-index: 65; font-size: 18px; }}
        
        /* MINIMIZE (PiP) */
        body.minimized .player-overlay {{
            width: 320px !important; height: 180px !important; 
            top: auto !important; left: auto !important; bottom: 20px !important; right: 20px !important;
            border-radius: 12px; border: 2px solid var(--primary); box-shadow: 0 10px 40px rgba(0,0,0,0.5);
        }}
        body.minimized .bottom-controls, body.minimized .settings-menu, 
        body.minimized .lock-icon, body.minimized .watermark, body.minimized .red-bar-box, 
        body.minimized .gesture-val {{ display: none !important; }}
        
        body.minimized .player-header {{ padding: 5px; }}
        body.minimized #pTitle {{ font-size: 10px; white-space: nowrap; }}
        body.minimized .player-mid {{ pointer-events: none; }} 

        .pdf-frame {{ width: 100%; height: 100%; border: none; background: white; }}
        .img-view {{ width: 100%; height: 100%; object-fit: contain; }}
        .footer {{ text-align: center; padding: 20px; color: var(--text-sec); font-size: 11px; }}
        #toast {{ position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%); background: rgba(0,0,0,0.8); color: white; padding: 8px 16px; border-radius: 20px; font-size: 12px; z-index: 5000; display: none; }}
    </style>
</head>
<body>
    {login_html}

    <div id="app-wrapper">
        <div class="header">
            <div class="h-top">
                <div class="h-title">{title}</div>
                <div class="right-actions">
                    <a href="{TELEGRAM_LINK}" target="_blank" class="tg-link">✈ Join TG</a>
                    <span class="mode-btn" onclick="toggleMode()">🌓</span>
                </div>
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
            <div class="stat-card" onclick="filterList('all')"><span class="stat-num">{len(raw_lines)}</span><span class="stat-label">All</span></div>
            <div class="stat-card sc-fav" onclick="filterList('FAV')"><span class="stat-num" id="favCount">-</span><span class="stat-label">❤️ Favs</span></div>
            <div class="stat-card sc-vid" onclick="filterList('VIDEO')"><span class="stat-num">{v_c}</span><span class="stat-label">Video</span></div>
            <div class="stat-card sc-aud" onclick="filterList('AUDIO')"><span class="stat-num">{a_c}</span><span class="stat-label">Audio</span></div>
            <div class="stat-card" onclick="filterList('PDF')"><span class="stat-num" style="color:var(--green)">{p_c}</span><span class="stat-label">PDF</span></div>
            <div class="stat-card" onclick="filterList('IMAGE')"><span class="stat-num" style="color:var(--orange)">{i_c}</span><span class="stat-label">Img</span></div>
        </div>

        <div class="list-container">
            <div class="search-box">
                <input type="text" class="search-bar" id="searchInput" placeholder="Search..." onkeyup="searchList()">
                <span class="clear-search" onclick="clearSearch()">✕</span>
            </div>
            <div id="playlistContainer">{items_html}</div>
            <div class="footer">Credits: {BOT_OWNER_NAME}</div>
        </div>
    </div>

    <div id="cinemaModal" class="cinema-modal">
        <div onclick="closeCinema()" style="position:absolute; top:20px; left:20px; color:white; font-size:24px; z-index:60; cursor:pointer;">✕</div>
        <div class="bg-layer" id="bgLayer"></div>
        <div class="cinema-content">
            <img src="" class="c-poster" id="cPoster">
            <h1 class="c-title" id="cTitle">Title</h1>
            <div style="display:flex; gap:10px; font-size:12px; opacity:0.8;">
                <span style="background:rgba(255,255,255,0.2); padding:2px 6px; border-radius:4px;">HD</span>
                <span id="cType">VIDEO</span>
            </div>
            <div style="width:100%; display:flex; flex-direction:column; gap:10px;">
                <button class="action-btn btn-main" onclick="startPlayer()">▶ Watch Now</button>
                <button class="action-btn btn-sub" onclick="toggleFav('favBtn')" id="favBtn">❤️ Add to Favorites</button>
            </div>
        </div>
    </div>

    <div id="playerOverlay" class="player-overlay">
        <div class="red-bar-box"><div class="red-bar" id="redBar"></div></div>
        <div class="gesture-val" id="gVal">50%</div>
        <div class="watermark">{BOT_OWNER_NAME}</div>
        
        <div class="player-header">
            <div style="display:flex; align-items:center; gap:15px; width:70%;">
                <span style="color:white; font-weight:600; font-size:14px; overflow:hidden; white-space:nowrap; text-overflow:ellipsis;" id="pTitle">Player</span>
                <span onclick="toggleMinimize()" style="color:white; cursor:pointer; font-size:18px;">📉</span>
            </div>
            <div style="display:flex; gap:20px;">
                <span onclick="toggleSettings()" style="color:white; font-size:20px; cursor:pointer;">⚙️</span>
                <span onclick="closePlayer()" style="color:white; font-size:24px; cursor:pointer;">✕</span>
            </div>
        </div>

        <div id="settingsMenu" class="settings-menu">
            <div class="sm-item"><div class="sm-label">Speed</div>
                <select class="sm-select" onchange="changeSpeed(this.value)">
                    <option value="0.5">0.5x</option><option value="1" selected>1x</option><option value="1.5">1.5x</option><option value="2">2x</option><option value="3">3x</option><option value="4">4x</option>
                </select>
            </div>
            <div class="sm-item"><div class="sm-label">Quality</div>
                <select class="sm-select" id="qualitySelect" onchange="changeQuality(this.value)"><option value="-1">Auto</option></select>
            </div>
            <div class="sm-item" style="border-top:1px solid #444; padding-top:10px; margin-top:5px;">
                <button class="clean-btn" onclick="cleanAllData()">🗑️ Clean All Data</button>
            </div>
        </div>

        <div class="player-mid" id="gestureArea" onclick="if(document.body.classList.contains('minimized')) toggleMinimize()">
            <div class="lock-icon" onclick="toggleLock(); event.stopPropagation();">🔓</div>
            <video id="player" playsinline controls style="width:100%; max-height:100%;"></video>
            <iframe id="pdfFrame" class="pdf-frame" style="display:none;"></iframe>
            <img id="imgView" class="img-view" style="display:none;">
        </div>

        <div class="bottom-controls" id="extControls">
            <button class="ctrl-btn" onclick="seek(-10)">⏪ 10s</button>
            <button class="ctrl-btn" onclick="seek(10)">10s ⏩</button>
            <button class="ctrl-btn" onclick="showToast('GIF Mode: ON')">GIF</button>
            <button class="ctrl-btn" onclick="showToast('CC: Enabled')">CC</button>
            <button class="ctrl-btn ctrl-next" onclick="playNext()">Next ⏭</button>
            <button class="ctrl-btn" onclick="downloadCurrent()">⬇ DL</button>
            <button class="ctrl-btn" onclick="toggleFav('pFavBtn')" id="pFavBtn">🤍 Fav</button>
        </div>
    </div>
    
    <div id="toast">Alert</div>

    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        function toggleMode() {{
            const current = document.documentElement.getAttribute('data-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            document.documentElement.setAttribute('data-theme', next);
            localStorage.setItem('uTheme', next);
        }}
        function setTheme(color) {{
            document.documentElement.setAttribute('data-color', color);
            localStorage.setItem('uColor', color);
        }}
        document.documentElement.setAttribute('data-theme', localStorage.getItem('uTheme') || 'dark');
        document.documentElement.setAttribute('data-color', localStorage.getItem('uColor') || 'blue');

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
        let isLocked = false;
        
        const player = new Plyr('#player', {{
            controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'settings', 'fullscreen'],
            hideControls: true, speed: {{ selected: 1, options: [0.5, 1, 1.5, 2, 3, 4] }}
        }});

        player.on('ended', () => playNext());

        window.onload = function() {{
            updateFavCount();
            playlist.forEach((item, idx) => {{
                if(localStorage.getItem('fav_' + item.url)) document.getElementById('list-fav-' + idx).style.display = 'inline';
            }});
        }};

        function cleanAllData() {{
            if(confirm("Are you sure you want to clear all Watch History & Favorites?")) {{
                localStorage.clear();
                location.reload();
            }}
        }}

        function openCinema(idx) {{
            currentIndex = idx;
            const item = playlist[idx];
            document.getElementById('bgLayer').style.backgroundImage = `url('${{item.poster}}')`;
            document.getElementById('cPoster').src = item.poster;
            document.getElementById('cTitle').innerText = item.name;
            document.getElementById('cType').innerText = item.type;
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
            document.getElementById('settingsMenu').style.display = 'none';

            if(item.type === 'VIDEO' || item.type === 'AUDIO') {{
                v.style.display='block';
                if(Hls.isSupported() && item.url.includes('.m3u8')) {{
                    hls.loadSource(item.url); hls.attachMedia(v);
                    hls.on(Hls.Events.MANIFEST_PARSED, () => {{
                        const qSel = document.getElementById('qualitySelect');
                        qSel.innerHTML = '<option value="-1">Auto</option>';
                        hls.levels.forEach((l, idx) => {{ qSel.innerHTML += `<option value="${{idx}}">${{l.height}}p</option>`; }});
                    }});
                }} else {{ v.src = item.url; }}
                player.play();
            }} else if(item.type === 'PDF') {{
                p.style.display='block';
                p.src = "https://docs.google.com/gview?embedded=true&url=" + encodeURIComponent(item.url);
            }} else if(item.type === 'IMAGE') {{
                i.style.display='block'; i.src = item.url;
            }} else {{ window.open(item.url, '_blank'); closePlayer(); }}
        }}

        function closePlayer() {{
            player.pause();
            document.getElementById('playerOverlay').style.display = 'none';
            document.body.classList.remove('minimized');
        }}

        let startY = 0;
        const area = document.getElementById('gestureArea');
        const redBar = document.getElementById('redBar');
        const gVal = document.getElementById('gVal');

        area.addEventListener('touchstart', (e) => {{ if(!isLocked) startY = e.touches[0].clientY; }});
        area.addEventListener('touchmove', (e) => {{
            if(isLocked) return;
            e.preventDefault();
            const delta = startY - e.touches[0].clientY;
            
            redBar.style.opacity = '1';
            let h = Math.abs(delta) * 0.5; if(h>100) h=100;
            redBar.style.height = h + "%";
            gVal.style.opacity = '1';

            if(e.touches[0].clientX > window.innerWidth / 2) {{
                let change = delta / 500; 
                let newVol = Math.min(Math.max(player.volume + change, 0), 1);
                player.volume = newVol;
                gVal.innerText = "Vol: " + Math.round(newVol * 100) + "%";
            }}
        }});
        area.addEventListener('touchend', () => {{ redBar.style.opacity = '0'; gVal.style.opacity = '0'; }});

        function toggleSettings() {{
            const menu = document.getElementById('settingsMenu');
            menu.style.display = (menu.style.display === 'flex') ? 'none' : 'flex';
        }}
        function changeSpeed(val) {{ player.speed = parseFloat(val); }}
        function changeQuality(val) {{ hls.currentLevel = parseInt(val); }}
        function seek(s) {{ player.currentTime += s; }}
        function playNext() {{ if(currentIndex+1 < playlist.length) {{ currentIndex++; startPlayer(); }} }}
        function downloadCurrent() {{ window.open(playlist[currentIndex].url, '_blank'); }}
        function toggleLock() {{
            isLocked = !isLocked;
            document.querySelector('.lock-icon').innerText = isLocked ? '🔒' : '🔓';
            document.getElementById('extControls').style.display = isLocked ? 'none' : 'flex';
        }}
        function toggleMinimize() {{
            document.body.classList.toggle('minimized');
        }}
        function toggleFav(btnId) {{
            const url = playlist[currentIndex].url;
            if(localStorage.getItem('fav_'+url)) {{
                localStorage.removeItem('fav_'+url);
                document.getElementById('list-fav-' + currentIndex).style.display = 'none';
            }} else {{
                localStorage.setItem('fav_'+url, 'true');
                document.getElementById('list-fav-' + currentIndex).style.display = 'inline';
            }}
            updateFavBtn(btnId);
            updateFavCount();
        }}
        function updateFavBtn(btnId) {{
            const url = playlist[currentIndex].url;
            const btn = document.getElementById(btnId);
            const isFav = localStorage.getItem('fav_'+url);
            if(btnId === 'favBtn') btn.innerText = isFav ? "✓ Added" : "❤️ Add to Favorites";
            else btn.innerText = isFav ? "❤️ Saved" : "🤍 Fav";
        }}
        function updateFavCount() {{
            let c = 0;
            playlist.forEach(i => {{ if(localStorage.getItem('fav_'+i.url)) c++; }});
            document.getElementById('favCount').innerText = c;
        }}
        function filterList(t) {{
            document.querySelectorAll('.list-item').forEach(e => {{
                let show = false;
                if(t === 'all') show = true;
                else if(t === 'FAV') {{
                    const idx = e.id.split('-')[1];
                    if(localStorage.getItem('fav_' + playlist[idx].url)) show = true;
                }}
                else if(e.getAttribute('data-type') === t) show = true;
                e.style.display = show ? 'flex' : 'none';
            }});
        }}
        function searchList() {{
            const v = document.getElementById('searchInput').value.toLowerCase();
            document.querySelector('.clear-search').style.display = v ? 'block' : 'none';
            document.querySelectorAll('.list-item').forEach(e => e.style.display = e.innerText.toLowerCase().includes(v) ? 'flex' : 'none');
        }}
        function clearSearch() {{
            document.getElementById('searchInput').value = '';
            searchList();
        }}
        function showToast(msg) {{
            const t = document.getElementById('toast');
            t.innerText = msg; t.style.display = 'block';
            setTimeout(() => t.style.display = 'none', 2000);
        }}
    </script>
</body>
</html>
"""

# ================= TELEGRAM HANDLER =================
@app.on_message(filters.command(["start", "stop", "html", "sky", "txt"]))
async def handle_cmds(c, m):
    cmd = m.command[0]
    if cmd == "start":
        return await m.reply_text(f"🚀 **Bot Online**\n\n/html - Generate\n/sky - Secured\n/txt - Links")
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
        out_path = path.rsplit('.', 1)[0] + "_Final.html"
        with open(out_path, "w", encoding="utf-8") as f: f.write(html_data)
        cap = "✅ **Ultimate Dashboard**\nClean Box, Clear Search, Watermark, PiP Added!"
    
    elif mode == "txt":
        links = re.findall(r"(https?://[^\s\n]+)", content)
        out_path = path.rsplit('.', 1)[0] + "_links.txt"
        with open(out_path, "w", encoding="utf-8") as f: f.write("\n".join(links))
        cap = f"📄 Links: {len(links)}"

    await m.reply_document(out_path, caption=cap)
    await msg.delete()
    if os.path.exists(path): os.remove(path)
    if os.path.exists(out_path): os.remove(out_path)

print("🚀 Bot Started...")
app.run()
