from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/download', methods=['GET'])
def download():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "Falta la URL"}), 400

    # Usamos una instancia pública de extracción que evadió el bloqueo de IP de YouTube
    cobalt_api_url = "https://co.wuk.sh/api/json"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "url": video_url,
        "vCodec": "h264"
    }

    try:
        response = requests.post(cobalt_api_url, json=payload, headers=headers, timeout=15)
        data = response.json()

        # Si nos devuelve una URL de descarga válida
        if "url" in data:
            return jsonify({"downloadUrl": data["url"]})
        elif "picker" in data and len(data["picker"]) > 0:
            return jsonify({"downloadUrl": data["picker"][0]["url"]})
        else:
            return jsonify({"error": "No se pudo extraer la URL del video"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
