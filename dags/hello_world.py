from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

import logging
logger = logging.getLogger("airflow.task")

default_args = {
    'owner': 'fabiatan',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='hello_world_v2',
    default_args=default_args,
    start_date=datetime(2023, 10,10),
    schedule_interval = '@daily',
    catchup=True
) as dag:
    task1 = BashOperator(
        task_id = 'task1',
        bash_command='echo Hello World'
    )