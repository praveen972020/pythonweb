# from flask import Flask, request, jsonify, send_file
# import yt_dlp
# import os

# app = Flask(__name__)

# # Folder to store downloaded videos
# DOWNLOAD_FOLDER = "downloads"
# os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# @app.route('/download', methods=['GET'])
# def download_video():
#     video_url = request.args.get('url')
#     if not video_url:
#         return jsonify({"error": "No URL provided"}), 400

#     try:
#         # Set yt-dlp options
#         ydl_opts = {
#             'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
#             'format': 'best',
#         }

#         # Download video
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(video_url, download=True)
#             file_path = ydl.prepare_filename(info)

#         return send_file(file_path, as_attachment=True)
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
import os
from flask import Flask, request, jsonify, send_file, render_template
import yt_dlp

app = Flask(__name__, template_folder="templates", static_folder="static")

download_folder = "downloads"
os.makedirs(download_folder, exist_ok=True)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        ydl_opts = {
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            'format': 'best',
            'noplaylist': True,  # Allows downloading entire playlists
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            if 'entries' in info:
                file_paths = [ydl.prepare_filename(entry) for entry in info['entries']]
                return jsonify({"message": "Playlist downloaded", "files": file_paths})
            else:
                file_path = ydl.prepare_filename(info)
                return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

