FROM python:3.9

RUN pip config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple && \
    pip install pip --no-cache-dir --upgrade

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

ADD . /app
WORKDIR /app

ENV ENV production
EXPOSE 8000

ENTRYPOINT ["gunicorn", "app:app", "-b", "0.0.0.0:8000", "-w", "1", "-k", "uvicorn.workers.UvicornWorker"]
