import os

from django.core.mail import send_mail

from app.celery.celery import app
from kafka_core.enums import KafkaTopic
from kafka_core.producer import send_to_kafka


@app.task(name="task")
def task(text: str = "default text"):
    print(text)


@app.task(name="auth_confirmation")
def send_confirm_to_email(email_subject: str, email_message: str, user_email: str):
    send_mail(
        subject=email_subject,
        message=email_message,
        from_email=os.environ.get("HOST_USER"),
        recipient_list=[user_email],
        fail_silently=False,
    )


@app.task(name="message")
def send_message(user: int) -> None:
    send_to_kafka(KafkaTopic.USER_REGISTRATION, f"user with id - {user}")
