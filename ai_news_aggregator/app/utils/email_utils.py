from __future__ import annotations

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import markdown

from app.config import get_settings


def send_markdown_email(to_email: str, subject: str, body_markdown: str) -> None:
    settings = get_settings()
    if not all([settings.smtp_server, settings.email_address, settings.email_password]):
        raise ValueError("SMTP_SERVER, EMAIL_ADDRESS, and EMAIL_PASSWORD are required")

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = settings.email_address
    message["To"] = to_email
    message.attach(MIMEText(body_markdown, "plain", "utf-8"))
    message.attach(MIMEText(markdown.markdown(body_markdown), "html", "utf-8"))

    with smtplib.SMTP(settings.smtp_server, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.email_address, settings.email_password)
        server.send_message(message)

