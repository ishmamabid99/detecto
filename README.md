# Detecto - Face Detection & Recognition App

A Flask-based web application for face detection and recognition using DeepFace and computer vision models.

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd detecto
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

   The app will be available at `http://localhost:3000`

## 🐳 Docker Deployment

### Fast Docker Build (Recommended)

To avoid downloading large packages like TensorFlow on every Docker build:

1. **Download Python wheels locally** (one-time setup)
   ```bash
   mkdir wheels
   pip download -r requirements.txt -d wheels
   ```

2. **Build Docker image**
   ```bash
   docker build -t detecto:latest .
   ```

3. **Run Docker container**
   ```bash
   docker run -p 3000:3000 detecto:latest
   ```

### Alternative: Standard Docker Build

If you don't want to pre-download wheels, modify the Dockerfile to remove the wheels references:

```dockerfile
# Remove this line from Dockerfile:
COPY wheels/ /wheels/

# Change this line:
RUN pip install --upgrade pip && pip install --no-index --find-links=/wheels -r requirements.txt

# To:
RUN pip install --upgrade pip && pip install -r requirements.txt
```

## 📁 Project Structure

```
detecto/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Docker configuration
├── models/            # Pre-trained model files
├── wheels/            # Downloaded Python wheels (git-ignored)
└── README.md          # This file
```

## 🔧 Requirements

- Python 3.10+
- Flask
- DeepFace
- TensorFlow
- OpenCV
- Gunicorn (for production)

## 🛠️ Development

### Adding New Dependencies

1. Add the package to `requirements.txt`
2. If using wheels for Docker builds, re-download them:
   ```bash
   rm -rf wheels/
   mkdir wheels
   pip download -r requirements.txt -d wheels
   ```

### Environment Variables

You can set these environment variables to customize the application:

- `TF_CPP_MIN_LOG_LEVEL=2` - Suppress TensorFlow warnings
- `CUDA_VISIBLE_DEVICES=""` - Disable GPU usage

## 🐛 Troubleshooting

### Common Docker Issues

1. **OpenCV ImportError (libGL.so.1)**
   - The Dockerfile includes system libraries (`libgl1`, `libglvnd0`, `libglib2.0-0`) to fix this

2. **Gunicorn not found**
   - Make sure `gunicorn` is in `requirements.txt`
   - Use single-stage Docker build (as provided in Dockerfile)

3. **TensorFlow warnings**
   - These are informational and don't affect functionality
   - Add environment variables to suppress them if needed

### Performance Tips

- Use pre-downloaded wheels for faster Docker builds
- Consider using a smaller base image for production
- Enable GPU support if available for better performance

## 📄 License

[Add your license information here]

## 🤝 Contributing

[Add contribution guidelines here]
