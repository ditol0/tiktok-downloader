from flask import Flask, request, jsonify, send_file, abort
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/download', methods=['POST'])
def download_video():
    # يدعم JSON و Form
    url = None
    if request.is_json:
        url = request.get_json().get("url")
    else:
        url = request.form.get("url")

    if not url:
        return jsonify({"error": "يرجى إرسال رابط الفيديو في الحقل 'url'."}), 400

    video_id = str(uuid.uuid4())
    filename = f"{video_id}.mp4"
    output_path = os.path.join(DOWNLOAD_FOLDER, filename)

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
            # نرجع رابط مباشر لتحميل الملف
            return jsonify({"download_url": f"https://{request.host}/file/{filename}"})
        else:
            return jsonify({"error": "فشل تحميل الفيديو."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/file/<filename>', methods=['GET'])
def serve_file(filename):
    path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(path):
        return send_file(path, as_attachment=True)
    else:
        abort(404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
