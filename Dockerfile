FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN pip install requests

COPY ./app /app

EXPOSE 80