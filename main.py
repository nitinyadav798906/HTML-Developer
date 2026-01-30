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

app = Client("ultimate_bot_final", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
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
    now_date = datetime.now().strftime("%d %b %Y")
    
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
        elif any(x in low_u for x in [".jpg", ".jpeg", ".png", ".webp", ".gif"]): t = "IMAGE"; i_c += 1; icon = "🖼️"
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

    pass_script = ""
    if is_protected:
        pass_script = f"""
        let p = prompt("🔒 Enter Password:");
        if(p !== "{SKY_PASSWORD}") {{ document.body.innerHTML = "<h2 style='text-align:center;margin-top:50px;color:red;'>🚫 ACCESS DENIED</h2>"; throw "Stop"; }}
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
        :root {{ --bg: #f8fafc; --card-bg: #ffffff; --primary: #2563eb; --text: #1e293b; --border: #e2e8f0; }}
        * {{ box-sizing: border-box; -webkit-tap-highlight-color: transparent; }}
        body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding-bottom: 80px; }}
        
        /* HEADER */
        .header {{ 
            background: rgba(255,255,255,0.95); position: sticky; top: 0; z-index: 100; 
            padding: 12px 20px; border-bottom: 1px solid var(--border);
            display: flex; justify-content: space-between; align-items: center;
            backdrop-filter: blur(5px);
        }}
        .header h2 {{ margin: 0; font-size: 16px; color: var(--primary); }}
        .reset-btn {{ font-size: 20px; cursor: pointer; color: #ef4444; margin-left: 15px; }}

        /* STATS */
        .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; padding: 10px 15px; }}
        .stat-box {{ background: var(--card-bg); padding: 10px; border-radius: 8px; text-align: center; border: 1px solid var(--border); cursor: pointer; }}
        .stat-num {{ font-size: 14px; font-weight: bold; display: block; }}
        .stat-label {{ font-size: 9px; color: #64748b; text-transform: uppercase; }}

        /* SEARCH */
        .search-wrap {{ padding: 0 15px 10px; position: sticky; top: 60px; z-index: 90; }}
        #searchInput {{ width: 100%; padding: 12px; border: 1px solid var(--border); border-radius: 8px; outline: none; }}

        /* LIST */
        .list-container {{ padding: 0 15px; }}
        .item-card {{ 
            background: var(--card-bg); margin-bottom: 8px; border-radius: 10px; padding: 12px;
            display: flex; align-items: center; border: 1px solid var(--border); cursor: pointer;
            transition: 0.2s;
        }}
        .item-card:hover {{ border-color: var(--primary); transform: translateY(-2px); }}
        .item-card.active-playing {{ border: 2px solid var(--primary); background: #eff6ff; }}
        
        .card-icon {{ width: 40px; height: 40px; background: #f1f5f9; border-radius: 8px; display: flex; justify-content: center; align-items: center; font-size: 18px; margin-right: 12px; flex-shrink: 0; }}
        .card-info {{ flex-grow: 1; min-width: 0; }}
        .card-title {{ font-size: 14px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
        .badge {{ font-size: 9px; padding: 2px 5px; border-radius: 4px; font-weight: 700; background: #eee; margin-right: 5px; }}
        .badge-VIDEO {{ background: #fee2e2; color: #ef4444; }}
        .badge-PDF {{ background: #dcfce7; color: #10b981; }}
        .badge-IMAGE {{ background: #fef3c7; color: #d97706; }}
        
        .progress-bg {{ height: 3px; background: #e2e8f0; margin-top: 5px; border-radius: 2px; width: 100%; }}
        .progress-fill {{ height: 100%; background: var(--primary); width: 0%; }}
        .item-card.watched .status-icon::after {{ content: '✅'; margin-left: 10px; }}

        /* UNIVERSAL MODAL */
        .modal {{ 
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255, 255, 255, 1); z-index: 2000; flex-direction: column;
        }}
        .modal-header {{ 
            padding: 15px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; background: #fff;
        }}
        .modal-title {{ font-weight: 700; font-size: 15px; max-width: 85%; line-height: 1.4; }}
        .close-btn {{ font-size: 24px; cursor: pointer; color: #666; }}

        /* CONTENT AREA */
        .content-area {{ flex-grow: 1; position: relative; background: #000; display: flex; align-items: center; justify-content: center; overflow: hidden; }}
        
        /* Video Specific */
        #player {{ width: 100%; height: 100%; }}
        .video-controls {{ background: #fff; padding: 10px; border-top: 1px solid #eee; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }}
        
        /* PDF/Image Specific */
        iframe.pdf-frame {{ width: 100%; height: 100%; border: none; background: #fff; }}
        img.view-img {{ max-width: 100%; max-height: 100%; object-fit: contain; }}

        /* Watermark & Overlay */
        #watermark {{ position: absolute; top: 20px; right: 20px; opacity: 0.3; color: white; font-weight: bold; pointer-events: none; z-index: 50; }}
        .dbl-tap-overlay {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; display: flex; }}
        .tap-zone {{ flex: 1; display: flex; align-items: center; justify-content: center; opacity: 0; color: white; background: rgba(0,0,0,0.2); font-size: 24px; transition: opacity 0.2s; }}

        .c-btn {{ background: #f1f5f9; border: 1px solid #e2e8f0; padding: 8px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: 600; }}
        .c-btn.primary {{ background: var(--primary); color: white; }}

        #toast {{ position: fixed; bottom: 30px; left: 50%; transform: translateX(-50%); background: #1e293b; color: white; padding: 8px 16px; border-radius: 20px; font-size: 12px; opacity: 0; transition: 0.3s; z-index: 3000; }}
    </style>
</head>
<body>
    <script>{pass_script}</script>

    <div class="header">
        <div>
            <h2>{title}</h2>
            <small style="color:#666">{len(raw_lines)} Items</small>
        </div>
        <div>
            <span onclick="window.scrollTo(0,0)" style="cursor:pointer; margin-right:15px;">🔝</span>
            <span class="reset-btn" onclick="resetData()" title="Clear Progress">🗑️</span>
        </div>
    </div>

    <div class="stats-grid">
        <div class="stat-box" onclick="filterList('all')"><span class="stat-num">{len(raw_lines)}</span><span class="stat-label">All</span></div>
        <div class="stat-box" onclick="filterList('VIDEO')" style="color:#ef4444"><span class="stat-num">{v_c}</span><span class="stat-label">Video</span></div>
        <div class="stat-box" onclick="filterList('PDF')" style="color:#10b981"><span class="stat-num">{p_c}</span><span class="stat-label">PDF</span></div>
        <div class="stat-box" onclick="filterList('IMAGE')" style="color:#d97706"><span class="stat-num">{i_c}</span><span class="stat-label">Img</span></div>
    </div>

    <div class="search-wrap"><input type="text" id="searchInput" placeholder="🔍 Search..." onkeyup="searchList()"></div>
    <div class="list-container" id="playlistContainer">{items_html}</div>
    <div id="toast">Alert</div>

    <div id="vModal" class="modal">
        <div class="modal-header">
            <div class="modal-title" id="mTitle">Title</div>
            <div class="close-btn" onclick="closeModal()">✕</div>
        </div>
        
        <div class="content-area" id="contentArea">
            <div id="watermark">{BOT_OWNER_NAME}</div>
            
            <div id="vidContainer" style="display:none; width:100%; height:100%; position:relative;">
                <div class="dbl-tap-overlay" id="tapLayer">
                    <div class="tap-zone" id="tapLeft">⏪</div>
                    <div class="tap-zone" id="tapRight">⏩</div>
                </div>
                <video id="player" playsinline controls></video>
            </div>

            <iframe id="pdfFrame" class="pdf-frame" style="display:none;"></iframe>

            <img id="imgView" class="view-img" style="display:none;">
        </div>

        <div class="video-controls" id="vidControls" style="display:none;">
            <button class="c-btn" onclick="seek(-10)">-10s</button>
            <button class="c-btn" onclick="seek(10)">+10s</button>
            <button class="c-btn primary" onclick="playNext()">Next ⏭️</button>
            <button class="c-btn" onclick="downloadCurrent()">⬇️ DL</button>
            <button class="c-btn" onclick="setSpeed(1.5)">1.5x</button>
            <button class="c-btn" onclick="setSpeed(2)">2x</button>
        </div>
    </div>

    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        const playlist = {js_playlist};
        let currentIndex = -1;
        let hls = new Hls();
        
        const player = new Plyr('#player', {{
            controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'volume', 'settings', 'fullscreen'],
            settings: ['quality', 'speed'],
            keyboard: {{ global: true }}
        }});

        window.onload = () => {{ restoreProgressUI(); }};

        function openContent(index) {{
            const item = playlist[index];
            currentIndex = index;
            
            // Highlight
            document.querySelectorAll('.item-card').forEach(el => el.classList.remove('active-playing'));
            document.getElementById(`item-${{index}}`).classList.add('active-playing');
            
            // UI Setup
            const modal = document.getElementById('vModal');
            document.getElementById('mTitle').innerText = item.name;
            modal.style.display = 'flex';
            
            // Hide All First
            document.getElementById('vidContainer').style.display = 'none';
            document.getElementById('vidControls').style.display = 'none';
            document.getElementById('pdfFrame').style.display = 'none';
            document.getElementById('imgView').style.display = 'none';

            if(item.type === 'VIDEO' || item.type === 'AUDIO') {{
                setupVideo(item);
            }} 
            else if (item.type === 'PDF') {{
                setupPDF(item.url);
            }} 
            else if (item.type === 'IMAGE') {{
                setupImage(item.url);
            }} 
            else {{
                window.open(item.url, '_blank');
                closeModal();
            }}
        }}

        function setupVideo(item) {{
            document.getElementById('vidContainer').style.display = 'block';
            document.getElementById('vidControls').style.display = 'flex';
            
            if (Hls.isSupported() && item.url.includes('.m3u8')) {{
                hls.loadSource(item.url); hls.attachMedia(document.getElementById('player'));
            }} else {{ document.getElementById('player').src = item.url; }}
            
            // Restore Progress
            const savedSpeed = localStorage.getItem('pref_speed') || 1;
            player.speed = parseFloat(savedSpeed);
            const lastTime = localStorage.getItem('prog_' + item.url);
            player.once('canplay', () => {{
                if(lastTime) {{ player.currentTime = parseFloat(lastTime); showToast("Resumed"); }}
                player.play();
            }});
            startWatermark();
        }}

        function setupPDF(url) {{
            document.getElementById('pdfFrame').style.display = 'block';
            // Use Google Docs Viewer for Embedded PDF
            document.getElementById('pdfFrame').src = "https://docs.google.com/gview?embedded=true&url=" + encodeURIComponent(url);
        }}

        function setupImage(url) {{
            document.getElementById('imgView').style.display = 'block';
            document.getElementById('imgView').src = url;
        }}

        // --- VIDEO LOGIC ---
        player.on('timeupdate', () => {{
            const url = playlist[currentIndex].url;
            const pct = (player.currentTime / player.duration) * 100;
            localStorage.setItem('prog_' + url, player.currentTime);
            if(!isNaN(pct)) {{
                const fill = document.getElementById(`prog-${{currentIndex}}`);
                if(fill) fill.style.width = `${{pct}}%`;
                if(pct > 90) {{
                    document.getElementById(`item-${{currentIndex}}`).classList.add('watched');
                    localStorage.setItem('watched_' + url, 'true');
                }}
            }}
        }});
        player.on('ratechange', () => {{ localStorage.setItem('pref_speed', player.speed); }});
        player.on('ended', () => {{ showToast("Next..."); setTimeout(playNext, 1500); }});

        function seek(sec) {{ player.currentTime += sec; }}
        function setSpeed(s) {{ player.speed = s; showToast(s + "x"); }}
        function playNext() {{
            let next = currentIndex + 1;
            if(next < playlist.length) openContent(next);
        }}
        function downloadCurrent() {{ window.open(playlist[currentIndex].url, '_blank'); }}

        // --- DOUBLE TAP ---
        let lastTap = 0;
        document.getElementById('tapLayer').addEventListener('click', (e) => {{
            const now = new Date().getTime();
            if (now - lastTap < 300) {{
                if (e.clientX < e.target.offsetWidth / 2) {{ seek(-10); animateTap('tapLeft'); }} 
                else {{ seek(10); animateTap('tapRight'); }}
            }}
            lastTap = now;
        }});
        function animateTap(id) {{
            const el = document.getElementById(id); el.style.opacity = '1';
            setTimeout(() => el.style.opacity = '0', 300);
        }}

        // --- UTILS ---
        function resetData() {{
            if(confirm("🗑️ Clear all progress and history?")) {{
                localStorage.clear();
                location.reload();
            }}
        }}

        function closeModal() {{
            player.pause(); if(hls) hls.detachMedia();
            document.getElementById('vModal').style.display = 'none';
            document.getElementById('pdfFrame').src = ""; // Stop PDF loading
        }}

        function restoreProgressUI() {{
            playlist.forEach((item, i) => {{
                if(localStorage.getItem('watched_' + item.url)) {{
                    document.getElementById(`item-${{i}}`).classList.add('watched');
                    const fill = document.getElementById(`prog-${{i}}`);
                    if(fill) fill.style.width = '100%';
                }}
            }});
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
        return await m.reply_text(f"🌟 **Ultimate Bot Active**\n\n/html - Generate Dashboard\n/sky - Protected Dashboard\n/txt - Extract Links")
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
    
    msg = await m.reply_text("⚡ Processing...")
    path = await m.download()
    with open(path, "r", encoding="utf-8", errors="ignore") as f: content = f.read()
    
    out_path = path + ".html"
    cap = ""

    if mode in ["html", "sky"]:
        html_data = generate_html(m.document.file_name, content, is_protected=(mode=="sky"))
        out_path = path.rsplit('.', 1)[0] + "_Final.html"
        with open(out_path, "w", encoding="utf-8") as f: f.write(html_data)
        cap = "🏆 **World Class Dashboard**\nFeatures: In-App PDF/Image, Reset Data, White Theme, Auto-Resume."
    
    elif mode == "txt":
        links = re.findall(r"(https?://[^\s\n]+)", content)
        out_path = path.rsplit('.', 1)[0] + "_links.txt"
        with open(out_path, "w", encoding="utf-8") as f: f.write("\n".join(links))
        cap = f"📄 Extracted {len(links)} Links"

    await m.reply_document(out_path, caption=cap)
    await msg.delete()
    if os.path.exists(path): os.remove(path)
    if os.path.exists(out_path): os.remove(out_path)

print("🏆 Ultimate Bot Started...")
app.run()
