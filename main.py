import os
from datetime import datetime
from pyrogram import Client, filters

# ================= CONFIG =================
BOT_OWNER_NAME = "Sachin Yadav & Nitin Yadav"
API_ID = 12475131
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"
TELEGRAM_LINK = "https://t.me/Raftaarss_don"

OLD_DOMAINS = [
    "https://apps-s3-jw-prod.utkarshapp.com/",
    "https://apps-s3-prod.utkarshapp.com/",
    "https://apps-s3-video-dist.utkarshapp.com/"
    "https://apps-s3-media.utkarshapp.com/"
]
NEW_DOMAIN = "https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/"

app = Client("pro_brand_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user_mode = {}

def replace_domains(text: str):
    for d in OLD_DOMAINS:
        text = text.replace(d, NEW_DOMAIN)
    return text

# ================= HTML GENERATOR =================
def generate_html(file_name, content):
    title = os.path.splitext(file_name)[0]
    now_full = datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
    lines = content.strip().split("\n")

    v_total, p_total, a_total, o_total = 0, 0, 0, 0
    folder_data = []
    current_folder = {"name": "General Content", "items": []}

    for line in lines:
        line = line.strip()
        if not line: continue
        
        if ":" in line and "http" in line:
            name, url = line.split(":", 1)
            name, url = name.strip(), replace_domains(url.strip())
            low = url.lower()
            
            # Determine Type
            if any(x in low for x in [".mp4", ".m3u8", ".mpd"]): 
                item_type = "video"; v_total += 1
            elif ".pdf" in low: 
                item_type = "pdf"; p_total += 1
            elif any(x in low for x in [".mp3", ".m4a"]): 
                item_type = "audio"; a_total += 1
            else: 
                item_type = "other"; o_total += 1
                
            current_folder["items"].append({"name": name, "url": url, "type": item_type})
        else:
            if current_folder["items"]:
                folder_data.append(current_folder)
            current_folder = {"name": line, "items": []}
    
    if current_folder["items"]:
        folder_data.append(current_folder)

    html_content = ""
    for idx, folder in enumerate(folder_data):
        html_content += f'''
        <div class="folder-wrapper">
            <div class="chapter-header" onclick="toggleFolder('folder-{idx}')">
                📁 {folder['name']} ({len(folder['items'])})
            </div>
            <div id="folder-{idx}" class="folder-content" style="display:none;">
                <div class="filter-tabs">
                    <button onclick="filterType('folder-{idx}', 'all')">All</button>
                    <button onclick="filterType('folder-{idx}', 'video')">Videos</button>
                    <button onclick="filterType('folder-{idx}', 'pdf')">PDFs</button>
                    <button onclick="filterType('folder-{idx}', 'audio')">Audio</button>
                </div>
        '''
        for item in folder['items']:
            icon = "🎬" if item['type']=="video" else "📄" if item['type']=="pdf" else "🎵" if item['type']=="audio" else "🔗"
            html_content += f'''
            <div class="chapter-item list-item" data-type="{item['type']}" onclick="window.open('{item['url']}', '_blank')">
                {icon} {item['name']}
            </div>'''
        html_content += "</div></div>"

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{ --bg: #ffffff; --text: #000; --card: #000; --card-text: #fff; --item: #f1f1f1; }}
        .dark-mode {{ --bg: #121212; --text: #fff; --card: #1f1f1f; --item: #222; }}
        body {{ font-family: sans-serif; background: var(--bg); color: var(--text); margin: 0; text-align: center; transition: 0.3s; }}
        .welcome-screen {{ padding: 50px 10px; min-height: 80vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        .welcome-title {{ color: green; font-size: 45px; font-weight: bold; }}
        .info-box {{ background: var(--card); color: var(--card-text); padding: 25px; border-radius: 15px; width: 90%; max-width: 500px; margin: 20px auto; }}
        .btn {{ padding: 12px 25px; border-radius: 10px; border: none; color: #fff; font-weight: bold; cursor: pointer; margin: 5px; width: 200px; }}
        .btn-red {{ background: red; }} .btn-blue {{ background: #007bff; }}
        .content-screen {{ display:none; padding: 10px; }}
        .top-time {{ background: #1a1a1a; color: yellow; padding: 10px; font-size: 0.8rem; margin-bottom: 10px; border-radius: 5px; }}
        .search-bar {{ width: 90%; padding: 12px; border: 2px solid #007bff; border-radius: 25px; margin: 10px auto; outline: none; display: block; }}
        .filter-tabs {{ display: flex; justify-content: center; gap: 5px; margin-bottom: 10px; flex-wrap: wrap; }}
        .filter-tabs button {{ background: #00bcd4; color: white; border: none; padding: 6px 12px; border-radius: 5px; font-size: 12px; cursor: pointer; }}
        .chapter-header {{ background: #ccc; color: #000; padding: 12px; text-align: left; font-weight: bold; margin: 10px 0; border-radius: 8px; cursor: pointer; }}
        .chapter-item {{ background: var(--item); padding: 12px; border-radius: 8px; margin: 5px 0; text-align: left; cursor: pointer; border: 1px solid #ddd; font-size: 14px; }}
        .dark-mode .chapter-header {{ background: #333; color: #fff; }}
    </style>
</head>
<body>
    <div id="welcome" class="welcome-screen">
        <div class="welcome-title">Welcome</div>
        <div class="info-box">
            <h2>{title}</h2>
            <div style="color:yellow; font-weight:bold;">📥 Created By : {BOT_OWNER_NAME}</div>
            <div style="color:yellow; margin-top:5px;">📅 Date : {now_full}</div>
        </div>
        <button class="btn btn-red" onclick="showContent()">Open Your Batch</button>
        <button class="btn btn-blue" onclick="toggleDark()">Switch to Dark Mode</button>
    </div>

    <div id="content-area" class="content-screen">
        <div class="top-time">📅 Date & Time : {now_full}</div>
        <button class="btn btn-blue" style="width:auto;" onclick="toggleDark()">Switch to Dark Mode</button>
        <div style="color:#007bff; font-weight:bold; margin: 10px 0;">🎥 {v_total} | 📄 {p_total} | 🎵 {a_total}</div>
        <input type="text" id="search" class="search-bar" placeholder="Search content..." onkeyup="searchFn()">
        {html_content}
        <a href="{TELEGRAM_LINK}" style="color:red; font-weight:bold; text-decoration:none; display:block; margin:20px;">JOIN TELEGRAM</a>
    </div>

    <script>
        function showContent() {{ document.getElementById('welcome').style.display='none'; document.getElementById('content-area').style.display='block'; }}
        function toggleDark() {{ document.body.classList.toggle('dark-mode'); }}
        function toggleFolder(id) {{ 
            let el = document.getElementById(id); 
            el.style.display = el.style.display === 'none' ? 'block' : 'none'; 
        }}
        function filterType(folderId, type) {{
            let items = document.querySelectorAll('#' + folderId + ' .list-item');
            items.forEach(item => {{
                item.style.display = (type === 'all' || item.getAttribute('data-type') === type) ? 'block' : 'none';
            }});
        }}
        function searchFn() {{
            let filter = document.getElementById('search').value.toLowerCase();
            let items = document.querySelectorAll('.list-item');
            items.forEach(item => {{
                item.style.display = item.innerText.toLowerCase().includes(filter) ? 'block' : 'none';
            }});
        }}
    </script>
</body>
</html>
"""

@app.on_message(filters.command("start"))
async def start(c, m):
    await m.reply_text("🚀 **Bot Ready!**\nSubject-wise folders & Filters supported.\nBhejo TXT file.")

@app.on_message(filters.document)
async def handle(c, m):
    if not m.document.file_name.endswith(".txt"): return
    path = await m.download()
    with open(path, "r", encoding="utf-8") as f:
        html = generate_html(m.document.file_name, f.read())
    h = path.replace(".txt", ".html")
    with open(h, "w", encoding="utf-8") as f: f.write(html)
    await m.reply_document(h, caption=f"👑 HTML Ready • {BOT_OWNER_NAME}")
    os.remove(path); os.remove(h)

app.run()
