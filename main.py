import os
import requests
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message

# Replace with your API ID, API Hash, and Bot Token
API_ID = "12475131"
API_HASH = "719171e38be5a1f500613837b79c536f"
BOT_TOKEN = "7889074753:AAExvdOFDteXIMECSYtIB1uRegDPkg-_1IA"

# Telegram channel where files will be forwarded
CHANNEL_USERNAME = "Sachin yadav Nitin yadav"  # Replace with your channel username

# Initialize Pyrogram Client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to extract names and URLs from the text file
def extract_names_and_urls(file_content):
    lines = file_content.strip().split("\n")
    data = []
    for line in lines:
        if ":" in line:
            name, url = line.split(":", 1)
            data.append((name.strip(), url.strip()))
    return data

# Function to categorize URLs
def categorize_urls(urls):
    videos = []
    pdfs = []
    others = []

    for name, url in urls:
        new_url = url

        # Handle Classplus DRM links
        if "media-cdn.classplusapp.com/drm/" in url or "tencent" in url or "1681" in url or "/cc/" in url or "videos.classplusapp.com" in url:
            new_url = f"https://ugxclassplusapi.vercel.app/get/cp/dl?url={url}"
            videos.append((name, new_url))

        elif "videos.classplusapp.com/" in url:
            vid_id = url.split("/")[-2]
            new_url = f"https://api.masterapi.tech/get/cp/dl?url={url}"
            videos.append((name, new_url))

        elif "d1q5ugnejk3zoi.cloudfront.net/" in url or "6UkV0qNY.mp4" in url or "notrbHqj.mp4" in url or ".mp4.m3u8" in url or "0IRSs8nO.mp4" in url:
            vid_id = url.split("/")[-2]
            new_url = f"https://eyecatchup.github.io/hlscast/player.html?fullscreen=1&autostart=1&video={url}"
            videos.append((name, new_url))

        elif "media-cdn.classplusapp.com/alisg-cdn-a.classplusapp.com/" in url:
            vid_id = url.split("/")[-2]
            new_url = f"https://ugxclassplusapi.vercel.app/get/cp/dl?url={url}"
            videos.append((name, new_url))

        elif "media-cdn.classplusapp.com/11443/" in url:
            vid_id = url.split("/")[-2]
            new_url = f"https://api.extractor.workers.dev/player?url={url}"
            videos.append((name, new_url))

        # Handle Testbook DRM
        elif "cpvod.testbook.com" in url:
            try:
                data = requests.get("https://api.masterapi.tech/get/get-hls-key?token=eyJjb3...").json()
                hls_key = data.get("key", "")
                new_url = f"http://api.masterapi.tech/akamai-player-v3?url={url}&hls-key={hls_key}"
                videos.append((name, new_url))
            except Exception as e:
                print("Error fetching HLS key:", e)
                others.append((name, url))

        # Youtube embeds
        elif "youtube.com/embed" in url:
            yt_id = url.split("/")[-1]
            new_url = f"https://www.youtube.com/watch?v={yt_id}"
            videos.append((name, new_url))

        #MPD links
        elif "/master.mpd" in url:
            vid_id = url.split("/")[-2]
            new_url = f"hhttps://download.asmultiverse.com/{video_id}/master.mpd"
            videos.append((name, new_url))

        # M3U8 links
        elif ".m3u8" in url:
            videos.append((name, url))
            
        elif ".mkv" in url:
            videos.append((name, url))
            
        elif ".mp4" in url:
            videos.append((name, url))

        # PDF links
        elif url.lower().endswith(".pdf"):
            pdfs.append((name, url))

        # Fallback
        else:
            others.append((name, url))

    return videos, pdfs, others
