from typing import Dict
from models.notification import EmailNotification, SMSNotification


class NotificationService:
    """Simple notification dispatcher."""

    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        try:
            n = EmailNotification(recipient, subject, body)
            return n.send()
        except Exception:
            return False

    def send_sms(self, recipient: str, body: str) -> bool:
        try:
            n = SMSNotification(recipient, '', body)
            return n.send()
        except Exception:
            return False
