FROM python:3.10-slim-bookworm

COPY ./app /app
COPY requirements.txt /app

RUN pip3 install -r app/requirements.txt
EXPOSE 80

CMD ["python3", "app/main.py"]
