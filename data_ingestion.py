# This script ingests financial market data using multiple sources, Kafka producers, and stores it securely
import requests
from kafka import KafkaProducer
import json

# Kafka Producer Configuration
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Data Sources
api_urls = [
    "https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?apikey=demo",
    "https://financialmodelingprep.com/api/v3/historical-price-full/MSFT?apikey=demo",
    "https://financialmodelingprep.com/api/v3/historical-price-full/GOOG?apikey=demo"
]

def fetch_market_data():
    for url in api_urls:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            historical_data = data['historical']
            for record in historical_data:
                producer.send('market_data_topic', record)
                print(f"Sent record to Kafka: {record}")
        else:
            print(f"Failed to fetch data from {url}")

if __name__ == '__main__':
    fetch_market_data()
