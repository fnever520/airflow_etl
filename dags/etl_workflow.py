import json
import pathlib
import os
import sys
import shutil
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

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

default_args = {
    'owner': 'Fabian Tan',
    'retries': 3,
    'email': ["fnever520@gmail.com"],
    'email_on_failure': True,
    'email_on_entry': True,
    'retry_delay': timedelta(minutes=5)
}

@dag(
    dag_id='etl_dev_workflow', 
    default_args=default_args, 
    start_date=datetime(2023, 12, 5),
    schedule_interval="0 9 * * *",
    catchup=False
    )
def run_etl_pipeline():
    env_var = env.load_env()
    MONGO_CONN_ID  = env_var['MONGO_CONN_ID']
    MONGO_COLLECTION = env_var['MONGO_COLLECTION']

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s %(message)s]"
    )
    logger = logging.getLogger(__name__)
    
    @task()
    def setup():
        return True

    @task()
    def extract_raw_data(**kwargs):
        src = '/home/fabian/src_logs/'
        dst = '/opt/airflow/data'
        ti = kwargs['ti']
        ti.xcom_push('id', 591)

        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

        return dst
    @task()
    def clean_data(dst):
        df = pd.read_csv(os.path.join(dst, 'water_level.csv'))
        print(f'Data shape: {df.shape}')

        return df
    
    @task()
    def upload_mongodb(data):
        hook = MongoHook(mongo_conn_id=MONGO_CONN_ID)
        client = hook.get_conn()
        print(client)
        db = client[hook.connection.schema]
        collection = db[MONGO_COLLECTION]
        print(f"Connected to MongoDB - {client.server_info()}")
        outcome = collection.insert_one(data)
        print(f"Inserted ID is {outcome.inserted_id}")

    @task_group(group_id='intermediate_dag')
    def etl_subdag():
        dst = extract_raw_data()
        compiled_df = clean_data(dst)
        upload_mongodb(compiled_df)

    @task()
    def empty_operator():
        pass

    @task(task_id='teardown', trigger_rule='none_failed_min_one_success')
    def teardown():
        return True
    
    @task.branch(task_id='branch_operator')
    def branch_operator():
        dest = '/opt/airflow/data'
        if os.path.exists(os.path.join(dest, "water_level_processed.csv")):
            print("The file has been post-processed, skipped")
            return "empty_operator"
        return 'intermediate_dag.extract_raw_data'
    
    start_task = setup()
    branch = branch_operator()
    etl = etl_subdag()
    empty = empty_operator()
    end_task = teardown()
    
    start_task >> branch >> [etl, empty] >> end_task

init_dag = run_etl_pipeline()

    