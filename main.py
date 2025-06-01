from flask import Flask, request, send_file, abort
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    if not data or "url" not in data:
        return {"error": "يرجى إرسال رابط الفيديو في حقل 'url'."}, 400
    
    url = data["url"]
    video_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.mp4")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': output_path,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if os.path.exists(output_path):
            return send_file(output_path, as_attachment=True)
        else:
            return {"error": "فشل تحميل الفيديو."}, 500
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        # تنظيف الملف بعد الإرسال
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
