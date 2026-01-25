import os
from datetime import datetime
from pyrogram import Client, filters

# ================= CONFIG =================
BOT_OWNER_NAME = "Sachin Yadav & Nitin Yadav"

API_ID = 12475131
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "8551687208:AAG0Vuuj3lyUhU1zClA_0C7VNS6pbhXUvsk"

TELEGRAM_LINK = "https://t.me/Raftaarss_don"

OLD_DOMAIN = "apps-s3-jw-prod.utkarshapp.com"
NEW_DOMAIN = "d1q5ugnejk3zoi.cloudfront.net/ut-production-jw"
# ==========================================

app = Client("pro_brand_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

user_mode = {}  # track /domain mode


# ================= HTML GENERATOR =================
def generate_html(file_name, content):
    title = os.path.splitext(file_name)[0]
    now = datetime.now().strftime("%d %b %Y")
    lines = content.strip().split("\n")

    html_sections = ""
    temp_content = ""
    current_folder = "Main Lessons"
    v_count, p_count = 0, 0

    for line in lines:
        if ":" in line and ("http" in line or "https" in line):
            name, url = line.split(":", 1)
            name, url = name.strip(), url.strip()

            if OLD_DOMAIN in url:
                url = url.replace(OLD_DOMAIN, NEW_DOMAIN)

            low = url.lower()
            if ".pdf" in low:
                p_count += 1
                temp_content += f'<a class="item-link pdf" href="{url}" target="_blank"><i class="fas fa-file-pdf"></i> {name}</a>'
            else:
                v_count += 1
                temp_content += f'<div class="item-link video" onclick="playMedia(\'{url}\', \'{name}\', this)"><i class="fas fa-play-circle"></i> {name}</div>'

        elif line.strip():
            if temp_content:
                html_sections += f'<div class="folder" onclick="toggleF(this)"><i class="fas fa-folder"></i> {current_folder}</div><div class="f-content">{temp_content}</div>'
            current_folder = line.strip()
            temp_content = ""

    if temp_content:
        html_sections += f'<div class="folder" onclick="toggleF(this)"><i class="fas fa-folder"></i> {current_folder}</div><div class="f-content">{temp_content}</div>'

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet">
<style>
body{{background:#0f0f0f;color:#fff;font-family:Arial;text-align:center}}
.folder{{background:#222;padding:15px;margin:10px;border-radius:6px;cursor:pointer}}
.f-content{{display:none}}
.item-link{{background:#111;padding:12px;margin:5px;border-radius:5px;cursor:pointer}}
</style>
</head>
<body>

<h2>{title}</h2>
<p>{now} • {v_count} Videos • {p_count} PDFs</p>

<video id="player" class="video-js vjs-fluid" controls></video>

{html_sections}

<a href="{TELEGRAM_LINK}">JOIN TELEGRAM</a>

<script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
<script>
const player = videojs('player');
function toggleF(e){{let c=e.nextElementSibling;c.style.display=c.style.display=='block'?'none':'block';}}
function playMedia(url){{player.src({{src:url,type:url.includes('.m3u8')?'application/x-mpegURL':'video/mp4'}});player.play();}}
</script>

</body>
</html>
"""


# ================= COMMANDS =================
@app.on_message(filters.command("start"))
async def start(c, m):
    user_mode.pop(m.from_user.id, None)
    await m.reply_text(
        f"🚀 **Ultra Branded Bot Active**\n\n"
        f"👑 Owner: {BOT_OWNER_NAME}\n\n"
        "📄 TXT bhejo ➜ HTML branded dashboard milega\n"
        "🔁 Sirf domain change ke liye /domain use karo"
    )


@app.on_message(filters.command("domain"))
async def domain(c, m):
    user_mode[m.from_user.id] = "domain"
    await m.reply_text(
        "🔁 **Domain Change Mode ON**\n\n"
        "📄 Ab `.txt` file bhejo\n"
        f"`{OLD_DOMAIN}` ➜ `{NEW_DOMAIN}`"
    )


# ================= FILE HANDLER =================
@app.on_message(filters.document)
async def handle(c, m):
    if not m.document.file_name.endswith(".txt"):
        return

    uid = m.from_user.id
    path = await m.download()

    # DOMAIN MODE
    if user_mode.get(uid) == "domain":
        msg = await m.reply_text("🔁 Replacing domain...")
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()

        data = data.replace(OLD_DOMAIN, NEW_DOMAIN)
        out = path.replace(".txt", "_domain.txt")

        with open(out, "w", encoding="utf-8") as f:
            f.write(data)

        await m.reply_document(out, caption="✅ Domain changed successfully")
        os.remove(path)
        os.remove(out)
        user_mode.pop(uid, None)
        await msg.delete()
        return

    # HTML MODE
    msg = await m.reply_text("💎 Creating branded HTML...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    html = generate_html(m.document.file_name, content)
    h_path = path.replace(".txt", ".html")

    with open(h_path, "w", encoding="utf-8") as f:
        f.write(html)

    await m.reply_document(h_path, caption=f"👑 Brand Dashboard Ready\nBy {BOT_OWNER_NAME}")
    os.remove(path)
    os.remove(h_path)
    await msg.delete()


app.run()
