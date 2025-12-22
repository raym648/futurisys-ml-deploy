# futurisys-ml-deploy/dockerfiles/api.Dockerfile

FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir uvicorn

COPY src/ ./src/

EXPOSE 7860

HEALTHCHECK CMD curl --fail http://localhost:7860/docs || exit 1

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "7860"]
