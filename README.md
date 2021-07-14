# Chat Room App
The goal of this exercise is to create a simple browser-based chat application using Python.
This application should allow several users to talk in a chatroom and also to get stock quotes
from an API using a specific command.
### Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
### Prerequisites
- ubuntu >= 16.04
- docker
- docker-compose
- Celery
- RabbitMQ
### Note: If you just want to run the app without test, you won't need install Celery and Rabbit. The dockerfile will create container with the needed images and dependencies
### To run the app 
Be sure you have installed docker and docker-composed, then move into the app directory and after that, run the follow bash script:
```./start_app.sh```
It will create a container, then it will download images needed for the application and then start the django app running in localhost
```url app: http://127.0.0.1:8000```
### Interface
<img align="center" src="https://i.imgur.com/RQgmUTW.png" width="50%"/>

### Testing
Be sure that celery and redis are running using the following commands:
- To run redis
```
redis-server
```
- To run celery
``` 
celery -A core worker -l info
```
Then, In other terminal run this command:
```
nosetests
```