# Function to generate HTML file with Video.js player
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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    <link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet" />
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Arial', sans-serif;
        }}

        body {{
            background: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }}

        .header {{
            background: #1c1c1c;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .subheading {{
            font-size: 16px;
            margin-top: 10px;
            color: #ccc;
            font-weight: normal;
        }}

        .subheading a {{
            color: #ffeb3b;
            text-decoration: none;
            font-weight: bold;
        }}

        #video-player {{
            margin: 20px auto;
            width: 90%;
            max-width: 800px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            background: #1c1c1c;
            padding: 10px;
        }}

        #url-input-container {{
            display: none;
            margin: 20px auto;
            width: 90%;
            max-width: 600px;
            text-align: center;
        }}

        #url-input-container input {{
            width: 70%;
            padding: 10px;
            border: 2px solid #007bff;
            border-radius: 5px;
            font-size: 16px;
            margin-right: 10px;
        }}

        #url-input-container button {{
            width: 25%;
            padding: 10px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            background: #007bff;
            color: white;
            cursor: pointer;
            transition: background 0.3s ease;
        }}

        #url-input-container button:hover {{
            background: #0056b3;
        }}

        .search-bar {{
            margin: 20px auto;
            width: 90%;
            max-width: 600px;
            text-align: center;
        }}

        .search-bar input {{
            width: 100%;
            padding: 10px;
            border: 2px solid #007bff;
            border-radius: 5px;
            font-size: 16px;
        }}

        .no-results {{
            color: red;
            font-weight: bold;
            margin-top: 20px;
            text-align: center;
            display: none;
        }}

        .container {{
            display: flex;
            justify-content: space-around;
            margin: 20px auto;
            width: 90%;
            max-width: 800px;
        }}

        .tab {{
            flex: 1;
            padding: 15px;
            background: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            transition: all 0.3s ease;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            margin: 0 5px;
        }}

        .tab:hover {{
            background: #007bff;
            color: white;
            transform: translateY(-5px);
        }}

        .content {{
            display: none;
            margin: 20px auto;
            width: 90%;
            max-width: 800px;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}

        .content h2 {{
            font-size: 22px;
            margin-bottom: 15px;
            color: #007bff;
        }}

        .video-list, .pdf-list, .other-list {{
            text-align: left;
        }}

        .video-list a, .pdf-list a, .other-list a {{
            display: block;
            padding: 10px;
            background: #f5f7fa;
            margin: 5px 0;
            border-radius: 5px;
            text-decoration: none;
            color: #007bff;
            font-weight: bold;
            transition: all 0.3s ease;
        }}

        .video-list a:hover, .pdf-list a:hover, .other-list a:hover {{
            background: #007bff;
            color: white;
            transform: translateX(10px);
        }}

        .footer {{
            margin-top: 30px;
            font-size: 16px;
            font-weight: bold;
            padding: 15px;
            background: #1c1c1c;
            color: white;
            text-align: center;
            border-radius: 10px;
        }}

        .footer a {{
            color: #ffeb3b;
            text-decoration: none;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="header">
        {file_name_without_extension}
        <div class="subheading">📥 Extracted By: <a href="https://t.me/gjskisb" target="_blank">Sachin yadav Nitin yadav™</a></div>
    </div>

    <div id="video-player">
        <video id="engineer-babu-player" class="video-js vjs-default-skin" controls preload="auto" width="640" height="360">
            <p class="vjs-no-js">
                To view this video please enable JavaScript, and consider upgrading to a web browser that
                <a href="https://videojs.com/html5-video-support/" target="_blank">supports HTML5 video</a>
            </p>
        </video>
    </div>

    <div id="url-input-container">
        <input type="text" id="url-input" placeholder="Enter video URL to play...">
        <button onclick="playCustomUrl()">Play</button>
    </div>

    <button onclick="toggleUrlInput()" style="margin: 20px auto; padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; display: block; width: 90%; max-width: 600px;">Enter Custom URL</button>

    <div class="search-bar">
        <input type="text" id="searchInput" placeholder="Search for videos, PDFs, or other resources..." oninput="filterContent()">
    </div>

    <div id="noResults" class="no-results">No results found.</div>

    <div class="container">
        <div class="tab" onclick="showContent('videos')">Videos</div>
        <div class="tab" onclick="showContent('pdfs')">PDFs</div>
        <div class="tab" onclick="showContent('others')">Others</div>
    </div>

    <div id="videos" class="content">
        <h2>All Video Lectures</h2>
        <div class="video-list">
            {video_links}
        </div>
    </div>

    <div id="pdfs" class="content">
        <h2>All PDFs</h2>
        <div class="pdf-list">
            {pdf_links}
        </div>
    </div>

    <div id="others" class="content">
        <h2>Other Resources</h2>
        <div class="other-list">
            {other_links}
        </div>
    </div>

    <div class="footer">Extracted By - <a href="https://t.me/raftaar_don" target="_blank">sachin yadav nitin yadav</a></div>

    <script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
    <script>
        const player = videojs('engineer-babu-player', {{
            controls: true,
            autoplay: false,
            preload: 'auto',
            fluid: true,
            controlBar: {{
                children: [
                    'playToggle',
                    'volumePanel',
                    'currentTimeDisplay',
                    'timeDivider',
                    'durationDisplay',
                    'progressControl',
                    'liveDisplay',
                    'remainingTimeDisplay',
                    'customControlSpacer',
                    'playbackRateMenuButton',
                    'chaptersButton',
                    'descriptionsButton',
                    'subsCapsButton',
                    'audioTrackButton',
                    'fullscreenToggle'
                ]
            }}
        }});

        function playVideo(url) {{
            if (url.includes('.m3u8')) {{
                document.getElementById('video-player').style.display = 'block';
                player.src({{ src: url, type: 'application/x-mpegURL' }});
                player.play().catch(() => {{
                    window.open(url, '_blank');
                }});
            }} else {{
                window.open(url, '_blank');
            }}
        }}

        function toggleUrlInput() {{
            const urlInputContainer = document.getElementById('url-input-container');
            urlInputContainer.style.display = urlInputContainer.style.display === 'none' ? 'block' : 'none';
        }}

        function playCustomUrl() {{
            const url = document.getElementById('url-input').value;
            if (url) {{
                playVideo(url);
            }}
        }}

        function showContent(tabName) {{
            const contents = document.querySelectorAll('.content');
            contents.forEach(content => {{
                content.style.display = 'none';
            }});
            const selectedContent = document.getElementById(tabName);
            if (selectedContent) {{
                selectedContent.style.display = 'block';
            }}
            filterContent();
        }}

        function filterContent() {{
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const categories = ['videos', 'pdfs', 'others'];
            let hasResults = false;

            categories.forEach(category => {{
                const items = document.querySelectorAll(`#${{category}} .${{category}}-list a`);
                let categoryHasResults = false;

                items.forEach(item => {{
                    const itemText = item.textContent.toLowerCase();
                    if (itemText.includes(searchTerm)) {{
                        item.style.display = 'block';
                        categoryHasResults = true;
                        hasResults = true;
                    }} else {{
                        item.style.display = 'none';
                    }}
                }});

                const categoryHeading = document.querySelector(`#${{category}} h2`);
                if (categoryHeading) {{
                    categoryHeading.style.display = categoryHasResults ? 'block' : 'none';
                }}
            }});

            const noResultsMessage = document.getElementById('noResults');
            if (noResultsMessage) {{
                noResultsMessage.style.display = hasResults ? 'none' : 'block';
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            showContent('videos');
        }});
    </script>
</body>
</html>
    """
    return html_template

# Function to download video using FFmpeg
def download_video(url, output_path):
    command = f"ffmpeg -i {url} -c copy {output_path}"
    subprocess.run(command, shell=True, check=True)

# Command handler for /start
@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await message.reply_text("𝐖𝐞𝐥𝐜𝐨𝐦𝐞! file bhej.𝐭𝐱𝐭 𝐟𝐢𝐥𝐞 𝐜𝐨𝐧𝐭𝐚𝐢𝐧𝐢𝐧𝐠 𝐔𝐑𝐋𝐬.")

# Message handler for file uploads
@app.on_message(filters.document)
async def handle_file(client: Client, message: Message):
    # Check if the file is a .txt file
    if not message.document.file_name.endswith(".txt"):
        await message.reply_text("Please upload a .txt file.")
        return

    # Download the file
    file_path = await message.download()
    file_name = message.document.file_name

    # Read the file content
    with open(file_path, "r") as f:
        file_content = f.read()

    # Extract names and URLs
    urls = extract_names_and_urls(file_content)

    # Categorize URLs
    videos, pdfs, others = categorize_urls(urls)

    # Generate HTML
    html_content = generate_html(file_name, videos, pdfs, others)
    html_file_path = file_path.replace(".txt", ".html")
    with open(html_file_path, "w") as f:
        f.write(html_content)

    # Send the HTML file to the user
    await message.reply_document(document=html_file_path, caption="✅ 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐃𝐨𝐧𝐞!\n\n📥 𝐄𝐱𝐭𝐫𝐚𝐜𝐭𝐞𝐝 𝐁𝐲 : Sachin yadav Nitin yadav™")

    # Forward the .txt file to the channel
    await client.send_document(chat_id=CHANNEL_USERNAME, document=file_path)

    # Clean up files
    os.remove(file_path)
    os.remove(html_file_path)

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run()
