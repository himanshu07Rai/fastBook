from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from src.config import Config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

mail = FastMail(
    config =ConnectionConfig(
        MAIL_USERNAME = Config.MAIL_USERNAME,
        MAIL_PASSWORD = Config.MAIL_PASSWORD,
        MAIL_FROM = Config.MAIL_FROM,
        MAIL_PORT = Config.MAIL_PORT,
        MAIL_SERVER = Config.MAIL_SERVER,
        MAIL_STARTTLS = Config.MAIL_STARTTLS,
        MAIL_SSL_TLS = Config.MAIL_SSL_TLS,
        USE_CREDENTIALS = Config.USE_CREDENTIALS,
        VALIDATE_CERTS = Config.VALIDATE_CERTS,
        TEMPLATE_FOLDER= Path(BASE_DIR, "templates")
    )
)


async def send_email(email: str, subject: str,template, **kwargs):
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        template_body=template,
        subtype="html",
        **kwargs
    )
    print("Sending email")
    await mail.send_message(message)
    