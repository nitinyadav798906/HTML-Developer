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

    # LOGIN LOGIC
    login_html = ""
    security_script = "document.getElementById('app-wrapper').style.display = 'block';" 
    
    if is_protected:
        security_script = "document.getElementById('login-screen').style.display = 'flex';"
        login_html = f"""
        <div id="login-screen">
            <div class="login-box">
                <h2 style="color:var(--primary)">🔒 Secured File</h2>
                <p>Created by {BOT_OWNER_NAME}</p>
                <input type="password" id="passInput" placeholder="Enter Access Key">
                <button onclick="checkPass()">Unlock Dashboard</button>
                <p id="errMsg" style="color:red; font-size:12px; margin-top:10px;"></p>
            </div>
        </div>
        """

    return f"""
<!DOCTYPE html>
<html lang="en" data-theme="blue">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    
    <style>
        /* --- 7 THEMES --- */
        :root {{ --bg: #f3f4f6; --card-bg: #fff; --text: #1f2937; --border: #e5e7eb; }}
        
        [data-theme="blue"] {{ --primary: #2563eb; --light: #eff6ff; }}
        [data-theme="red"] {{ --primary: #dc2626; --light: #fef2f2; }}
        [data-theme="green"] {{ --primary: #16a34a; --light: #f0fdf4; }}
        [data-theme="purple"] {{ --primary: #9333ea; --light: #faf5ff; }}
        [data-theme="orange"] {{ --primary: #ea580c; --light: #fff7ed; }}
        [data-theme="pink"] {{ --primary: #db2777; --light: #fdf2f8; }}
        [data-theme="dark"] {{ --primary: #475569; --light: #f8fafc; --bg: #0f172a; --card-bg: #1e293b; --text: #f1f5f9; --border: #334155; }}

        * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
        body {{ font-family: 'Poppins', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding-bottom: 80px; transition: 0.3s; }}
        
        #app-wrapper {{ display: none; }} 

        /* LOGIN */
        #login-screen {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: var(--bg); z-index: 5000; display: none; justify-content: center; align-items: center; }}
        .login-box {{ background: var(--card-bg); padding: 30px; border-radius: 16px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); text-align: center; width: 90%; max-width: 320px; border: 1px solid var(--border); }}
        .login-box input {{ width: 100%; padding: 12px; margin: 15px 0; border: 1px solid var(--border); border-radius: 8px; background: var(--bg); color: var(--text); outline: none; }}
        .login-box button {{ width: 100%; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }}

        /* HEADER */
        .header {{ background: var(--card-bg); padding: 15px; position: sticky; top: 0; z-index: 50; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-bottom: 1px solid var(--border); }}
        .top-row {{ display: flex; justify-content: space-between; align-items: center; }}
        .owner-tag {{ font-size: 10px; background: var(--primary); color: white; padding: 3px 8px; border-radius: 20px; font-weight: bold; }}
        .color-dots {{ display: flex; gap: 8px; margin-top: 10px; overflow-x: auto; padding-bottom: 5px; }}
        .dot {{ width: 20px; height: 20px; border-radius: 50%; cursor: pointer; border: 2px solid transparent; flex-shrink: 0; transition: 0.2s; }}
        .dot:hover {{ transform: scale(1.2); }}

        /* STATS */
        .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; padding: 15px; }}
        .stat-box {{ background: var(--card-bg); padding: 10px; border-radius: 12px; text-align: center; border: 1px solid var(--border); cursor: pointer; }}
        .stat-num {{ font-size: 16px; font-weight: bold; display: block; }}
        .stat-label {{ font-size: 10px; opacity: 0.7; text-transform: uppercase; font-weight: 600; }}

        /* LIST */
        .list-container {{ padding: 0 15px; }}
        .item-card {{ background: var(--card-bg); margin-bottom: 10px; border-radius: 12px; padding: 12px; display: flex; align-items: center; border: 1px solid var(--border); cursor: pointer; }}
        .item-card.active-playing {{ border: 2px solid var(--primary); background: var(--light); }}
        .card-icon {{ width: 45px; height: 45px; background: var(--bg); border-radius: 10px; display: flex; justify-content: center; align-items: center; font-size: 20px; margin-right: 12px; color: var(--text); }}
        .card-info {{ flex-grow: 1; min-width: 0; }}
        .card-title {{ font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: var(--text); }}
        .badge {{ font-size: 9px; padding: 2px 6px; border-radius: 4px; font-weight: bold; margin-right: 5px; background: #eee; color: #333; }}
        .progress-bg {{ height: 3px; background: var(--border); margin-top: 8px; border-radius: 2px; width: 100%; }}
        .progress-fill {{ height: 100%; background: var(--primary); width: 0%; }}
        .item-card.watched .status-icon::after {{ content: '✅'; margin-left: 10px; }}

        /* PLAYER MODAL */
        .modal {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 2000; align-items: center; justify-content: center; flex-direction: column; }}
        .modal-content {{ width: 100%; max-width: 900px; position: relative; background: #000; box-shadow: 0 10px 40px rgba(0,0,0,0.5); display: flex; flex-direction: column; }}
        
        .player-header {{ 
            display: flex; justify-content: space-between; padding: 12px 15px; color: white;
            background: linear-gradient(to bottom, rgba(0,0,0,0.9), transparent);
            position: absolute; top: 0; width: 100%; z-index: 20; cursor: move;
        }}
        #playerTitle {{ font-weight: bold; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; max-width: 70%; font-size: 14px; pointer-events: none; }}
        .win-icons {{ display: flex; gap: 15px; pointer-events: auto; }}
        .win-btn {{ cursor: pointer; font-size: 20px; color: #fff; text-shadow: 0 0 5px black; }}
        .close-x {{ font-size: 22px; font-weight: bold; color: #ff4d4d; }}

        .media-box {{ width: 100%; background: #000; display: flex; justify-content: center; align-items: center; min-height: 250px; position: relative; }}
        .pdf-frame {{ width: 100%; height: 80vh; border: none; background: #fff; }}
        .view-img {{ max-width: 100%; max-height: 80vh; object-fit: contain; }}

        /* OVERLAY SEEK BUTTONS */
        .overlay-seek {{
            position: absolute; top: 50%; transform: translateY(-50%);
            background: rgba(0,0,0,0.5); color: white; border: 1px solid rgba(255,255,255,0.2);
            padding: 10px 15px; border-radius: 30px; font-size: 14px; font-weight: bold;
            cursor: pointer; z-index: 15; backdrop-filter: blur(2px); transition: 0.2s;
        }}
        .overlay-seek:hover {{ background: rgba(255,255,255,0.2); }}
        .seek-left {{ left: 20px; }}
        .seek-right {{ right: 20px; }}

        /* CONTROLS */
        .controls-row {{ display: flex; gap: 10px; justify-content: center; padding: 15px; background: #111; flex-wrap: wrap; width: 100%; }}
        .c-btn {{ background: #333; color: white; border: 1px solid #444; padding: 8px 16px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 5px; }}
        .c-btn.primary {{ background: var(--primary); border-color: var(--primary); }}

        /* MINIMIZED */
        body.minimized .modal {{ background: transparent !important; pointer-events: none; justify-content: unset; align-items: unset; }}
        body.minimized .modal-content {{ 
            pointer-events: auto; width: 300px !important; border: 1px solid #444; 
            border-radius: 12px; overflow: hidden; position: fixed; bottom: 80px; right: 20px; 
            box-shadow: 0 5px 20px rgba(0,0,0,0.5); z-index: 3000;
        }}
        body.minimized .controls-row, body.minimized .pdf-frame, body.minimized .view-img, body.minimized .overlay-seek {{ display: none !important; }}
        body.minimized #playerTitle {{ font-size: 12px; }}
        body.minimized .player-header {{ padding: 8px; background: rgba(0,0,0,0.8); cursor: move; }}
        body.minimized .close-x {{ display: none; }}

        #watermark {{ position: absolute; top: 10%; right: 5%; color: rgba(0,0,0,0.5); font-weight: 900; pointer-events: none; z-index: 20; font-size: 18px; text-shadow: none; }}
        #toast {{ position: fixed; bottom: 50px; left: 50%; transform: translateX(-50%); background: #333; color: white; padding: 8px 16px; border-radius: 20px; font-size: 12px; opacity: 0; transition: 0.3s; z-index: 3000; }}
        
        /* Volume Gesture Indicator */
        #volIndicator {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(0,0,0,0.7); padding: 20px; border-radius: 10px; color: white; font-weight: bold; display: none; z-index: 30; }}
    </style>
</head>
<body>
    {login_html}

    <div id="app-wrapper">
        <div class="header">
            <div class="top-row">
                <h2 style="margin:0; font-size:16px;">{title}</h2>
                <div onclick="if(confirm('Clear Data?')) {{ localStorage.clear(); location.reload(); }}" style="cursor:pointer;" title="Reset">🗑️</div>
            </div>
            <div class="color-dots">
                <div class="dot" style="background:#2563eb" onclick="setTheme('blue')"></div>
                <div class="dot" style="background:#dc2626" onclick="setTheme('red')"></div>
                <div class="dot" style="background:#16a34a" onclick="setTheme('green')"></div>
                <div class="dot" style="background:#9333ea" onclick="setTheme('purple')"></div>
                <div class="dot" style="background:#ea580c" onclick="setTheme('orange')"></div>
                <div class="dot" style="background:#db2777" onclick="setTheme('pink')"></div>
                <div class="dot" style="background:#475569" onclick="setTheme('dark')"></div>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-box" onclick="filterList('all')"><span class="stat-num">{len(raw_lines)}</span>All</div>
            <div class="stat-box" onclick="filterList('FAV')" style="color:#ef4444; border-color:#fca5a5"><span class="stat-num" id="favCount">-</span>Fav ❤️</div>
            <div class="stat-box" onclick="filterList('VIDEO')" style="color:var(--primary)"><span class="stat-num">{v_c}</span>Video</div>
            <div class="stat-box" onclick="filterList('AUDIO')" style="color:#0284c7"><span class="stat-num">{a_c}</span>Audio</div>
            <div class="stat-box" onclick="filterList('PDF')" style="color:#10b981"><span class="stat-num">{p_c}</span>PDF</div>
            <div class="stat-box" onclick="filterList('IMAGE')" style="color:#d97706"><span class="stat-num">{i_c}</span>Img</div>
        </div>

        <div class="list-container" style="margin-top:5px;">
            <input type="text" id="searchInput" placeholder="🔍 Search..." onkeyup="searchList()" style="width:100%; padding:12px; border:1px solid var(--border); border-radius:8px; margin-bottom:10px; background:var(--card-bg); color:var(--text); outline:none;">
            <div id="playlistContainer">{items_html}</div>
        </div>

        <div id="vModal" class="modal">
            <div class="modal-content" id="modalContent">
                <div class="player-header" id="dragHandle">
                    <div id="playerTitle">Player</div>
                    <div class="win-icons">
                        <span class="win-btn" onclick="toggleMinimize()">📉</span>
                        <span class="win-btn close-x" onclick="closeModal()">✕</span>
                    </div>
                </div>

                <div class="media-box" id="mediaBox">
                    <div id="watermark">{BOT_OWNER_NAME}</div>
                    <div id="volIndicator">Vol: 100%</div>
                    
                    <div id="vidContainer" style="width:100%; position:relative; display:none;">
                        <div class="overlay-seek seek-left" onclick="seek(-10)">⏪ 10s</div>
                        <div class="overlay-seek seek-right" onclick="seek(10)">10s ⏩</div>
                        
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
                    <button class="c-btn" onclick="setSpeed(1.5)">1.5x</button>
                    <button class="c-btn" onclick="setSpeed(2)">2x</button>
                </div>
            </div>
        </div>
        <div id="toast">Alert</div>
    </div>

    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        function checkPass() {{
            if(document.getElementById('passInput').value === "{SKY_PASSWORD}") {{
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('app-wrapper').style.display = 'block';
            }} else document.getElementById('errMsg').innerText = "❌ Incorrect Key";
        }}
        {security_script}

        const playlist = {js_playlist};
        let currentIndex = -1;
        let hls = new Hls();
        let isMinimized = false;
        
        let currTheme = localStorage.getItem('theme') || 'blue';
        document.documentElement.setAttribute('data-theme', currTheme);

        function setTheme(theme) {{
            currTheme = theme;
            document.documentElement.setAttribute('data-theme', currTheme);
            localStorage.setItem('theme', currTheme);
            showToast("Theme: " + theme.toUpperCase());
        }}

        // --- PLAYER CONFIG WITH 4K SUPPORT ---
        const player = new Plyr('#player', {{
            controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'volume', 'settings', 'fullscreen'],
            settings: ['quality', 'speed'],
            quality: {{ default: 1080, options: [4320, 2160, 1440, 1080, 720, 576, 480, 360, 240] }} // Enable High Res Options
        }});

        // --- VOLUME GESTURE LOGIC ---
        let touchStartY = 0;
        let startVol = 1;
        const mediaBox = document.getElementById('mediaBox');
        
        mediaBox.addEventListener('touchstart', (e) => {{
            if(isMinimized || document.getElementById('vidContainer').style.display === 'none') return;
            // Check if right side
            if(e.touches[0].clientX > window.innerWidth / 2) {{
                touchStartY = e.touches[0].clientY;
                startVol = player.volume;
            }}
        }});

        mediaBox.addEventListener('touchmove', (e) => {{
             if(isMinimized || document.getElementById('vidContainer').style.display === 'none') return;
             // Right side swipe
             if(e.touches[0].clientX > window.innerWidth / 2) {{
                 e.preventDefault();
                 const deltaY = touchStartY - e.touches[0].clientY;
                 const adjustment = deltaY / 200; // Sensitivity
                 let newVol = startVol + adjustment;
                 if(newVol > 1) newVol = 1;
                 if(newVol < 0) newVol = 0;
                 player.volume = newVol;
                 
                 const vInd = document.getElementById('volIndicator');
                 vInd.style.display = 'block';
                 vInd.innerText = 'Vol: ' + Math.round(newVol * 100) + '%';
                 clearTimeout(window.volTimer);
                 window.volTimer = setTimeout(() => vInd.style.display = 'none', 1000);
             }}
        }});

        window.onload = () => {{
            updateFavCount();
            playlist.forEach((item, i) => {{
                if(localStorage.getItem('watched_' + item.url)) {{
                    document.getElementById(`item-${{i}}`).classList.add('watched');
                    const fill = document.getElementById(`prog-${{i}}`);
                    if(fill) fill.style.width = '100%';
                }}
            }});
        }};

        function updateFavCount() {{
            let c = 0;
            playlist.forEach(item => {{ if(localStorage.getItem('fav_' + item.url)) c++; }});
            document.getElementById('favCount').innerText = c;
        }}

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
            }} else if (item.type === 'PDF') {{
                document.getElementById('pdfFrame').style.display = 'block';
                document.getElementById('pdfFrame').src = "https://docs.google.com/gview?embedded=true&url=" + encodeURIComponent(item.url);
            }} else if (item.type === 'IMAGE') {{
                document.getElementById('imgView').style.display = 'block';
                document.getElementById('imgView').src = item.url;
            }} else {{
                window.open(item.url, '_blank');
                closeModal();
            }}
        }}

        function setupVideo(item) {{
            document.getElementById('vidContainer').style.display = 'block';
            document.getElementById('vidControls').style.display = 'flex';
            if (Hls.isSupported() && item.url.includes('.m3u8')) {{
                hls.loadSource(item.url); hls.attachMedia(document.getElementById('player'));
                hls.on(Hls.Events.MANIFEST_PARSED, () => {{
                    // Auto-detect levels including 4K
                    const levels = hls.levels.map(l => l.height);
                    player.config.quality = {{ default: levels[levels.length-1], options: levels, onChange: (q) => hls.currentLevel = hls.levels.findIndex(l => l.height === q) }};
                }});
            }} else {{ document.getElementById('player').src = item.url; }}
            
            const lastTime = localStorage.getItem('prog_' + item.url);
            player.once('canplay', () => {{
                if(lastTime) player.currentTime = parseFloat(lastTime);
                player.play();
                const btn = document.querySelector('#vidControls button:nth-child(5)');
                if(localStorage.getItem('fav_' + item.url)) {{
                    btn.innerText = '❤️ Saved'; btn.style.color = '#ef4444';
                }} else {{
                    btn.innerText = '🤍 Fav'; btn.style.color = 'white';
                }}
            }});
        }}

        // MOVABLE MINIMIZE LOGIC
        function toggleMinimize() {{
            isMinimized = !isMinimized;
            document.body.classList.toggle('minimized', isMinimized);
            if(isMinimized) {{
                const content = document.getElementById('modalContent');
                content.style.left = ''; content.style.top = ''; 
                content.style.bottom = '80px'; content.style.right = '20px';
                makeDraggable(content);
            }}
        }}

        function makeDraggable(element) {{
            const header = document.getElementById('dragHandle');
            let isDragging = false, startX, startY, initialLeft, initialTop;
            header.onmousedown = header.ontouchstart = dragStart;

            function dragStart(e) {{
                if (!isMinimized) return;
                e.preventDefault();
                isDragging = true;
                const clientX = e.clientX || e.touches[0].clientX;
                const clientY = e.clientY || e.touches[0].clientY;
                startX = clientX; startY = clientY;
                const rect = element.getBoundingClientRect();
                initialLeft = rect.left; initialTop = rect.top;
                document.onmouseup = document.ontouchend = dragEnd;
                document.onmousemove = document.ontouchmove = drag;
            }}

            function drag(e) {{
                if (!isDragging) return;
                e.preventDefault();
                const clientX = e.clientX || e.touches[0].clientX;
                const clientY = e.clientY || e.touches[0].clientY;
                const deltaX = clientX - startX;
                const deltaY = clientY - startY;
                element.style.position = 'fixed';
                element.style.bottom = 'auto'; element.style.right = 'auto';
                element.style.left = initialLeft + deltaX + 'px';
                element.style.top = initialTop + deltaY + 'px';
            }}

            function dragEnd() {{ isDragging = false; document.onmouseup = document.ontouchend = null; document.onmousemove = document.ontouchmove = null; }}
        }}

        player.on('timeupdate', () => {{
            const url = playlist[currentIndex].url;
            localStorage.setItem('prog_' + url, player.currentTime);
            if((player.currentTime / player.duration) > 0.9) {{
                localStorage.setItem('watched_' + url, 'true');
                document.getElementById(`item-${{currentIndex}}`).classList.add('watched');
            }}
        }});
        player.on('ended', () => {{ showToast("Next..."); setTimeout(playNext, 1000); }});

        function seek(s) {{ player.currentTime += s; }}
        function playNext() {{ if(currentIndex + 1 < playlist.length) openContent(currentIndex + 1); }}
        function downloadCurrent() {{ window.open(playlist[currentIndex].url, '_blank'); }}
        function setSpeed(s) {{ player.speed = s; showToast(s+"x"); }}
        
        function toggleFav(btn) {{
            const url = playlist[currentIndex].url;
            if(localStorage.getItem('fav_' + url)) {{
                localStorage.removeItem('fav_' + url);
                btn.innerText = '🤍 Fav'; btn.style.color = 'white';
                showToast("Removed from Fav");
            }} else {{
                localStorage.setItem('fav_' + url, 'true');
                btn.innerText = '❤️ Saved'; btn.style.color = '#ef4444';
                showToast("Added to Fav");
            }}
            updateFavCount();
        }}
        
        function closeModal() {{
            player.pause(); if(hls) hls.detachMedia();
            document.getElementById('vModal').style.display = 'none';
            document.getElementById('pdfFrame').src = "";
            document.body.classList.remove('minimized'); isMinimized = false;
        }}

        function filterList(type) {{
            document.querySelectorAll('.item-card').forEach(el => {{
                let show = false;
                if (type === 'all') show = true;
                else if (type === 'FAV') {{
                     const idx = el.id.split('-')[1];
                     const url = playlist[idx].url;
                     if(localStorage.getItem('fav_' + url)) show = true;
                }}
                else if (el.getAttribute('data-type') === type) show = true;
                el.style.display = show ? 'flex' : 'none';
            }});
            showToast("Filter: " + type);
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
    </script>
</body>
</html>
"""

# ================= TELEGRAM HANDLER =================
@app.on_message(filters.command(["start", "stop", "html", "sky", "txt"]))
async def handle_cmds(c, m):
    cmd = m.command[0]
    if cmd == "start":
        return await m.reply_text(f"🔥 **Pro Player Bot**\n\n/html - Normal\n/sky - Secured\n/txt - Links")
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
        out_path = path.rsplit('.', 1)[0] + "_Pro.html"
        with open(out_path, "w", encoding="utf-8") as f: f.write(html_data)
        cap = "🔥 **Ultra Pro Dashboard**\nFeatures: 4K Support, Volume Swipe, Overlay Buttons."
    
    elif mode == "txt":
        links = re.findall(r"(https?://[^\s\n]+)", content)
        out_path = path.rsplit('.', 1)[0] + "_links.txt"
        with open(out_path, "w", encoding="utf-8") as f: f.write("\n".join(links))
        cap = f"📄 Extracted {len(links)} Links"

    await m.reply_document(out_path, caption=cap)
    await msg.delete()
    if os.path.exists(path): os.remove(path)
    if os.path.exists(out_path): os.remove(out_path)

print("🔥 Pro Bot Started...")
app.run()
