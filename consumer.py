from confluent_kafka import Consumer, KafkaError
import json
import socketio

# Set up SocketIO client
sio = socketio.Client()

# Connect to the Flask-SocketIO server
sio.connect('http://localhost:5000')  # Assuming your Flask app is running on localhost:5000

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'new-weather-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(**conf)

# Subscribe to the weather-topic
consumer.subscribe(['weather-topic'])

# Consume messages and send them to Flask-SocketIO server
try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Timeout after 1 second if no message
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                continue
            else:
                print(f"Consumer error: {msg.error()}")
                continue

        # Parse the message value (JSON string)
        weather_data = json.loads(msg.value().decode('utf-8'))
        
        print(json.dumps(weather_data, indent=4))  # Print the weather data
        
        # Emit weather data to Flask-SocketIO
        sio.emit('weather_update', weather_data)  # Sending to 'weather_update' event

except KeyboardInterrupt:
    pass

finally:
    # Close down the consumer
    consumer.close()
    sio.disconnect()  # Close the SocketIO connection

