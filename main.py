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

OLD_DOMAINS = [
    "https://apps-s3-jw-prod.utkarshapp.com/", 
    "https://apps-s3-prod.utkarshapp.com/", 
    "https://apps-s3-video-dist.utkarshapp.com/"
]
NEW_DOMAIN = "https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/"

app = Client("master_ultimate_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_mode = {}

# --- Helper: Fix Domains ---
def fix_domain(url):
    url = url.strip()
    for d in OLD_DOMAINS:
        if d in url: return url.replace(d, NEW_DOMAIN)
    return url

# --- Helper: HTML to TXT (Reverse) ---
def html_to_txt(content):
    pattern = r"openModal\('([^']+)','([^']+)','[^']+'\)"
    matches = re.findall(pattern, content)
    return "\n".join([f"{m[1]}: {m[0]}" for m in matches])

# ================= HTML GENERATOR =================
def generate_html(file_name, content, is_protected=False):
    title = os.path.splitext(file_name)[0]
    raw_lines = re.findall(r"([^:\n]+):?\s*(https?://[^\s\n]+)", content)
    
    organized_data = {}
    for name, url in raw_lines:
        clean_name = name.strip()
        parts = clean_name.split('-')
        # Auto-Detect Subject/Teacher Name
        f_key = parts[1].strip().split(' ')[0] if len(parts) > 1 else "General"
        f_key = re.sub(r'[0-9-]', '', f_key).strip() or "Batch Content"
        
        if f_key not in organized_data: organized_data[f_key] = []
        organized_data[f_key].append((clean_name, fix_domain(url)))

    folder_html = ""
    for f_name, items in sorted(organized_data.items()):
        f_id = re.sub(r'\W+', '', f_name)
        items_list = "".join([
            f'<div class="list-item" onclick="openModal(\'{u}\', \'{n}\', \'{"VIDEO" if any(x in u.lower() for x in [".m3u8",".mp4"]) else "PDF"}\')">'
            f'<div class="item-icon-bg">{"📽️" if any(x in u.lower() for x in [".m3u8",".mp4"]) else "📄"}</div>'
            f'<div class="item-title">{n}</div></div>' for n, u in items
        ])
        folder_html += f'<div class="folder-card"><div class="folder-header" onclick="toggleFolder(\'{f_id}\')"><span>📂 {f_name.upper()} ({len(items)})</span><span id="icon-{f_id}">➕</span></div><div id="{f_id}" class="folder-content">{items_list}</div></div>'

    pass_js = f'let p=prompt("🔐 Enter Key:"); if(p!=="{SKY_PASSWORD}")document.body.innerHTML="<h1>Denied</h1>";' if is_protected else ""

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.plyr.io/3.7.8/plyr.css" />
    <style>
        :root {{ --p: #8e44ad; --bg: #f4f7f6; --c: #fff; }}
        body {{ font-family: sans-serif; background: var(--bg); margin: 0; padding-bottom: 20px; }}
        .header {{ background: var(--c); padding: 15px; text-align: center; border-bottom: 3px solid var(--p); position: sticky; top:0; z-index:100; }}
        .folder-card {{ background: var(--c); margin: 10px 15px; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .folder-header {{ background: var(--p); color: white; padding: 12px 15px; cursor: pointer; display: flex; justify-content: space-between; font-weight: bold; }}
        .folder-content {{ display: none; padding: 5px 0; }}
        .list-item {{ background: var(--c); margin: 5px 10px; padding: 10px; border-radius: 8px; display: flex; align-items: center; border-bottom: 1px solid #eee; cursor: pointer; }}
        .modal {{ display: none; position: fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.95); z-index:999; align-items:center; justify-content:center; }}
        .m-body {{ background: var(--c); width: 95%; max-width: 650px; border-radius: 12px; overflow: hidden; position: relative; }}
        #watermark {{ position: absolute; color: rgba(255,255,255,0.2); font-size: 14px; pointer-events: none; z-index: 1001; font-weight: bold; }}
    </style>
</head>
<body>
    <div id="vModal" class="modal">
        <div class="m-body">
            <div id="watermark">{BOT_OWNER_NAME}</div>
            <div style="padding:10px; display:flex; justify-content:space-between; border-bottom:1px solid #eee;">
                <b id="mT" style="font-size:11px;">Player</b><span onclick="closeModal()" style="cursor:pointer; font-size:24px;">&times;</span>
            </div>
            <div style="position:relative; background:#000;">
                <video id="player" playsinline controls></video>
                <div style="position:absolute; top:40%; left:10px; z-index:10;"><button onclick="player.rewind(10)" style="background:rgba(0,0,0,0.5); color:white; border:none; border-radius:50%; width:40px; height:40px;">⏪</button></div>
                <div style="position:absolute; top:40%; right:10px; z-index:10;"><button onclick="player.forward(10)" style="background:rgba(0,0,0,0.5); color:white; border:none; border-radius:50%; width:40px; height:40px;">⏩</button></div>
            </div>
            <div style="display:flex; justify-content:space-around; padding:10px; background:#eee;">
                <button onclick="player.speed = 1">1x</button><button onclick="player.speed = 1.5">1.5x</button><button onclick="player.speed = 2">2x</button><button onclick="player.requestPictureInPicture()">📺 PiP</button>
            </div>
        </div>
    </div>
    <div class="header"><h2 style="font-size:16px; margin:0; color:var(--p);">{title}</h2><small>{datetime.now().strftime("%d %b %Y")}</small></div>
    <div style="padding:15px;"><input type="text" id="sr" placeholder="Search..." onkeyup="search()" style="width:100%; padding:12px; border-radius:10px; border:1px solid #ddd;"></div>
    <div id="fd">{folder_html}</div>
    <script src="https://cdn.plyr.io/3.7.8/plyr.polyfilled.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script>
        {pass_js}
        const player = new Plyr('#player'); let hls = new Hls();
        function toggleFolder(id) {{ const el=document.getElementById(id); el.style.display = el.style.display==='block'?'none':'block'; }}
        function openModal(u, n, t) {{
            if(t==='VIDEO') {{
                document.getElementById('vModal').style.display='flex'; document.getElementById('mT').innerText=n;
                if(u.includes('.m3u8')) {{ hls.loadSource(u); hls.attachMedia(document.getElementById('player')); }} else {{ document.getElementById('player').src=u; }}
                player.play(); setInterval(()=>{{ document.getElementById('watermark').style.top=Math.random()*70+10+"%"; document.getElementById('watermark').style.left=Math.random()*70+10+"%"; }},5000);
            }} else {{ window.open(u); }}
        }}
        function closeModal() {{ player.pause(); hls.detachMedia(); document.getElementById('vModal').style.display='none'; }}
        function search() {{
            let v=document.getElementById('sr').value.toLowerCase();
            document.querySelectorAll('.list-item').forEach(i=>i.style.display=i.innerText.toLowerCase().includes(v)?'flex':'none');
            if(v.length>0) document.querySelectorAll('.folder-content').forEach(f=>f.style.display="block");
        }}
    </script>
</body>
</html>
"""

# ================= COMMANDS =================
@app.on_message(filters.command(["start", "html", "sky", "domain", "txt"]))
async def cmds(c, m):
    cmd = m.command[0]
    if cmd == "start":
        return await m.reply_text(f"👑 **{BOT_OWNER_NAME} Bot**\n\n/domain - TXT to TXT (Update)\n/html - TXT to HTML\n/sky - Password Lock\n/txt - HTML to TXT")
    user_mode[m.from_user.id] = cmd
    await m.reply_text(f"✅ Mode: **{cmd.upper()}**\nFile Bhejo!")

@app.on_message(filters.document)
async def process(c, m):
    uid = m.from_user.id
    mode = user_mode.get(uid)
    if not mode: return await m.reply_text("Pehle mode select karo!")
    
    path = await m.download()
    with open(path, "r", encoding="utf-8") as f: content = f.read()

    if mode == "txt":
        result = html_to_txt(content)
        out = "Reverse_Links.txt"
        with open(out, "w", encoding="utf-8") as f: f.write(result)
        await m.reply_document(out, caption="✅ HTML to TXT Done!")
    elif mode == "domain":
        lines = re.findall(r"([^:\n]+):?\s*(https?://[^\s\n]+)", content)
        out = "Updated_Links.txt"
        with open(out, "w", encoding="utf-8") as f:
            for n, u in lines: f.write(f"{n.strip()}: {fix_domain(u)}\n")
        await m.reply_document(out, caption="✅ TXT Domain Update Done!")
    else:
        out = path.split('.')[0] + ".html"
        with open(out, "w", encoding="utf-8") as f: f.write(generate_html(m.document.file_name, content, (mode=="sky")))
        await m.reply_document(out, caption="📂 Dashboard Ready!")

    os.remove(path); os.remove(out)

app.run()
