import os
import re
from datetime import datetime
from pyrogram import Client, filters

# ================= CONFIG =================
BOT_OWNER_NAME = "Sachin Yadav & Nitin Yadav"
API_ID = 12475131
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"

# Domain Configuration
OLD_DOMAINS = ["https://apps-s3-jw-prod.utkarshapp.com/", "https://apps-s3-prod.utkarshapp.com/", "https://apps-s3-video-dist.utkarshapp.com/"]
NEW_DOMAIN = "https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/"

app = Client("complete_pro_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_mode = {}

# Logic: Sirf Video links ka domain badalne ke liye
def fix_video_domain(url):
    low = url.lower()
    if any(ext in low for ext in [".mp4", ".m3u8", ".mpd", "/m3u8"]):
        for d in OLD_DOMAINS:
            if d in url: return url.replace(d, NEW_DOMAIN)
    return url

# ================= 1. HTML TO TXT =================
def html_to_txt(html_content):
    # Regex to find links and names from the new structure
    matches = re.findall(r"'(http.*?)'", html_content)
    names = re.findall(r'<span class="name">(.*?)</span>', html_content)
    extracted = []
    for u, n in zip(matches, names):
        extracted.append(f"{n.strip()}: {u}")
    return "\n".join(extracted)

# ================= 2. TXT TO HTML (Filter & Category Style) =================
def generate_html(file_name, content):
    title = os.path.splitext(file_name)[0]
    now = datetime.now().strftime("%d %b %Y")
    lines = content.strip().split("\n")
    
    items_html = ""
    v_c = p_c = a_c = o_c = 0

    for idx, line in enumerate(lines):
        line = line.strip()
        if not line or "http" not in line: continue
        name, url = line.split(":", 1) if ":" in line else ("File", line)
        name, url = name.strip(), fix_video_domain(url.strip())
        
        # Type Detection
        low_u = url.lower()
        if any(x in low_u for x in [".mp4", ".m3u8", ".mpd"]): t = "video"; v_c += 1
        elif ".pdf" in low_u: t = "pdf"; p_c += 1
        elif any(x in low_u for x in [".mp3", ".wav", ".m4a"]): t = "audio"; a_c += 1
        else: t = "other"; o_c += 1

        items_html += f'''
        <div class="item" data-type="{t}" id="item-{idx}">
            <div class="item-info" onclick="{f"playVideo('{url}')" if t=='video' else f"window.open('{url}')"}">
                <span class="icon">{'🎬' if t=='video' else '📄' if t=='pdf' else '🎵' if t=='audio' else '🔗'}</span>
                <span class="name">{name}</span>
            </div>
            <span class="fav-btn" onclick="toggleFav('{idx}')">♡</span>
        </div>'''

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <style>
        body {{ font-family: sans-serif; background: #f0f2f5; margin: 0; padding-bottom: 20px; }}
        .header {{ background: #fff; padding: 15px; text-align: center; border-bottom: 2px solid #007bff; position: sticky; top: 0; z-index: 1000; }}
        .filter-bar {{ display: flex; overflow-x: auto; padding: 10px; background: #fff; gap: 10px; border-bottom: 1px solid #ddd; position: sticky; top: 60px; z-index: 999; }}
        .chip {{ padding: 8px 15px; background: #eee; border-radius: 20px; font-size: 12px; white-space: nowrap; cursor: pointer; font-weight: bold; }}
        .chip.active {{ background: #007bff; color: #fff; }}
        .item {{ background: #fff; margin: 8px 12px; padding: 15px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; border-left: 5px solid #007bff; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
        .item-info {{ flex: 1; display: flex; align-items: center; cursor: pointer; overflow: hidden; }}
        .name {{ font-size: 13px; font-weight: 600; white-space: nowrap; text-overflow: ellipsis; overflow: hidden; }}
        .icon {{ margin-right: 10px; font-size: 20px; }}
        .fav-btn {{ font-size: 24px; color: red; cursor: pointer; margin-left: 10px; }}
        #player-container {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 2000; }}
        .close-p {{ position: absolute; top: 15px; right: 20px; color: white; font-size: 35px; cursor: pointer; z-index: 2001; }}
    </style>
</head>
<body>
    <div id="player-container"><span class="close-p" onclick="closePlayer()">&times;</span><video id="player" playsinline controls></video></div>
    <div class="header">
        <h3 style="margin:0;">{title}</h3>
        <p style="font-size:10px; color:#888; margin:5px 0;">{BOT_OWNER_NAME} | {now}</p>
    </div>
    <div class="filter-bar">
        <div class="chip active" onclick="filter('all', this)">All</div>
        <div class="chip" onclick="filter('video', this)">🎬 Videos ({v_c})</div>
        <div class="chip" onclick="filter('pdf', this)">📄 PDFs ({p_c})</div>
        <div class="chip" onclick="filter('audio', this)">🎵 Audio ({a_c})</div>
        <div class="chip" onclick="filter('fav', this)">❤️ Favorites</div>
    </div>
    <div id="list">{items_html}</div>
    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        const player = new Plyr('#player');
        let favorites = JSON.parse(localStorage.getItem('favs') || '[]');
        function filter(type, el) {{
            document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
            el.classList.add('active');
            document.querySelectorAll('.item').forEach(i => {{
                let id = i.id.split('-')[1];
                if(type === 'all') i.style.display = 'flex';
                else if(type === 'fav') i.style.display = favorites.includes(id) ? 'flex' : 'none';
                else i.style.display = i.getAttribute('data-type') === type ? 'flex' : 'none';
            }});
        }}
        function toggleFav(id) {{
            if(favorites.includes(id)) favorites = favorites.filter(f => f !== id);
            else favorites.push(id);
            localStorage.setItem('favs', JSON.stringify(favorites));
            updateIcons();
        }}
        function updateIcons() {{
            document.querySelectorAll('.item').forEach(i => {{
                let id = i.id.split('-')[1];
                i.querySelector('.fav-btn').innerText = favorites.includes(id) ? '❤️' : '♡';
            }});
        }}
        function playVideo(url) {{
            document.getElementById('player-container').style.display = 'block';
            if (url.includes('.m3u8')) {{ const hls = new Hls(); hls.loadSource(url); hls.attachMedia(document.getElementById('player')); }}
            else {{ document.getElementById('player').src = url; }}
            player.play();
        }}
        function closePlayer() {{ player.pause(); document.getElementById('player-container').style.display = 'none'; }}
        updateIcons();
    </script>
</body>
</html>
"""

# ================= COMMAND HANDLERS =================
@app.on_message(filters.command("start"))
async def start(c, m):
    await m.reply_text(f"👑 **{BOT_OWNER_NAME} Bot Active**\n\n/html - TXT to Filter HTML\n/txt - HTML to TXT\n/domain - Only Video Domain Change")

@app.on_message(filters.command(["html", "txt", "domain"]))
async def mode_selection(c, m):
    user_mode[m.from_user.id] = m.command[0]
    await m.reply_text(f"✅ Mode: **{m.command[0].upper()}**")

@app.on_message(filters.document)
async def handle_document(c, m):
    mode = user_mode.get(m.from_user.id, "html")
    path = await m.download()
    
    if mode == "txt":
        with open(path, "r", encoding="utf-8") as f: data = html_to_txt(f.read())
        out = path.replace(".html", ".txt")
        with open(out, "w", encoding="utf-8") as f: f.write(data)
    elif mode == "domain":
        with open(path, "r", encoding="utf-8") as f: lines = f.readlines()
        with open(path, "w", encoding="utf-8") as f:
            for l in lines:
                if ":" in l:
                    nm, url = l.split(":", 1)
                    f.write(f"{nm}: {fix_video_domain(url.strip())}\n")
                else: f.write(l)
        out = path
    else: # Mode HTML
        with open(path, "r", encoding="utf-8") as f: html = generate_html(m.document.file_name, f.read())
        out = path.replace(".txt", ".html")
        with open(out, "w", encoding="utf-8") as f: f.write(html)

    await m.reply_document(out, caption=f"✨ Done by {BOT_OWNER_NAME}")
    os.remove(path)
    if out != path: os.remove(out)

app.run()
