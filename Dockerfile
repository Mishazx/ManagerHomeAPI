# Dockerfile
ARG BASE_IMAGE
FROM ${BASE_IMAGE}/python:3.8

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY .env /app/

COPY . /app/

EXPOSE 20000

CMD ["python", "manage.py", "runserver", "0.0.0.0:20000"]
