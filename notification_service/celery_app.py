from celery import Celery

import os
from celery import Celery

CELERY_APP_NAME = os.getenv("CELERY_APP_NAME", "notif_app")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "daniyal")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "123")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")

BROKER_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"
BACKEND = os.getenv("CELERY_BACKEND", "rpc://")
INCLUDE = os.getenv("CELERY_INCLUDE", "tasks.notif_tasks").split(",")

celery_app = Celery(
    CELERY_APP_NAME,
    broker=BROKER_URL,
    backend=BACKEND,
    include=INCLUDE,
)

celery_app.conf.task_routes = {
    "tasks.*": {"queue": os.getenv("CELERY_QUEUE", "notif_save_queue")},
}


