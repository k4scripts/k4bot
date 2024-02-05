FROM python:3.11

WORKDIR /app

COPY src /app/src

COPY requirements.txt /app

RUN useradd -m k4bot

RUN chsh -s /usr/sbin/nologin root

USER k4bot

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "src/main.py"]
