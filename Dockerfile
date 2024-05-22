FROM apache/airflow:2.8.0-python3.9

COPY . /opt/airflow
WORKDIR /opt/airflow
USER root
RUN apt-get update && apt-get install -y vim curl wget ssh gosu

USER airflow
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# expose for ssh
EXPOSE 22

## Expose for spark use 
EXPOSE 7000-8000

## Expose for master webui
EXPOSE 8080

## expose for slave webui
EXPOSE 8081