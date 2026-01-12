import os
import requests
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message

# Replace with your API ID, API Hash, and Bot Token
API_ID = "12475131"
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "7889074753:AAH66Cltd_20v9YtxOT8ounMEkNyQIv3NxE"

# Telegram channel where files will be forwarded
CHANNEL_USERNAME = "Sachin yadav Nitin yadav" 

# Initialize Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

def extract_names_and_urls(file_content):
    lines = file_content.strip().split("\n")
    data = []
    for line in lines:
        if ":" in line:
            name, url = line.split(":", 1)
            data.append((name.strip(), url.strip()))
    return data

def categorize_urls(urls):
    videos = []
    pdfs = []
    others = []

    for name, url in urls:
        new_url = url
        if "https://apps-s3-jw-prod.utkarshapp.com" in url:
            new_url = url.replace(
                "https://apps-s3-jw-prod.utkarshapp.com",
                "https://d1q5ugnejk3zoi.cloudfront.net/ut-production-jw/"
            )

        # Video Formats Support
        is_video = any(ext in new_url.lower() for ext in [".m3u8", ".mp4", ".webm", ".mkv", ".mpd"])
        
        if "media-cdn.classplusapp.com/drm/" in new_url or "tencent" in new_url or "1681" in new_url or "/cc/" in new_url or "videos.classplusapp.com" in new_url:
            new_url = f"https://itsgolu-v1player.vercel.app/?url={new_url}"
            videos.append((name, new_url))
        elif "d1q5ugnejk3zoi.cloudfront.net/" in new_url or "s3convertedcdn.ifasonline.com" in new_url:
            new_url = f"https://eyecatchup.github.io/hlscast/player.html?fullscreen=1&autostart=1&video={new_url}"
            videos.append((name, new_url))
        elif is_video:
            videos.append((name, new_url))
        elif new_url.lower().endswith(".pdf"):
            pdfs.append((name, new_url))
        else:
            others.append((name, new_url))

    return videos, pdfs, others

def generate_html(file_name, videos, pdfs, others):
    file_name_without_extension = os.path.splitext(file_name)[0]
    video_links = "".join(f'<a href="#" onclick="playVideo(\'{url}\')">{name}</a>' for name, url in videos)
    pdf_links = "".join(f'<a href="{url}" target="_blank">{name}</a>' for name, url in pdfs)
    other_links = "".join(f'<a href="{url}" target="_blank">{name}</a>' for name, url in others)

    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{file_name_without_extension}</title>
    <link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet" />
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }}
        body {{ background: #f5f7fa; color: #333; }}
        .header {{ background: #1c1c1c; color: white; padding: 20px; text-align: center; }}
        .subheading {{ font-size: 14px; margin-top: 5px; color: #aaa; }}
        #video-player {{ margin: 20px auto; width: 90%; max-width: 800px; background: #000; border-radius: 8px; overflow: hidden; }}
        .container {{ display: flex; justify-content: center; margin: 20px auto; width: 90%; }}
        .tab {{ padding: 10px 20px; background: white; cursor: pointer; border: 1px solid #ddd; margin: 0 5px; border-radius: 5px; }}
        .content {{ display: none; margin: 20px auto; width: 90%; max-width: 800px; background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .video-list a, .pdf-list a, .other-list a {{ display: block; padding: 10px; background: #f9f9f9; margin-bottom: 5px; text-decoration: none; color: #007bff; border-radius: 5px; font-weight: bold; }}
        .video-list a:hover {{ background: #007bff; color: white; }}
    </style>
</head>
<body>
    <div class="header">
        {file_name_without_extension}
        <div class="subheading">Extracted By: Sachin yadav Nitin yadav™</div>
    </div>

    <div id="video-player">
        <video id="main-player" class="video-js vjs-default-skin vjs-big-play-centered" controls preload="auto" width="640" height="360"></video>
    </div>

    <div class="container">
        <div class="tab" onclick="showContent('videos')">Videos</div>
        <div class="tab" onclick="showContent('pdfs')">PDFs</div>
        <div class="tab" onclick="showContent('others')">Others</div>
    </div>

    <div id="videos" class="content"><h2>Videos</h2><div class="video-list">{video_links}</div></div>
    <div id="pdfs" class="content"><h2>PDFs</h2><div class="pdf-list">{pdf_links}</div></div>
    <div id="others" class="content"><h2>Others</h2><div class="other-list">{other_links}</div></div>

    <script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
    <script>
        const player = videojs('main-player', {{ fluid: true, playbackRates: [0.5, 1, 1.5, 2] }});

        function playVideo(url) {{
            let type = 'video/mp4';
            if (url.includes('.m3u8')) type = 'application/x-mpegURL';
            else if (url.includes('.webm')) type = 'video/webm';
            
            player.src({{ src: url, type: type }});
            player.play();
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function showContent(id) {{
            document.querySelectorAll('.content').forEach(el => el.style.display = 'none');
            document.getElementById(id).style.display = 'block';
        }}
        
        document.addEventListener('DOMContentLoaded', () => showContent('videos'));
    </script>
</body>
</html>
    """
    return html_template

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Send me a .txt file containing Name:URL links.")

@app.on_message(filters.document)
async def handle_file(client, message):
    if not message.document.file_name.endswith(".txt"):
        return await message.reply_text("Please upload a .txt file.")

    file_path = await message.download()
    with open(file_path, "r") as f:
        file_content = f.read()

    urls = extract_names_and_urls(file_content)
    videos, pdfs, others = categorize_urls(urls)
    html_content = generate_html(message.document.file_name, videos, pdfs, others)
    
    html_file_path = file_path.replace(".txt", ".html")
    with open(html_file_path, "w") as f:
        f.write(html_content)

    await message.reply_document(document=html_file_path, caption="✅ HTML File Generated!")
    
    # Clean up
    if os.path.exists(file_path): os.remove(file_path)
    if os.path.exists(html_file_path): os.remove(html_file_path)

if __name__ == "__main__":
    print("Bot is running...")
    app.run()
