from abc import ABC, abstractmethod


class Notification(ABC):
    """Abstract notification class."""

    def __init__(self, recipient: str, subject: str, body: str):
        self._recipient = recipient
        self._subject = subject
        self._body = body

    @abstractmethod
    def send(self) -> bool:
        raise NotImplementedError()


class EmailNotification(Notification):
    """Email notification implementation (placeholder)."""

    def send(self) -> bool:
        # In production, integrate SMTP/SendGrid. This is a placeholder.
        print(f"Sending email to {self._recipient}: {self._subject}")
        return True


class SMSNotification(Notification):
    """SMS notification implementation (placeholder)."""

    def send(self) -> bool:
        # In production, integrate Twilio or other SMS provider.
        print(f"Sending SMS to {self._recipient}: {self._body}")
        return True
