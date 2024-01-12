FROM apache/airflow:latest-python3.10

COPY . /opt/airflow
USER root
RUN apt-get update && apt-get install -y vim curl

WORKDIR /opt/airflow
USER airflow
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --user -r requirements.txt