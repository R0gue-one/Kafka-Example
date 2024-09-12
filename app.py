from flask import Flask, jsonify, render_template
from confluent_kafka import Consumer, Producer, KafkaError
import json
import threading
import requests
import time

app = Flask(__name__)

weather_Data = {}
conf_consumer = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'weather-consumer-group',
    'auto.offset.reset': 'latest',
    'enable.auto.commit': True
}

conf_producer = {
    'bootstrap.servers': 'localhost:9092'
}

consumer = Consumer(**conf_consumer)
consumer.subscribe(['weather-topic'])

producer = Producer(**conf_producer)

def produce_weather_data():
    while True:
        try:
            # Fetch data from Weather API
            api_url = 'http://api.weatherapi.com/v1/current.json?key=95c4a38f95c547a9b3a93205241109&q=London&aqi=yes'
            response = requests.get(api_url)
            weather_data = response.json()

            # Produce Kafka message
            producer.produce('weather-topic', value=json.dumps(weather_data), callback=delivery_report)
            producer.flush()

            print("Weather data produced:", json.dumps(weather_data, indent=4))
            # print("Weather Data Produced !")

            # Wait for 60 seconds before fetching data again
            time.sleep(60)
        except Exception as e:
            print(f"Error producing data: {str(e)}")
            time.sleep(60)  # Retry after 60 seconds

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def consume_messages():
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Consumer error: {msg.error()}")
                continue

        global weather_Data
        weather_Data = json.loads(msg.value().decode('utf-8'))
        print("Data Received")

@app.route('/dashboard', methods=["GET"])
def show_data():
    return jsonify(weather_Data), 200

@app.route('/')
def index():
    return render_template('dashboard.html')

if __name__ == '__main__':
    # Start Kafka consumer thread
    consumer_thread = threading.Thread(target=consume_messages)
    consumer_thread.daemon = True
    consumer_thread.start()

    # Start Kafka producer thread
    producer_thread = threading.Thread(target=produce_weather_data)
    producer_thread.daemon = True
    producer_thread.start()

    app.run(debug=True)

