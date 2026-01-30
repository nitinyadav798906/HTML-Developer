import os
import re
import json
from datetime import datetime
from pyrogram import Client, filters

# ================= CONFIG =================
BOT_OWNER_NAME = "Sachin & Nitin"
API_ID = 12475131
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"
SKY_PASSWORD = "7989"

OLD_DOMAINS = ["https://apps-s3-jw-prod.utkarshapp.com/", "https://apps-s3-prod.utkarshapp.com/", "https://apps-s3-video-dist.utkarshapp.com/"]
NEW_DOMAIN = "https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/"

app = Client("ultimate_final_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_mode = {}

def fix_domain(url):
    low = url.lower()
    if any(x in low for x in [".m3u8", ".mpd", ".mp4", "/m3u8"]):
        for d in OLD_DOMAINS:
            if d in url: return url.replace(d, NEW_DOMAIN)
    return url

# ================= HTML MASTER GENERATOR =================
def generate_html(file_name, content, is_protected=False):
    title = os.path.splitext(file_name)[0]
    now_date = datetime.now().strftime("%d %b %Y")
    
    # Extract Links
    raw_lines = re.findall(r"([^:\n]+):?\s*(https?://[^\s\n]+)", content)
    v_c = p_c = a_c = 0
    items_html = ""
    playlist_data = []

    for idx, (name, url) in enumerate(raw_lines):
        url = fix_domain(url.strip())
        name = name.strip()
        low_u = url.lower()
        
        if any(x in low_u for x in [".m3u8", ".mpd", ".mp4"]): t = "VIDEO"; v_c += 1; icon = "📽️"
        elif ".pdf" in low_u: t = "PDF"; p_c += 1; icon = "📄"
        elif any(x in low_u for x in [".m4a", ".mp3"]): t = "AUDIO"; a_c += 1; icon = "🎵"
        else: t = "OTHER"; icon = "📁"

        playlist_data.append({"url": url, "name": name, "type": t})

        # ID add kiya taaki JS se style change kar sakein
        items_html += f'''
        <div class="list-item" id="item-{idx}" data-url="{url}" data-type="{t}" onclick="playFromList({idx})">
            <div class="item-icon-bg">{icon}</div>
            <div class="item-details">
                <div class="item-title">{name}</div>
                <div class="item-meta">
                    <span>Type: {t}</span>
                    <span class="watched-badge" id="badge-{idx}" style="display:none;">✅ WATCHED</span>
                </div>
            </div>
        </div>'''

    js_playlist = json.dumps(playlist_data)

    pass_logic = f"""
    let pass = prompt("🔐 Enter Access Key:");
    if(pass !== "{SKY_PASSWORD}") {{ document.body.innerHTML = "<h1 style='color:red;text-align:center;margin-top:20%;'>❌ Access Denied</h1>"; throw "Stop"; }}
    """ if is_protected else ""

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <style>
        :root {{ --bg: #f4f7f6; --text: #333; --card: #ffffff; --purple: #6c5ce7; --green: #00b894; }}
        .dark-mode {{ --bg: #1e1e2e; --text: #e0e0e0; --card: #2d2d44; --purple: #a29bfe; }}
        
        body {{ font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding-bottom: 40px; transition: 0.3s; }}
        
        .header {{ background: var(--card); padding: 15px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); position: sticky; top:0; z-index:100; }}
        
        .dashboard {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; padding: 15px; }}
        .card {{ background: var(--card); padding: 15px; border-radius: 12px; border-left: 4px solid var(--purple); cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,0.05); text-align: center; }}
        
        .list-item {{ background: var(--card); margin: 8px 15px; padding: 12px; border-radius: 12px; display: flex; align-items: center; border: 1px solid transparent; cursor: pointer; transition: 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.03); }}
        .list-item:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
        
        /* Active & Watched Styles */
        .active-playing {{ border: 2px solid var(--purple) !important; background: rgba(108, 92, 231, 0.05) !important; }}
        .watched-item {{ opacity: 0.7; }}
        .watched-badge {{ font-size: 10px; background: var(--green); color: white; padding: 2px 6px; border-radius: 4px; margin-left: 10px; }}

        .item-icon-bg {{ width: 40px; height: 40px; background: rgba(108,92,231,0.1); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 15px; font-size: 18px; }}
        
        /* Modal & Player */
        .modal {{ display: none; position: fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.95); z-index:999; align-items:center; justify-content:center; flex-direction:column; backdrop-filter: blur(5px); }}
        .m-body {{ background: #000; width: 100%; max-width: 900px; overflow: hidden; position: relative; box-shadow: 0 0 30px rgba(108,92,231,0.3); }}
        
        #watermark {{ position: absolute; color: rgba(255,255,255,0.4); font-size: 14px; pointer-events: none; z-index: 20; font-weight: bold; }}
        
        /* Control Buttons */
        .ctrl-row {{ display: flex; justify-content: center; background: #111; padding: 10px; gap: 10px; flex-wrap: wrap; }}
        .btn {{ border: none; background: #333; color: #fff; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 13px; transition: 0.2s; display: flex; align-items: center; gap: 5px; }}
        .btn:hover {{ background: #444; }}
        .btn-primary {{ background: var(--purple); }}
        .btn-primary:hover {{ background: #5649c0; }}
        
        /* Toast */
        #toast {{ visibility: hidden; min-width: 250px; background-color: #333; color: #fff; text-align: center; border-radius: 8px; padding: 12px; position: fixed; z-index: 1000; left: 50%; bottom: 30px; transform: translateX(-50%); }}
        #toast.show {{ visibility: visible; animation: fadein 0.5s, fadeout 0.5s 2.5s; }}
        @keyframes fadein {{ from {{bottom: 0; opacity: 0;}} to {{bottom: 30px; opacity: 1;}} }}
        @keyframes fadeout {{ from {{bottom: 30px; opacity: 1;}} to {{bottom: 0; opacity: 0;}} }}
    </style>
</head>
<body>
    <div id="toast">Notification</div>

    <div id="vModal" class="modal">
        <div class="m-body">
            <div id="watermark">{BOT_OWNER_NAME}</div>
            <div style="padding:10px 20px; display:flex; justify-content:space-between; align-items:center; background:#1e1e1e; color:white;">
                <b id="mT" style="font-size:14px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:80%;">Player</b>
                <span onclick="closeModal()" style="cursor:pointer; font-size:24px;">&times;</span>
            </div>
            
            <video id="player" playsinline controls></video>
            
            <div class="ctrl-row">
                <button class="btn" onclick="seek(-10)">⏪ -10s</button>
                <button class="btn" onclick="seek(10)">+10s ⏩</button>
                <button class="btn btn-primary" onclick="playNext()">Next ⏭️</button>
                <button class="btn" onclick="downloadVid()">⬇️ DL</button>
                <button class="btn" onclick="toggleFav(this)">🤍</button>
            </div>
            <div class="ctrl-row" style="padding-top:0;">
                <button class="btn" onclick="changeSpeed(1.25, this)">1.25x</button>
                <button class="btn" onclick="changeSpeed(1.5, this)">1.5x</button>
                <button class="btn" onclick="changeSpeed(2, this)">2x</button>
            </div>
        </div>
    </div>

    <div class="header">
        <h2 style="margin:0; color:var(--purple);">{title}</h2>
        <div style="font-size:12px; color:#777; margin-top:5px;">
            <span onclick="document.body.classList.toggle('dark-mode')" style="cursor:pointer;">🌓 Switch Theme</span>
        </div>
    </div>

    <div class="dashboard">
        <div class="card" onclick="runFilter('all')"><b>{len(raw_lines)}</b><br><small>All</small></div>
        <div class="card" onclick="runFilter('VIDEO')" style="border-left-color:#e74c3c;"><b style="color:#e74c3c;">{v_c}</b><br><small>Videos</small></div>
    </div>

    <div style="padding:0 15px;">
        <input type="text" id="searchInput" placeholder="Search lessons..." onkeyup="search()" style="width:100%; padding:12px; border-radius:8px; border:1px solid #ddd; outline:none; background:var(--card); color:var(--text); box-sizing: border-box;">
    </div>
    
    <div id="itemList">{items_html}</div>

    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        {pass_logic}
        const playlist = {js_playlist};
        let currentIndex = -1;
        let currentVidUrl = "";
        
        // Setup Player with Chromecast
        const player = new Plyr('#player', {{ 
            controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'volume', 'captions', 'settings', 'pip', 'airplay', 'fullscreen'],
            settings: ['quality', 'speed'],
            keyboard: {{ global: true }}
        }});
        
        let hls = new Hls();

        // --- INIT: Check Watched Status ---
        window.onload = function() {{
            playlist.forEach((item, idx) => {{
                if(localStorage.getItem('watched_' + item.url)) {{
                    markUIWatched(idx);
                }}
            }});
        }};

        function playFromList(idx) {{
            currentIndex = idx;
            const item = playlist[idx];
            
            // UI Updates
            document.querySelectorAll('.list-item').forEach(i => i.classList.remove('active-playing'));
            const el = document.getElementById('item-' + idx);
            if(el) el.classList.add('active-playing');

            openModal(item.url, item.name, item.type);
        }}

        function openModal(url, name, type) {{
            if(type === 'VIDEO') {{
                currentVidUrl = url;
                document.getElementById('vModal').style.display = 'flex';
                document.getElementById('mT').innerText = name;
                
                if(url.includes('.m3u8')) {{
                    hls.loadSource(url); hls.attachMedia(document.getElementById('player'));
                    hls.on(Hls.Events.MANIFEST_PARSED, () => {{
                        const q = hls.levels.map(l => l.height);
                        player.config.quality = {{ default: q[0], options: q, onChange: v => hls.currentLevel = hls.levels.findIndex(l => l.height === v) }};
                    }});
                }} else {{ document.getElementById('player').src = url; }}
                
                // Resume & Watched Logic
                const savedTime = localStorage.getItem(url);
                player.once('canplay', () => {{
                    if (savedTime) {{ player.currentTime = parseFloat(savedTime); showToast("Resumed"); }}
                    player.play();
                }});
                
                player.on('timeupdate', () => {{
                    localStorage.setItem(url, player.currentTime);
                    // Mark watched if > 90%
                    if(player.duration > 0 && (player.currentTime / player.duration) > 0.9) {{
                        markAsWatched(url, currentIndex);
                    }}
                }});

                player.on('ended', () => {{ playNext(); }});
                startWatermark();

            }} else {{ window.open(url); }}
        }}

        function markAsWatched(url, idx) {{
            if(!localStorage.getItem('watched_' + url)) {{
                localStorage.setItem('watched_' + url, 'true');
                markUIWatched(idx);
            }}
        }}

        function markUIWatched(idx) {{
            const badge = document.getElementById('badge-' + idx);
            const item = document.getElementById('item-' + idx);
            if(badge) badge.style.display = 'inline-block';
            if(item) item.classList.add('watched-item');
        }}

        function playNext() {{
            let nextIdx = currentIndex + 1;
            while(nextIdx < playlist.length && playlist[nextIdx].type !== 'VIDEO') nextIdx++;
            if(nextIdx < playlist.length) {{
                showToast("Playing Next...");
                playFromList(nextIdx);
            }} else {{ showToast("Playlist Finished!"); }}
        }}

        function seek(s) {{ player.currentTime += s; }}
        function downloadVid() {{ window.open(currentVidUrl, '_blank'); }}
        function changeSpeed(s, b) {{ player.speed = s; }}
        
        function toggleFav(btn) {{
            btn.innerText = btn.innerText === '🤍' ? '❤️' : '🤍';
            btn.style.color = btn.innerText === '❤️' ? '#e74c3c' : 'white';
        }}

        function showToast(msg) {{
            const x = document.getElementById("toast");
            x.innerText = msg; x.className = "show";
            setTimeout(() => x.className = x.className.replace("show", ""), 3000);
        }}

        function startWatermark() {{
            const w = document.getElementById('watermark');
            setInterval(() => {{
                w.style.top = Math.random() * 80 + 10 + "%";
                w.style.left = Math.random() * 80 + 10 + "%";
            }}, 5000);
        }}

        function closeModal() {{ player.pause(); hls.detachMedia(); document.getElementById('vModal').style.display = 'none'; }}
        function runFilter(t) {{ document.querySelectorAll('.list-item').forEach(i => i.style.display = (t === 'all' || i.getAttribute('data-type') === t) ? 'flex' : 'none'); }}
        function search() {{
            let v = document.getElementById('searchInput').value.toLowerCase();
            document.querySelectorAll('.list-item').forEach(i => i.style.display = i.innerText.toLowerCase().includes(v) ? 'flex' : 'none');
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
        return await m.reply_text(f"👑 {BOT_OWNER_NAME} Bot Active\n\n/html - Normal Dashboard\n/sky - Password Protected\n/txt - Link Extractor\n/stop - Reset Bot")
    if cmd == "stop":
        user_mode.pop(m.from_user.id, None)
        return await m.reply_text("🛑 Process Stopped & Memory Cleared.")
    user_mode[m.from_user.id] = cmd
    await m.reply_text(f"✅ Mode Set: {cmd.upper()}\nAb .txt file bhejo!")

@app.on_message(filters.document)
async def process_file(c, m):
    uid = m.from_user.id
    mode = user_mode.get(uid)
    if not mode: return await m.reply_text("❌ Select Mode First!")
    
    path = await m.download()
    with open(path, "r", encoding="utf-8") as f: content = f.read()
    
    if mode in ["html", "sky"]:
        out = path.split('.')[0] + ".html"
        with open(out, "w", encoding="utf-8") as f:
            f.write(generate_html(m.document.file_name, content, is_protected=(mode == "sky")))
        cap = "🔒 Protected (Pass: 7989)" if mode == "sky" else "✨ Normal Dashboard"
    
    elif mode == "txt":
        links = re.findall(r"(https?://[^\s\n]+)", content)
        out = path.split('.')[0] + "_links.txt"
        with open(out, "w", encoding="utf-8") as f: f.write("\n".join(links))
        cap = "📄 Links Extracted"

    await m.reply_document(out, caption=f"{cap}\nBy: {BOT_OWNER_NAME}")
    os.remove(path); os.remove(out)

print("Ultimate Bot Started...")
app.run()
