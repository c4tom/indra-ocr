FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    HF_HOME=/models

WORKDIR /app

# Install Indra OCR and its Python dependencies from this repository.
COPY . .
RUN pip install --no-cache-dir .

# The bundled viewer binds to 127.0.0.1 by default. This wrapper makes it
# listen on all container interfaces so Docker can publish the port.
COPY docker/run_viewer.py /app/docker/run_viewer.py

EXPOSE 8765

CMD ["python", "/app/docker/run_viewer.py", "--port", "8765", "--threads", "4"]
