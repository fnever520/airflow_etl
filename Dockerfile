FROM apache/airflow:latest-python3.10
ENV TZ=Etc/UTC
WORKDIR /app
COPY . /app
COPY requirements.txt /app/requirements.txt
USER root
RUN apt-get update && apt-get install -y vim
USER airflow
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --user -r /app/requirements.txt