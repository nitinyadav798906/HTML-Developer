import os
import re
from datetime import datetime
from pyrogram import Client, filters

# ================= CONFIG =================
BOT_OWNER_NAME = "Sachin Yadav & Nitin Yadav"
API_ID = 12475131
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"
SKY_PASSWORD = "7989" 

OLD_DOMAINS = ["https://apps-s3-jw-prod.utkarshapp.com/", "https://apps-s3-prod.utkarshapp.com/", "https://apps-s3-video-dist.utkarshapp.com/"]
NEW_DOMAIN = "https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/"

app = Client("master_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_mode = {}

# --- Utility Functions ---
def fix_domain(url):
    url = url.strip()
    for d in OLD_DOMAINS:
        if d in url: return url.replace(d, NEW_DOMAIN)
    return url

def get_clean_subject(text):
    # Faltu symbols hatane ka logic
    if "-" in text:
        subject = text.split("-")[1].strip().split(" ")[0]
    else:
        subject = text.strip().split(" ")[0]
    subject = re.sub(r'[^\w\u0900-\u097F]', '', subject)
    return subject.upper() if len(subject) > 1 else "BATCH CONTENT"

# ================= HTML GENERATOR =================
def generate_html(file_name, content, is_protected=False):
    title = os.path.splitext(file_name)[0]
    raw_lines = re.findall(r"([^:\n]+):?\s*(https?://[^\s\n]+)", content)
    
    organized_data = {}
    for name, url in raw_lines:
        folder = get_clean_subject(name)
        if folder not in organized_data: organized_data[folder] = []
        organized_data[folder].append((name.strip(), fix_domain(url)))

    folder_html = ""
    for f_name, items in sorted(organized_data.items()):
        f_id = "".join(filter(str.isalnum, f_name))
        items_list = ""
        for n, u in items:
            t = "VIDEO" if any(x in u.lower() for x in [".m3u8", ".mp4", ".mpd"]) else "PDF"
            item_id = "".join(filter(str.isalnum, n))[:15]
            items_list += f'''
            <div class="list-item">
                <div class="info" onclick="openP('{u}', '{n}', '{t}')">
                    <span>{"📽️" if t=="VIDEO" else "📄"}</span>
                    <span class="name">{n}</span>
                </div>
                <div class="btns">
                    <a href="{u}" download>📥</a>
                    <span class="fav" onclick="fav('{item_id}','{u}','{n}','{t}')">🤍</span>
                </div>
            </div>'''
        folder_html += f'<div class="f-card"><div class="f-head" onclick="tg(\'{f_id}\')">📂 {f_name} ({len(items)})</div><div id="{f_id}" class="f-cont">{items_list}</div></div>'

    pass_check = f'let p=prompt("🔐 Key:"); if(p!=="{SKY_PASSWORD}")document.body.innerHTML="<h1>Denied</h1>";' if is_protected else ""

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <style>
        body {{ font-family: sans-serif; background: #f4f7f6; margin: 0; }}
        .nav {{ background: #6c5ce7; color: #fff; padding: 15px; text-align: center; position: sticky; top:0; z-index:100; }}
        .f-card {{ background: #fff; margin: 10px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .f-head {{ padding: 12px; cursor: pointer; font-weight: bold; border-bottom: 1px solid #eee; }}
        .f-cont {{ display: none; background: #fafafa; }}
        .list-item {{ display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee; }}
        .info {{ flex: 1; cursor: pointer; font-size: 13px; }}
        .btns {{ display: flex; gap: 12px; font-size: 18px; }}
        .btns a {{ text-decoration: none; }}
        #vMod {{ display: none; position: fixed; top:0; left:0; width:100%; height:100%; background:#000; z-index:1000; align-items:center; justify-content:center; }}
        #wm {{ position: absolute; color: rgba(255,255,255,0.3); font-size: 14px; z-index: 1001; pointer-events: none; }}
    </style>
</head>
<body>
    <div id="vMod"><div style="width:100%; max-width:700px; position:relative;">
        <div id="wm">{BOT_OWNER_NAME}</div>
        <span onclick="closeP()" style="color:#fff; font-size:30px; position:absolute; top:-40px; right:0; cursor:pointer;">&times;</span>
        <video id="player" playsinline controls></video>
    </div></div>
    <div class="nav"><h3>{title}</h3></div>
    {folder_html}
    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        {pass_check}
        const player = new Plyr('#player'); let hls = new Hls();
        function tg(id) {{ const el=document.getElementById(id); el.style.display=el.style.display==='block'?'none':'block'; }}
        function openP(u, n, t) {{
            if(t==='VIDEO') {{
                document.getElementById('vMod').style.display='flex';
                if(u.includes('.m3u8')) {{ hls.loadSource(u); hls.attachMedia(document.getElementById('player')); }}
                else {{ document.getElementById('player').src=u; }}
                player.play(); setInterval(()=>{{
                    document.getElementById('wm').style.top=Math.random()*80+5+"%";
                    document.getElementById('wm').style.left=Math.random()*80+5+"%";
                }}, 3000);
            }} else {{ window.open(u); }}
        }}
        function closeP() {{ player.pause(); document.getElementById('vMod').style.display='none'; }}
    </script>
</body>
</html>
"""

# ================= BOT HANDLERS =================
@app.on_message(filters.command(["start", "html", "sky", "domain", "txt"]))
async def start_handler(c, m):
    cmd = m.command[0]
    if cmd == "start":
        return await m.reply_text("👑 **Master Bot**\n/domain - Update TXT\n/html - Folders\n/sky - Password\n/txt - Reverse")
    user_mode[m.from_user.id] = cmd
    await m.reply_text(f"✅ Mode: **{cmd.upper()}** - Bhejo file!")

@app.on_message(filters.document)
async def file_handler(c, m):
    mode = user_mode.get(m.from_user.id)
    if not mode: return await m.reply_text("Pehle mode select karo!")
    
    path = await m.download()
    with open(path, "r", encoding="utf-8") as f: content = f.read()

    if mode == "txt":
        matches = re.findall(r"openP\('([^']+)','([^']+)','[^']+'\)", content)
        out = "Links_Extracted.txt"
        with open(out, "w", encoding="utf-8") as f:
            for u, n in matches: f.write(f"{n}: {u}\n")
    elif mode == "domain":
        lines = re.findall(r"([^:\n]+):?\s*(https?://[^\s\n]+)", content)
        out = "Updated_Links.txt"
        with open(out, "w", encoding="utf-8") as f:
            for n, u in lines: f.write(f"{n.strip()}: {fix_domain(u)}\n")
    else:
        out = path.split('.')[0] + ".html"
        with open(out, "w", encoding="utf-8") as f: f.write(generate_html(m.document.file_name, content, (mode=="sky")))

    await m.reply_document(out)
    os.remove(path); os.remove(out)

app.run()
