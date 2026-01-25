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
]

NEW_DOMAIN = "https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/"
# ==========================================

app = Client(
    "pro_brand_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

user_mode = {}


# ================= DOMAIN REPLACER =================
def replace_domains(text: str):
    for d in OLD_DOMAINS:
        text = text.replace(d, NEW_DOMAIN)
    return text


# ================= HTML GENERATOR =================
def generate_html(file_name, content):
    title = os.path.splitext(file_name)[0]
    now = datetime.now().strftime("%d %b %Y")
    lines = content.strip().split("\n")

    html_sections = ""
    temp = ""
    folder = "Main Content"
    v, p, a = 0, 0, 0

    for line in lines:
        if ":" in line and ("http" in line or "https" in line):
            name, url = line.split(":", 1)
            name, url = name.strip(), replace_domains(url.strip())
            low = url.lower()

            if any(x in low for x in [".mp3", ".m4a", ".wav"]):
                a += 1
                temp += f'''
                <div class="item audio" onclick="playAudio('{url}')">
                <i class="fas fa-headphones"></i> {name}</div>'''

            elif ".pdf" in low:
                p += 1
                temp += f'''
                <a class="item pdf" href="{url}" target="_blank">
                <i class="fas fa-file-pdf"></i> {name}</a>'''

            elif any(x in low for x in [".mp4", ".m3u8", ".mpd", ".mkv"]):
                v += 1
                temp += f'''
                <div class="item video" onclick="playVideo('{url}')">
                <i class="fas fa-play-circle"></i> {name}</div>'''

            else:
                temp += f'''
                <a class="item other" href="{url}" target="_blank">
                <i class="fas fa-download"></i> {name}</a>'''

        elif line.strip():
            if temp:
                html_sections += f'''
                <div class="folder" onclick="toggle(this)">
                <i class="fas fa-folder"></i> {folder}</div>
                <div class="content">{temp}</div>'''
            folder = line.strip()
            temp = ""

    if temp:
        html_sections += f'''
        <div class="folder" onclick="toggle(this)">
        <i class="fas fa-folder"></i> {folder}</div>
        <div class="content">{temp}</div>'''

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet">
<style>
body{{background:#0f0f0f;color:#fff;font-family:Arial;margin:0}}
header{{background:#111;padding:15px;text-align:center}}
.folder{{background:#222;margin:10px;padding:14px;border-radius:8px;cursor:pointer}}
.content{{display:none}}
.item{{background:#1a1a1a;margin:6px;padding:12px;border-radius:6px}}
.video i{{color:red}} .pdf i{{color:#ff4444}} .audio i{{color:#00ffaa}}
.player{{position:sticky;top:0;background:#000}}
</style>
</head>

<body>
<header>
<h2>{title}</h2>
<p>{now} • 🎥{v} 🎧{a} 📄{p}</p>
</header>

<div class="player">
<video id="v" class="video-js vjs-fluid" controls></video>
<audio id="a" controls style="width:100%;display:none"></audio>
</div>

{html_sections}

<a href="{TELEGRAM_LINK}" style="display:block;text-align:center;color:red;margin:20px">
JOIN TELEGRAM</a>

<script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
<script>
const vp = videojs("v");
function toggle(e){{let c=e.nextElementSibling;c.style.display=c.style.display=="block"?"none":"block";}}
function playVideo(u){{
 document.getElementById("a").style.display="none";
 vp.src({{src:u,type:u.includes(".m3u8")?"application/x-mpegURL":
                 u.includes(".mpd")?"application/dash+xml":"video/mp4"}});
 vp.play(); window.scrollTo(0,0);
}}
function playAudio(u){{
 vp.pause(); document.getElementById("a").style.display="block";
 document.getElementById("a").src=u;
 window.scrollTo(0,0);
}}
</script>
</body>
</html>
"""


# ================= COMMANDS =================
@app.on_message(filters.command("start"))
async def start(c, m):
    user_mode.pop(m.from_user.id, None)
    await m.reply_text(
        "🚀 **Branded Player Bot Active**\n\n"
        "📄 TXT ➜ HTML (Video + Audio + PDF)\n"
        "🎥 All extensions supported\n\n"
        "🔁 Only domain change: /domain"
    )


@app.on_message(filters.command("domain"))
async def domain(c, m):
    user_mode[m.from_user.id] = "domain"
    await m.reply_text(
        "🔁 **DOMAIN CHANGE MODE**\n\n"
        "📄 TXT bhejo → TXT milega\n"
        "❌ HTML nahi banega"
    )


# ================= FILE HANDLER =================
@app.on_message(filters.document)
async def handle(c, m):
    if not m.document.file_name.endswith(".txt"):
        return

    uid = m.from_user.id
    path = await m.download()

    if user_mode.get(uid) == "domain":
        with open(path, "r", encoding="utf-8") as f:
            data = replace_domains(f.read())

        out = path.replace(".txt", "_domain.txt")
        with open(out, "w", encoding="utf-8") as f:
            f.write(data)

        await m.reply_document(out, caption="✅ Domain changed (TXT)")
        os.remove(path); os.remove(out)
        user_mode.pop(uid, None)
        return

    with open(path, "r", encoding="utf-8") as f:
        html = generate_html(m.document.file_name, f.read())

    h = path.replace(".txt", ".html")
    with open(h, "w", encoding="utf-8") as f:
        f.write(html)

    await m.reply_document(h, caption=f"👑 HTML Ready • {BOT_OWNER_NAME}")
    os.remove(path); os.remove(h)


app.run()
