import json
import pathlib
import os
import sys
import re
import pandas as pd
from libs import env
import logging
from datetime import datetime, timedelta

#Setting path
root_dir = pathlib.Path(os.path.dirname(os.path.realpath(__file__))).parent.__str__()
sys.path.append(root_dir)

from airflow.decorators import dag, task, task_group
from airflow.utils.edgemodifier import Label
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.sensors.base import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

default_args = {
    'owner': 'fabiatan',
    'email': ['fnever520@gmail.com'],
    'email_on_failure': True,
    'email_on_entry': True
}

class RegexFileSensor(BaseSensorOperator):
    @apply_defaults
    def __init__(self, directory, pattern, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.directory = directory
        self.pattern = pattern

    def poke(self, context):
        self.log.info(f" Checking for files in {self.directory} matching pattern {self.pattern}")

        for filename in os.listdir(self.directory):
            if re.match(self.pattern, filename):
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                self.log.info(f'Found matching file {filename}')
                context['ti'].xcom_push(key='found_file', value=filename)
                return True
        return False

    def execute(self, context):
        try:
            super().execute(context)
        except Exception as e:
            self.log.warning(f"Sensor timed out or failed with exception: {e}")

    
@dag(
    dag_id='file_sensing',
    default_args=default_args,
    start_date=datetime(2024,6,30),
    schedule_interval=timedelta(minutes=60),
    catchup=False
)

def run_file_sense():

    file_sensor_task = RegexFileSensor(
        task_id='check_for_zip_file',
        directory='/home/fabiantan/work',
        pattern='.*\.zip$',
        poke_interval=10,
        timeout=600
    )

    @task()
    def process_file(ti=None):
        found_file = ti.xcom_pull(task_ids='check_for_zip_file', key='found_file')
        if found_file:
            print("Start downstream task")
        
        else:
            print("no file is found. Skip downstream task")

        
    file_sensor_task >> process_file()

run_file_sense()
