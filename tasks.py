from celery import Celery
broker_url='amqp://localhost//'

app = Celery('tasks',broker='loca')