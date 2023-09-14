FROM python:3.10.13-alpine3.17 

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r requirements.txt --no-cache-dir \
    && mkdir logs/

COPY . .

ENTRYPOINT ["python3", "main.py"]
