from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "Falta la URL"}), 400

    ydl_opts = {
        'format': 'b/best',  # Busca directamente el formato combinado más simple
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'nocheckcertificate': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # Intenta obtener la URL directa del video
            download_url = info.get('url')
            
            # Si es un playlist o lista de formatos, toma el primero válido
            if not download_url and 'formats' in info:
                for fmt in info['formats']:
                    if fmt.get('url'):
                        download_url = fmt['url']
                        break

            if download_url:
                return jsonify({"downloadUrl": download_url})
            else:
                return jsonify({"error": "No se encontró enlace directo"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
