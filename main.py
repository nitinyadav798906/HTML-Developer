import os
import re
import json
import random
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

app = Client("ultimate_replica_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
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

    # Fake Posters for Cinema Look
    posters = [
        "https://images.unsplash.com/photo-1626814026160-2237a95fc5a0?w=500&auto=format&fit=crop&q=60",
        "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&auto=format&fit=crop&q=60",
        "https://images.unsplash.com/photo-1616530940355-351fabd9524b?w=500&auto=format&fit=crop&q=60"
    ]

    for idx, (name, url) in enumerate(raw_lines):
        url = fix_domain(url.strip())
        name = name.strip()
        low_u = url.lower()
        
        if any(x in low_u for x in [".m3u8", ".mpd", ".mp4"]): t = "VIDEO"; v_c += 1; icon = "🎥"
        elif ".pdf" in low_u: t = "PDF"; p_c += 1; icon = "📑"
        elif any(x in low_u for x in [".jpg", ".jpeg", ".png", ".webp"]): t = "IMAGE"; i_c += 1; icon = "🖼️"
        elif any(x in low_u for x in [".m4a", ".mp3"]): t = "AUDIO"; a_c += 1; icon = "🎧"
        else: t = "OTHER"; icon = "📂"

        # Metadata Simulation
        poster = random.choice(posters)
        rating = round(random.uniform(7.0, 9.8), 1)
        
        playlist_data.append({
            "url": url, "name": name, "type": t,
            "poster": poster, "rating": rating
        })

        items_html += f'''
        <div class="card item-card" id="item-{idx}" data-type="{t}" onclick="initCinema({idx})">
            <div class="card-icon">{icon}</div>
            <div class="card-info">
                <div class="card-title">{name}</div>
                <div class="card-meta">
                    <span class="badge badge-{t}">{t}</span>
                    <span class="meta-tag">⭐ {rating}</span>
                </div>
                <div class="progress-bg"><div class="progress-fill" id="prog-{idx}" style="width: 0%"></div></div>
            </div>
            <div class="status-icon" id="status-{idx}"></div>
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
                <h2 style="color:#2563eb">🔒 Secure Access</h2>
                <input type="password" id="passInput" placeholder="Enter Access Code">
                <button onclick="checkPass()">Unlock</button>
                <p id="errMsg"></p>
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
        :root {{ --bg: #0f172a; --card-bg: #1e293b; --text: #f8fafc; --primary: #3b82f6; --red: #ef4444; }}
        * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
        body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding-bottom: 80px; overflow-x: hidden; }}
        
        #app-wrapper {{ display: none; }} 

        /* --- LOGIN --- */
        #login-screen {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0f172a; z-index: 9999; display: none; justify-content: center; align-items: center; }}
        .login-box {{ background: #1e293b; padding: 25px; border-radius: 12px; text-align: center; border: 1px solid #334155; width: 85%; max-width: 320px; }}
        .login-box input {{ width: 100%; padding: 12px; margin: 15px 0; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: white; outline: none; }}
        .login-box button {{ width: 100%; padding: 12px; background: var(--primary); color: white; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; }}

        /* --- HEADER & LIST --- */
        .header {{ background: var(--card-bg); padding: 15px; position: sticky; top: 0; z-index: 50; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }}
        .list-container {{ padding: 15px; }}
        .item-card {{ background: var(--card-bg); margin-bottom: 10px; border-radius: 10px; padding: 12px; display: flex; align-items: center; border: 1px solid #334155; transition: 0.2s; cursor: pointer; }}
        .item-card.active-playing {{ border: 1px solid var(--primary); background: rgba(37,99,235,0.1); }}
        .card-icon {{ width: 40px; height: 40px; background: rgba(255,255,255,0.05); border-radius: 8px; display: flex; justify-content: center; align-items: center; margin-right: 12px; font-size: 18px; }}
        .card-info {{ flex-grow: 1; min-width: 0; }}
        .card-title {{ font-size: 13px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .badge {{ font-size: 10px; padding: 2px 6px; border-radius: 4px; margin-right: 5px; background: rgba(255,255,255,0.1); }}
        .progress-bg {{ height: 2px; background: #334155; margin-top: 6px; width: 100%; }}
        .progress-fill {{ height: 100%; background: var(--primary); width: 0%; }}

        /* === CINEMA POPUP (Image 6 Style) === */
        .cinema-modal {{
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: #000; z-index: 2000; overflow-y: auto;
        }}
        .poster-bg {{
            position: absolute; top: 0; left: 0; width: 100%; height: 65%;
            background-size: cover; background-position: center;
            mask-image: linear-gradient(to bottom, black 20%, transparent 100%);
            -webkit-mask-image: linear-gradient(to bottom, black 20%, transparent 100%);
            opacity: 0.7; z-index: 1; filter: blur(8px);
        }}
        .cinema-content {{
            position: relative; z-index: 10; padding: 20px; margin-top: 45vh;
            display: flex; flex-direction: column; gap: 15px;
        }}
        .main-poster {{
            width: 140px; height: 200px; border-radius: 8px; box-shadow: 0 10px 40px rgba(0,0,0,0.6);
            object-fit: cover; margin-top: -100px; border: 1px solid rgba(255,255,255,0.2); align-self: center;
        }}
        .c-title {{ font-size: 24px; font-weight: 800; color: white; text-align: center; margin: 10px 0; letter-spacing: 0.5px; }}
        .c-meta {{ display: flex; gap: 10px; justify-content: center; font-size: 12px; color: #cbd5e1; margin-bottom: 20px; }}
        .tag {{ background: rgba(255,255,255,0.15); padding: 5px 10px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.1); }}
        
        /* Cinema Buttons */
        .action-btn {{
            width: 100%; padding: 14px; border-radius: 8px; font-size: 15px; font-weight: 700;
            border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;
        }}
        .btn-play {{ background: white; color: black; margin-bottom: 10px; }}
        .btn-list {{ background: transparent; color: white; border: 1px solid rgba(255,255,255,0.3); }}
        .btn-details {{ background: transparent; color: #94a3b8; font-size: 13px; margin-top: 5px; }}

        /* === PLAYER UI (Image 7 Style) === */
        .player-wrapper {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: black;
            z-index: 3000; display: none; flex-direction: column;
        }}
        .player-top {{ 
            padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; 
            color: white; font-weight: 600; font-size: 14px; position: absolute; top: 0; width: 100%; z-index: 50;
            background: linear-gradient(to bottom, rgba(0,0,0,0.8), transparent);
        }}
        .vid-container {{
            width: 100%; flex-grow: 1; display: flex; align-items: center; justify-content: center; position: relative;
        }}
        
        /* Custom Controls Overlay */
        .custom-controls {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            background: rgba(0,0,0,0.4); z-index: 40; transition: opacity 0.3s;
        }}
        .center-btns {{ display: flex; align-items: center; gap: 40px; }}
        .play-big {{ font-size: 50px; color: white; cursor: pointer; opacity: 0.9; }}
        .skip-big {{ font-size: 30px; color: white; cursor: pointer; opacity: 0.7; }}

        /* Vertical Red Bar (Gesture Feedback) */
        .gesture-bar {{
            position: absolute; width: 6px; height: 100px; background: #ef4444; border-radius: 10px;
            top: 50%; left: 50%; transform: translate(-50%, -50%); display: none;
            box-shadow: 0 0 15px rgba(239,68,68,0.6); z-index: 60;
        }}
        .gesture-text {{
            position: absolute; top: 40%; left: 50%; transform: translate(-50%, -50%);
            color: white; font-weight: bold; font-size: 24px; display: none; z-index: 60; text-shadow: 0 2px 5px black;
        }}

        /* Buttons Row (Image 3 Style) */
        .external-controls {{
            background: #000; padding: 15px; display: flex; justify-content: center; gap: 8px; border-top: 1px solid #222;
        }}
        .ext-btn {{
            background: #1e293b; color: white; border: none; padding: 8px 14px; border-radius: 6px;
            font-size: 12px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 5px;
        }}
        .btn-blue {{ background: #2563eb; }}
        
        /* Hidden Plyr Controls Override */
        .plyr__controls {{ opacity: 0; transition: opacity 0.3s; }}
        .vid-container:hover .plyr__controls {{ opacity: 1; }}
        
        /* Lock Button */
        .lock-btn {{
            position: absolute; bottom: 80px; right: 20px; background: rgba(255,255,255,0.2); 
            padding: 10px; border-radius: 50%; cursor: pointer; color: white; z-index: 50;
        }}

        #login-screen p {{ color: #ef4444; font-size: 12px; margin-top: 10px; }}
    </style>
</head>
<body>
    {login_html}

    <div id="app-wrapper">
        <div class="header">
            <div><h2>{title}</h2><small style="color:#64748b">{len(raw_lines)} Items</small></div>
        </div>

        <div class="list-container">
            <input type="text" id="searchInput" placeholder="Search..." onkeyup="searchList()" style="width:100%; padding:12px; border-radius:8px; border:1px solid #334155; background:#1e293b; color:white; margin-bottom:15px;">
            <div id="playlistContainer">{items_html}</div>
        </div>
    </div>

    <div id="cinemaModal" class="cinema-modal">
        <div style="position:absolute; top:20px; left:20px; z-index:50; color:white; font-size:24px; cursor:pointer;" onclick="closeCinema()">✕</div>
        <div class="poster-bg" id="bgPoster"></div>
        
        <div class="cinema-content">
            <img src="" class="main-poster" id="mainPoster">
            <div class="c-title" id="mTitle">Movie Title</div>
            <div class="c-meta">
                <span class="tag" id="mRating">⭐ 7.2</span>
                <span class="tag">2025</span>
                <span class="tag" id="mType">Video</span>
            </div>
            
            <button class="action-btn btn-play" onclick="startPlayback()">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="black"><path d="M8 5v14l11-7z"/></svg> Watch Now
            </button>
            <button class="action-btn btn-list" onclick="toggleWatchlist()" id="wlBtn">
                + Add to Watchlist
            </button>
            <button class="action-btn btn-details">Show More Details ⌄</button>
            
            <div style="color:#94a3b8; font-size:13px; line-height:1.5; margin-top:10px;">
                Experience high-quality streaming. This content is protected and optimized for the best viewing experience.
            </div>
        </div>
    </div>

    <div id="playerWrapper" class="player-wrapper">
        <div class="player-top">
            <span id="pTitle" style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:80%;">Player</span>
            <span onclick="closePlayer()" style="font-size:24px; cursor:pointer;">✕</span>
        </div>

        <div class="vid-container" id="vidArea">
            <div id="gestureBar" class="gesture-bar"></div>
            <div id="gestureText" class="gesture-text">50%</div>

            <div class="custom-controls" id="overlayControls">
                <div class="center-btns">
                    <div class="skip-big" onclick="seek(-10)">⏮</div>
                    <div class="play-big" onclick="togglePlay()" id="centerPlayBtn">▶</div>
                    <div class="skip-big" onclick="seek(10)">⏭</div>
                </div>
            </div>

            <div class="lock-btn" onclick="toggleLock()">🔓</div>

            <video id="player" playsinline controls style="width:100%; max-height:100%;"></video>
            
            <iframe id="pdfFrame" style="width:100%; height:100%; border:none; background:white; display:none;"></iframe>
            <img id="imgView" style="width:100%; height:100%; object-fit:contain; display:none;">
        </div>

        <div class="external-controls" id="extControls">
            <button class="ext-btn" onclick="seek(-10)">-10s</button>
            <button class="ext-btn" onclick="seek(10)">+10s</button>
            <button class="ext-btn btn-blue" onclick="playNext()">Next ⏭</button>
            <button class="ext-btn" onclick="downloadCurrent()">⬇ DL</button>
            <button class="ext-btn" onclick="changeSpeed()">1.5x</button>
        </div>
    </div>

    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        function checkPass() {{
            if(document.getElementById('passInput').value === "{SKY_PASSWORD}") {{
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('app-wrapper').style.display = 'block';
            }} else document.getElementById('errMsg').innerText = "Incorrect Code";
        }}
        {security_script}

        const playlist = {js_playlist};
        let currentIndex = -1;
        let hls = new Hls();
        let isLocked = false;
        
        const player = new Plyr('#player', {{
            controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'settings', 'fullscreen'],
            hideControls: true // We use our custom overlay mostly
        }});

        // --- CINEMA MODE ---
        function initCinema(index) {{
            const item = playlist[index];
            currentIndex = index;
            
            document.getElementById('bgPoster').style.backgroundImage = `url('${{item.poster}}')`;
            document.getElementById('mainPoster').src = item.poster;
            document.getElementById('mTitle').innerText = item.name;
            document.getElementById('mRating').innerText = "⭐ " + item.rating;
            document.getElementById('mType').innerText = item.type;
            
            const wlBtn = document.getElementById('wlBtn');
            if(localStorage.getItem('fav_'+item.url)) {{
                wlBtn.innerText = "✓ Added to Watchlist"; wlBtn.style.border = "1px solid #3b82f6";
            }} else {{
                wlBtn.innerText = "+ Add to Watchlist"; wlBtn.style.border = "1px solid rgba(255,255,255,0.3)";
            }}

            document.getElementById('cinemaModal').style.display = 'block';
        }}

        function closeCinema() {{ document.getElementById('cinemaModal').style.display = 'none'; }}

        // --- PLAYER LOGIC ---
        function startPlayback() {{
            document.getElementById('cinemaModal').style.display = 'none';
            document.getElementById('playerWrapper').style.display = 'flex';
            document.getElementById('pTitle').innerText = playlist[currentIndex].name;
            
            const item = playlist[currentIndex];
            const vidArea = document.getElementById('player');
            const pdf = document.getElementById('pdfFrame');
            const img = document.getElementById('imgView');
            const ext = document.getElementById('extControls');

            vidArea.style.display = 'none'; pdf.style.display = 'none'; img.style.display = 'none';
            ext.style.display = 'none';

            if(item.type === 'VIDEO' || item.type === 'AUDIO') {{
                vidArea.style.display = 'block'; ext.style.display = 'flex';
                if(Hls.isSupported() && item.url.includes('.m3u8')) {{
                    hls.loadSource(item.url); hls.attachMedia(vidArea);
                }} else {{ vidArea.src = item.url; }}
                player.play();
            }} else if(item.type === 'PDF') {{
                pdf.style.display = 'block';
                pdf.src = "https://docs.google.com/gview?embedded=true&url=" + encodeURIComponent(item.url);
            }} else if(item.type === 'IMAGE') {{
                img.style.display = 'block'; img.src = item.url;
            }} else {{
                window.open(item.url, '_blank'); closePlayer();
            }}
        }}

        function closePlayer() {{
            player.pause();
            document.getElementById('playerWrapper').style.display = 'none';
        }}

        // --- GESTURES (Volume/Bright) ---
        let startY = 0;
        let startVal = 0;
        const touchArea = document.getElementById('vidArea');
        const bar = document.getElementById('gestureBar');
        const txt = document.getElementById('gestureText');

        touchArea.addEventListener('touchstart', (e) => {{
            if(isLocked) return;
            startY = e.touches[0].clientY;
            if(e.touches[0].clientX > window.innerWidth / 2) startVal = player.volume; // Right = Vol
            else startVal = 100; // Left = Bright (Simulated)
        }});

        touchArea.addEventListener('touchmove', (e) => {{
            if(isLocked) return;
            e.preventDefault();
            const delta = startY - e.touches[0].clientY;
            const percent = delta / 300;
            
            bar.style.display = 'block'; txt.style.display = 'block';
            
            if(e.touches[0].clientX > window.innerWidth / 2) {{
                // Volume
                let v = startVal + percent;
                if(v > 1) v = 1; if(v < 0) v = 0;
                player.volume = v;
                txt.innerText = Math.round(v*100) + "%";
                bar.style.height = (v*100) + "px";
            }} else {{
                // Brightness
                let b = 100 + (percent * 100);
                if(b < 20) b = 20; if(b > 150) b = 150;
                document.getElementById('playerWrapper').style.filter = `brightness(${{b}}%)`;
                txt.innerText = "☀ " + Math.round(b) + "%";
                bar.style.height = (b/1.5) + "px";
            }}
        }});

        touchArea.addEventListener('touchend', () => {{
            setTimeout(() => {{ bar.style.display = 'none'; txt.style.display = 'none'; }}, 500);
        }});

        // --- CONTROLS ---
        function togglePlay() {{
            if(player.playing) {{ player.pause(); document.getElementById('centerPlayBtn').innerText = "▶"; }}
            else {{ player.play(); document.getElementById('centerPlayBtn').innerText = "⏸"; }}
        }}
        player.on('play', () => document.getElementById('centerPlayBtn').innerText = "⏸");
        player.on('pause', () => document.getElementById('centerPlayBtn').innerText = "▶");

        function seek(s) {{ player.currentTime += s; }}
        function playNext() {{ if(currentIndex+1 < playlist.length) initCinema(currentIndex+1); }}
        function downloadCurrent() {{ window.open(playlist[currentIndex].url, '_blank'); }}
        function changeSpeed() {{ 
            if(player.speed === 1) player.speed = 1.5; 
            else if(player.speed === 1.5) player.speed = 2; 
            else player.speed = 1;
        }}
        
        function toggleLock() {{
            isLocked = !isLocked;
            const btn = document.querySelector('.lock-btn');
            const overlay = document.getElementById('overlayControls');
            const ext = document.getElementById('extControls');
            
            if(isLocked) {{
                btn.innerText = "🔒"; overlay.style.display = 'none'; ext.style.pointerEvents = 'none'; ext.style.opacity = '0.5';
            }} else {{
                btn.innerText = "🔓"; overlay.style.display = 'flex'; ext.style.pointerEvents = 'auto'; ext.style.opacity = '1';
            }}
        }}

        function toggleWatchlist() {{
            const url = playlist[currentIndex].url;
            const btn = document.getElementById('wlBtn');
            if(localStorage.getItem('fav_'+url)) {{
                localStorage.removeItem('fav_'+url);
                btn.innerText = "+ Add to Watchlist"; btn.style.border = "1px solid rgba(255,255,255,0.3)";
            }} else {{
                localStorage.setItem('fav_'+url, 'true');
                btn.innerText = "✓ Added to Watchlist"; btn.style.border = "1px solid #3b82f6";
            }}
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
        return await m.reply_text(f"🔥 **Replica Bot Ready**\n\n/html - Normal\n/sky - Locked\n/txt - Links")
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
        out_path = path.rsplit('.', 1)[0] + "_Replica.html"
        with open(out_path, "w", encoding="utf-8") as f: f.write(html_data)
        cap = "🔥 **True Copy Dashboard Generated**\nIncludes Cinema Popup, MX Player Gestures & Red Accents."
    
    elif mode == "txt":
        links = re.findall(r"(https?://[^\s\n]+)", content)
        out_path = path.rsplit('.', 1)[0] + "_links.txt"
        with open(out_path, "w", encoding="utf-8") as f: f.write("\n".join(links))
        cap = f"📄 Extracted {len(links)} Links"

    await m.reply_document(out_path, caption=cap)
    await msg.delete()
    if os.path.exists(path): os.remove(path)
    if os.path.exists(out_path): os.remove(out_path)

print("🔥 Replica Bot Started...")
app.run()
