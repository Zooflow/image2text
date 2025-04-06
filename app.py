from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import pytesseract
import re
import os

app = Flask(__name__)
CORS(app)

def clean_text(text):
    text = text.replace('\n', ' ')  # Unir líneas
    text = text.replace('  ', ' ')  # Espacios dobles
    text = text.strip()  # Quitar espacios al inicio y final
    text = re.sub(r'[^\w\s.,!?¿¡-]', '', text)  # Quita símbolos raros, conserva puntuación
    return text

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    try:
        img = Image.open(file)
        texto = pytesseract.image_to_string(img, lang='eng+spa')
        texto_limpio = clean_text(texto)
        return jsonify({'texto': texto_limpio})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
