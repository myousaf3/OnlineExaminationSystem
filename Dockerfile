FROM python:3.8-slim-buster
ENV PYTHONNUNBUFFERED 1
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:7000", "project.wsgi:application"]