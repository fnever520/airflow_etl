import json
from datetime import datetime, timedelta

from airflow.decorators import dag, task
from airflow.providers.mongo.hooks.mongo import MongoHook

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

MONGO_CONN_ID = 'dev_mongo'
MONGO_DB = 'metastore'
MONGO_COLLECTION = 'metacollection'

def json_sample():
    dummy_json = {
        'name': 'fabian',
        'time': timestamp
    }
    return json.dumps(dummy_json)

default_args = {
    'owner': 'fabiatan',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

@dag(
    dag_id='etl_dev_mongodb', 
    default_args=default_args, 
    start_date=datetime(2023, 12, 5),
    schedule_interval=timedelta(hours=1),
    catchup=False
    )
def run_etl_pipeline():
    @task()
    def extract_raw_data():
        pass

    @task()
    def clean_data():
        pass

    @task()
    def upload_mongodb(result):
        hook = MongoHook(conn_id=MONGO_CONN_ID)
        client = hook.get_conn()
        print(client)
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        print(f"Connected to MongoDB - {client.server_info()}")
        data = json.loads(result)
        collection.insert_one(data)

    extract_raw_data() >> clean_data() >> upload_mongodb(json_example())

init_dag = run_etl_pipeline()

    