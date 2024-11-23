from celery import Celery
from src.mail import send_email
from asgiref.sync import async_to_sync


c_app = Celery()

c_app.config_from_object('src.config')

@c_app.task
def send_email_task(email, subject, template):
    async_to_sync(send_email)(email, subject, template)
    print("Email sent")