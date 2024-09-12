# Overview 
A basic app in Python/Flask that get weather update from [weatherapi.com](https://www.weatherapi.com/) and stores it in Apache Kafka which then can be viewed from dashboard
![Screenshot from 2024-09-12 13-37-58](https://github.com/user-attachments/assets/ed097c51-5478-401d-b898-32d3e783326f)

# Getting started
## Setup Kafka
[Full tutorial](https://kafka.apache.org/quickstart)

+ Setup kafka env
  In your dir where you have installed kafka copy and paste
  ```
  $ bin/zookeeper-server-start.sh config/zookeeper.properties
  ```
  In new terminal session run
  ```
  $ bin/kafka-server-start.sh config/server.properties
  ```
+ Create a topic called ```weather-topic``` (again in new terminal session)
  ```
  $ bin/kafka-topics.sh --create --topic weather-topic --bootstrap-server localhost:9092
  ```
## Run Python file
+ Run app.py then go to ```http://localhost:5000/```
  you should se the first update in a few seconds then the weather api will give new update every 1,2 mins which will be updated live on dashboard
  
+ If you want to update manually run producer.py

+ Rn I have set api_url (in app.py and producer.py) for ease of use (will be removing it in 2,3 days)
