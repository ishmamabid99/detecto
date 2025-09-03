# Face Recognition API (Python, DeepFace)
# Requirements: Flask, DeepFace, Pillow
# Install: pip install flask deepface pillow

from flask import Flask, request, jsonify
from deepface import DeepFace
from PIL import Image
import os
import tempfile
import requests

app = Flask(__name__)

# Ensure uploads directory exists
def ensure_uploads_dir():
    if not os.path.exists('uploads'):
        os.makedirs('uploads')

# Download image from URL and save to temp file
def download_image(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        for chunk in response.iter_content(1024):
            tmp.write(chunk)
        tmp.close()
        return tmp.name
    else:
        raise Exception('Failed to download image')

# Preprocess image (resize, convert to RGB)
def preprocess_image(path):
    img = Image.open(path).convert('RGB')
    img = img.resize((224, 224))
    img.save(path)
    return path

@app.route('/')
def index():
    return jsonify({
        'name': 'Face Detection API (DeepFace)',
        'status': 'running',
        'endpoints': {
            'compareFaces': 'POST /api/compare-faces',
            'compareMixed': 'POST /api/compare-mixed'
        }
    })

@app.route('/healthz')
def healthz():
    return jsonify({
        'uptime': os.times()[4],
        'message': 'Ok',
        'date': str(__import__('datetime').datetime.now())
    })

# Compare two face images from URLs
@app.route('/api/compare-faces', methods=['POST'])
def compare_faces():
    data = request.get_json()
    image1_url = data.get('image1Url')
    image2_url = data.get('image2Url')
    if not image1_url or not image2_url:
        return jsonify({'error': 'Both image URLs are required'}), 400
    try:
        path1 = preprocess_image(download_image(image1_url))
        path2 = preprocess_image(download_image(image2_url))
        result = DeepFace.verify(path1, path2, model_name='ArcFace')
        os.remove(path1)
        os.remove(path2)
        return jsonify({
            'matched': result['verified'],
            'distance': result['distance'],
            'similarity': 1 - result['distance'],
            'percentageMatch': f"{round((1 - result['distance']) * 100)}%"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Compare uploaded image with image from URL
@app.route('/api/compare-mixed', methods=['POST'])
def compare_mixed():
    ensure_uploads_dir()
    image_url = request.form.get('imageUrl')
    file = request.files.get('image')
    if not image_url or not file:
        return jsonify({'error': 'Both image URL and an uploaded file are required'}), 400
    try:
        url_path = preprocess_image(download_image(image_url))
        upload_path = os.path.join('uploads', file.filename)
        file.save(upload_path)
        preprocess_image(upload_path)
        result = DeepFace.verify(url_path, upload_path, model_name='ArcFace')
        os.remove(url_path)
        os.remove(upload_path)
        return jsonify({
            'matched': result['verified'],
            'distance': result['distance'],
            'similarity': 1 - result['distance'],
            'percentageMatch': f"{round((1 - result['distance']) * 100)}%"
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    ensure_uploads_dir()
    app.run(host='0.0.0.0', port=3000)
