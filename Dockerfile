FROM python:3.10-slim-buster
WORKDIR /usr/src/async_analyze_metrics
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get -y install netcat gcc postgresql && apt-get clean
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["uvicorn", "api.server:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "5000"]