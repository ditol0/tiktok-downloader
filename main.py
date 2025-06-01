from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "No URL provided", 400

    ydl_opts = {
        'outtmpl': 'video.mp4',
        'format': 'mp4',
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    response = send_file('video.mp4', as_attachment=True)

    if os.path.exists('video.mp4'):
        os.remove('video.mp4')

    return response

app.run(host='0.0.0.0', port=81)
