from confluent_kafka import Producer
import requests
import json

# Kafka producer configuration
conf = {'bootstrap.servers': 'localhost:9092'}

producer = Producer(**conf)

# Define a delivery report callback
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Fetch data from Weather API
api_url = "Enter Your API call url here from weatherapi.com"
response = requests.get(api_url)
weather_data = response.json()

print(json.dumps(weather_data, indent=4))

# Produce Kafka message
producer.produce('weather-topic', value=json.dumps(weather_data), callback=delivery_report)

# Wait for messages to be sent
producer.flush()

