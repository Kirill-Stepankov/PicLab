from celery import Celery


app_celery = Celery('app',
             broker='amqp://guest@localhost//',
             backend='rpc://',
             include=['src.pictures.tasks']
             )
