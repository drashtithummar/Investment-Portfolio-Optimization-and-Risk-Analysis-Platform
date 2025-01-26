# This script consumes data from Kafka, processes it with PySpark, and securely stores it in AWS S3
from pyspark.sql import SparkSession
from kafka import KafkaConsumer
import boto3
import json

# Initialize Spark Session
spark = SparkSession.builder.appName("DataProcessing").getOrCreate()

# Kafka Consumer Configuration
consumer = KafkaConsumer(
    'market_data_topic',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# AWS S3 Configuration
s3 = boto3.client('s3')
bucket_name = 'secure-portfolio-data'

def process_and_store_data():
    for message in consumer:
        record = message.value
        df = spark.createDataFrame([record])
        df = df.withColumn("daily_return", (df["close"] - df["open"]) / df["open"])
        df.write.mode("append").parquet(f"s3a://{bucket_name}/processed_data/")
        print("Data processed and stored in S3")

if __name__ == '__main__':
    process_and_store_data()
