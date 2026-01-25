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

app = Client(
    "pro_brand_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

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

            # utkarsh auto fix
            if OLD_DOMAIN in url:
                url = url.replace(OLD_DOMAIN, NEW_DOMAIN)

            low = url.lower()
            if ".pdf" in low:
                p_count += 1
                temp_content += f'''
                <a class="item pdf" href="{url}" target="_blank">
                    <i class="fas fa-file-pdf"></i> {name}
                </a>'''
            else:
                v_count += 1
                temp_content += f'''
                <div class="item video" onclick="play('{url}', this)">
                    <i class="fas fa-play-circle"></i> {name}
                </div>'''

        elif line.strip():
            if temp_content:
                html_sections += f'''
                <div class="folder" onclick="toggle(this)">
                    <i class="fas fa-folder"></i> {current_folder}
                </div>
                <div class="content">{temp_content}</div>'''
            current_folder = line.strip()
            temp_content = ""

    if temp_content:
        html_sections += f'''
        <div class="folder" onclick="toggle(this)">
            <i class="fas fa-folder"></i> {current_folder}
        </div>
        <div class="content">{temp_content}</div>'''

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{title}</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet">

<style>
body{{background:#0f0f0f;color:#fff;font-family:Arial;margin:0;text-align:center}}
header{{padding:15px;background:#111;border-bottom:2px solid red}}
.folder{{background:#222;margin:10px;padding:15px;border-radius:8px;cursor:pointer;text-align:left}}
.content{{display:none}}
.item{{background:#1a1a1a;margin:5px;padding:12px;border-radius:6px;text-align:left;cursor:pointer}}
.video i{{color:red}}
.pdf i{{color:#ff4444}}
.player-wrap{{position:sticky;top:0;background:#000;z-index:999}}
</style>
</head>

<body>

<header>
<h2>{title}</h2>
<p>{now} • {v_count} Videos • {p_count} PDFs</p>
</header>

<div class="player-wrap">
<video id="player" class="video-js vjs-fluid vjs-big-play-centered" controls></video>
</div>

{html_sections}

<a href="{TELEGRAM_LINK}" style="display:block;margin:20px;color:red;font-weight:bold">
JOIN TELEGRAM
</a>

<script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
<script>
const player = videojs("player", {{
    playbackRates:[0.5,1,1.25,1.5,2]
}});

function toggle(e){{
  let c=e.nextElementSibling;
  c.style.display=c.style.display=="block"?"none":"block";
}}

function play(url, el){{
  if(url.includes("classplus") || url.includes("drm")){{
    window.open("https://itsgolu-v1player.vercel.app/?url="+url);
    return;
  }}
  let type=url.includes(".m3u8")?"application/x-mpegURL":
           url.includes(".mpd")?"application/dash+xml":"video/mp4";
  player.src({{src:url,type:type}});
  player.play();
  window.scrollTo({{top:0,behavior:"smooth"}});
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
        "📄 TXT bhejo ➜ HTML dashboard milega\n"
        "🎥 All formats supported (MP4 / M3U8 / MPD)\n\n"
        "🔁 Sirf domain change ke liye /domain use karo"
    )


@app.on_message(filters.command("domain"))
async def domain(c, m):
    user_mode[m.from_user.id] = "domain"
    await m.reply_text(
        "🔁 **DOMAIN CHANGE MODE ON**\n\n"
        "📄 TXT bhejo\n"
        f"`{OLD_DOMAIN}` ➜ `{NEW_DOMAIN}`\n\n"
        "❌ HTML generate nahi hoga"
    )


# ================= FILE HANDLER =================
@app.on_message(filters.document)
async def handle(c, m):
    if not m.document.file_name.endswith(".txt"):
        return

    uid = m.from_user.id
    path = await m.download()

    # DOMAIN ONLY MODE
    if user_mode.get(uid) == "domain":
        msg = await m.reply_text("🔁 Domain replace ho raha hai...")
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()

        data = data.replace(OLD_DOMAIN, NEW_DOMAIN)

        out = path.replace(".txt", "_domain.txt")
        with open(out, "w", encoding="utf-8") as f:
            f.write(data)

        await m.reply_document(out, caption="✅ Domain change complete (TXT)")
        os.remove(path)
        os.remove(out)
        user_mode.pop(uid, None)
        await msg.delete()
        return

    # DEFAULT = TXT ➜ HTML
    msg = await m.reply_text("🎨 Professional HTML ban raha hai...")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    html = generate_html(m.document.file_name, content)
    h_path = path.replace(".txt", ".html")

    with open(h_path, "w", encoding="utf-8") as f:
        f.write(html)

    await m.reply_document(
        h_path,
        caption=f"👑 Branded Dashboard Ready\nBy {BOT_OWNER_NAME}"
    )

    os.remove(path)
    os.remove(h_path)
    await msg.delete()


app.run()
