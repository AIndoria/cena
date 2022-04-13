import pytest

from cena.core.config import get_app_settings
from cena.services.email import EmailService
from cena.services.email.email_senders import ABCEmailSender

FAKE_ADDRESS = "my_secret_email@email.com"

SUBJECTS = {"Cena Forgot Password", "Invitation to join Cena", "Test Email"}


class TestEmailSender(ABCEmailSender):
    def send(self, email_to: str, subject: str, html: str) -> bool:

        # check email_to:
        assert email_to == FAKE_ADDRESS

        # check subject:
        assert subject in SUBJECTS

        # check html is rendered:
        assert "{{" not in html
        assert "}}" not in html

        return True


def patch_env(monkeypatch):
    monkeypatch.setenv("SMTP_HOST", "email.cena.io")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_TLS", "True")
    monkeypatch.setenv("SMTP_FROM_NAME", "Cena")
    monkeypatch.setenv("SMTP_FROM_EMAIL", "cena@cena.io")
    monkeypatch.setenv("SMTP_USER", "cena@cena.io")
    monkeypatch.setenv("SMTP_PASSWORD", "cena-password")


@pytest.fixture()
def email_service(monkeypatch) -> EmailService:
    patch_env(monkeypatch)
    email_service = EmailService(TestEmailSender())
    get_app_settings.cache_clear()
    email_service.settings = get_app_settings()
    return email_service


def test_email_disabled(monkeypatch):
    email_service = EmailService(TestEmailSender())

    monkeypatch.setenv("SMTP_HOST", "")  # disable email

    get_app_settings.cache_clear()
    email_service.settings = get_app_settings()
    success = email_service.send_test_email(FAKE_ADDRESS)
    assert not success


def test_test_email(email_service):
    success = email_service.send_test_email(FAKE_ADDRESS)
    assert success


def test_forgot_password_email(email_service):
    success = email_service.send_forgot_password(FAKE_ADDRESS, "https://password-url.com")
    assert success


def test_invitation_email(email_service):
    success = email_service.send_invitation(FAKE_ADDRESS, "https://invitie-url.com")
    assert success
