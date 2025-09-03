# Multistage Dockerfile for Flask DeepFace App


# Single-stage build for simplicity and to ensure gunicorn is available
FROM python:3.10-slim
WORKDIR /app

# Install build dependencies and system libraries
RUN apt-get update \
	&& apt-get install -y build-essential libgl1 libglvnd0 libglib2.0-0 \
	&& rm -rf /var/lib/apt/lists/*

# Copy requirements and wheels, then install Python dependencies
COPY requirements.txt ./
COPY wheels/ /wheels/
RUN pip install --upgrade pip && pip install --no-index --find-links=/wheels -r requirements.txt

# Copy app code and models
COPY app.py ./
COPY models/ ./models/

# Set environment variables to suppress TensorFlow warnings
ENV TF_CPP_MIN_LOG_LEVEL=2
ENV CUDA_VISIBLE_DEVICES=""

# Expose Flask port
EXPOSE 3000

# Run the Flask app with Gunicorn (WSGI server)
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "app:app"]
