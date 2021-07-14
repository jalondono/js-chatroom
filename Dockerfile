FROM python:3.7
ENV PYTHONBUFFERED=1
WORKDIR /usr/src/app
COPY requirements.txt ./
ENV CELERY_BROKER="redis://redis:6379/0"
RUN pip install -r requirements.txt
