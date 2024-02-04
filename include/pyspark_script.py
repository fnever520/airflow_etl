from pyspark.sql import SparkSession

def drop_columns_from_dataset(input_path, output_path):
    # Create or get a spark session
    spark = SparkSession.builder.appName("DropColumnsApp").getOrCreate()

    # Read the dataset
    df = spark.read.csv(input_path, header=True, inferScheme=True)

    # Drop the desired columns
    columns_to_drop = ['column1', 'column2']
    df_transformed = df.drop(*columns_to_drop)

    # SAve the transformed dataset
    df_transformed.write.csv(output_path, header=True)

    # Stop the spark session
    spark.stop()

if __name__ == "__main__":
    input_dataset_path = '/opt/airflow/data/hw2.csv'
    output_dataset_path = '/opt/airflow/data/hw2_transform.csv'

    drop_columns_from_dataset(input_dataset_path, output_dataset_path)
