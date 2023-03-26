FROM python:3.9

ENV PYTHONUNBUFFERED=1
WORKDIR /pipelines/
COPY requirements.txt ./
RUN pip install -r requirements.txt
