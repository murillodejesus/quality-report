import base64
import os
import io
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

GOOGLE_APPS_SCRIPT_URL = "https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec"

@app.route('/upload', methods=['POST'])
def upload_photo():
    if not requests.is_json:
        return jsonify({"success": False, "message": "Invalid request format"}), 400
    
    data = request.get_json()
    photo_name = data.get('photo_name')
    base64_image = data.get('base64_image')
    if not all([photo_name, base64_image]):
        return jsonify({"success": False, "message": "Missing photo name or image data"}), 400 
    
    try:
        payload = {
            'photo_name': photo_name,
            'base64_image': base64_image
        }
        response = requests.post(GOOGLE_APPS_SCRIPT_URL, json=payload)
        response_data = response.json()
        
        if response_data.get('status') == 'success':
            return jsonify({"success": True, "message": "Foto enviada para a planilha com sucesso."})
        else:
            return jsonify({"success": False, "message": response_data.get('message', 'Erro desconhecido no Apps Script')})

    except Exception as e:
        print(f"Erro no processamento da requisição: {e}")
        return jsonify({"success": False, "message": f"Erro interno: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

