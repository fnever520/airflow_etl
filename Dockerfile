FROM apache/airflow:2.7.3
ENV TZ=Etc/UTC
WORKDIR /app
COPY . /app
COPY requirements.txt /app/requirements.txt
RUN pip install --user --upgrade pip
RUN pip install --no-cache-dir --user -r /app/requirements.txt