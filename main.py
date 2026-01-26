import os
import re
from datetime import datetime
from pyrogram import Client, filters

# ================= CONFIG =================
BOT_OWNER_NAME = "Sachin Yadav & Nitin Yadav"
API_ID = 12475131
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"

# Domain Changer Config
OLD_DOMAINS = ["https://apps-s3-jw-prod.utkarshapp.com/", "https://apps-s3-prod.utkarshapp.com/", "https://apps-s3-video-dist.utkarshapp.com/"]
NEW_DOMAIN = "https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/"

app = Client("domain_pro_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_mode = {}

# Logic: Domain Badalne ke liye
def fix_domain(url):
    for d in OLD_DOMAINS:
        if d in url:
            return url.replace(d, NEW_DOMAIN)
    return url

# Logic: HTML se wapas TXT nikalne ke liye
def html_to_txt(html_content):
    matches = re.findall(r'onclick="window\.open\(\'(.*?)\'\)".*?>(.*?)</div>', html_content)
    extracted = []
    for url, name in matches:
        clean_name = re.sub(r'[🎬📄🔗📂]', '', name).strip()
        extracted.append(f"{clean_name}: {url}")
    return "\n".join(extracted)

# Logic: Professional HTML banane ke liye (Auto-Folder)
def generate_html(file_name, content):
    title = os.path.splitext(file_name)[0]
    now = datetime.now().strftime("%d %b %Y, %I:%M %p")
    lines = content.strip().split("\n")
    v_t, p_t = 0, 0
    folder_data = []
    current_folder = None

    for line in lines:
        line = line.strip()
        if not line or "http" not in line: continue
        name, url = line.split(":", 1) if ":" in line else ("Class", line)
        name, url = name.strip(), fix_domain(url.strip()) # Domain auto-change here
        
        # 1-Count Detection for Folders
        if re.match(r'^(01|1)[\s\.\-]', name) or current_folder is None:
            if current_folder: folder_data.append(current_folder)
            f_name = re.sub(r'^(01|1)[\s\.\-]', '', name).strip()
            current_folder = {"name": f_name, "items": []}

        t = "video" if any(x in url.lower() for x in [".mp4", ".m3u8", ".mpd"]) else "pdf"
        if t == "video": v_t += 1
        else: p_t += 1
        current_folder["items"].append({"name": name, "url": url, "type": t})
            
    if current_folder: folder_data.append(current_folder)

    html_folders = ""
    for idx, f in enumerate(folder_data):
        html_folders += f'''
        <div class="folder" onclick="toggle('f-{idx}')">
            <span>📂 {f['name']}</span>
            <span class="count">{len(f['items'])} Classes</span>
        </div>
        <div id="f-{idx}" class="content" style="display:none;">'''
        for i in f['items']:
            icon = "🎬" if i['type']=="video" else "📄"
            html_folders += f'<div class="item" onclick="window.open(\'{i["url"]}\')">{icon} {i["name"]}</div>'
        html_folders += "</div>"

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
    <style>
        body {{ font-family: sans-serif; background: #f0f2f5; margin: 0; padding-bottom: 40px; }}
        .header {{ background: #fff; padding: 15px; text-align: center; border-bottom: 3px solid #007bff; position: sticky; top: 0; z-index: 100; }}
        .folder {{ background: #fff; margin: 10px; padding: 15px; border-radius: 8px; font-weight: bold; display: flex; justify-content: space-between; cursor: pointer; border: 1px solid #ddd; }}
        .count {{ background: #007bff; color: #fff; padding: 2px 8px; border-radius: 10px; font-size: 11px; }}
        .item {{ background: #fff; margin: 5px 15px; padding: 12px; border-radius: 5px; font-size: 13px; border-left: 4px solid #007bff; cursor: pointer; border-bottom: 1px solid #eee; }}
    </style>
</head>
<body>
    <div class="header">
        <h3 style="margin:0;">{title}</h3>
        <div style="color:#007bff; font-size:12px; font-weight:bold;">🎥 {v_t} Videos | 📄 {p_t} PDFs</div>
        <div style="font-size:10px; color:#888;">{now}</div>
    </div>
    {html_folders}
    <div style="text-align:center; padding:20px; font-size:12px; color:#999;">Created By: {BOT_OWNER_NAME}</div>
    <script>
        function toggle(id) {{ var e = document.getElementById(id); e.style.display = e.style.display === 'none' ? 'block' : 'none'; }}
    </script>
</body>
</html>
"""

# ================= HANDLERS =================
@app.on_message(filters.command("start"))
async def start(c, m):
    await m.reply_text(f"🚀 **Bot Mode: All-In-One**\nOwner: {BOT_OWNER_NAME}\n\nCommands:\n/html - TXT to HTML (Auto Domain Change)\n/txt - HTML to TXT\n/domain - Only Domain Changer (TXT to TXT)")

@app.on_message(filters.command(["html", "txt", "domain"]))
async def mode(c, m):
    user_mode[m.from_user.id] = m.command[0]
    await m.reply_text(f"✅ Mode Switched to: **{m.command[0].upper()}**")

@app.on_message(filters.document)
async def handle(c, m):
    mode = user_mode.get(m.from_user.id, "html")
    path = await m.download()
    
    if mode == "txt":
        with open(path, "r", encoding="utf-8") as f:
            data = html_to_txt(f.read())
        out = path.replace(".html", ".txt")
        with open(out, "w", encoding="utf-8") as f: f.write(data)
    
    elif mode == "domain":
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(path, "w", encoding="utf-8") as f:
            for l in lines: f.write(fix_domain(l))
        out = path
        
    else: # Default: HTML Mode (With Domain Change)
        with open(path, "r", encoding="utf-8") as f:
            html = generate_html(m.document.file_name, f.read())
        out = path.replace(".txt", ".html")
        with open(out, "w", encoding="utf-8") as f: f.write(html)

    await m.reply_document(out, caption=f"✨ Processed by {BOT_OWNER_NAME}")
    os.remove(path)
    if out != path: os.remove(out)

app.run()
