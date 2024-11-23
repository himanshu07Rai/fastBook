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

async def send_email(email: str, subject: str, **kwargs):
    template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{subject}</title>
    </head>
    <body>
        <h1>Welcome to Fast Book</h1>
        <p>Hello {kwargs.get('username', '')},</p>
        <p>{kwargs.get('message', '')}</p>
    </body>
    </html>
    """
    
    message = MessageSchema(
        subject=subject,
        recipients=[email],
        template_body=template,
        subtype="html",
        **kwargs
    )
    await mail.send_message(message)
    