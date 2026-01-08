FROM python:3.12-slim

WORKDIR /src

COPY app/requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir -r /src/requirements.txt

COPY app /src/app

EXPOSE 8000

ENV PYTHONPATH=/src

CMD ["fastapi","dev","app/main.py","--host","0.0.0.0"]