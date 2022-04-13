import re

from cena.core.config import get_app_settings


def test_default_settings(monkeypatch):
    monkeypatch.delenv("DEFAULT_GROUP", raising=False)
    monkeypatch.delenv("DEFAULT_PASSWORD", raising=False)
    monkeypatch.delenv("POSTGRES_USER", raising=False)
    monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)
    monkeypatch.delenv("DEFAULT_PASSWORD", raising=False)
    monkeypatch.delenv("API_PORT", raising=False)
    monkeypatch.delenv("API_DOCS", raising=False)
    monkeypatch.delenv("IS_DEMO", raising=False)

    get_app_settings.cache_clear()
    app_settings = get_app_settings()

    assert app_settings.DEFAULT_GROUP == "Home"
    assert app_settings.DEFAULT_PASSWORD == "MyPassword"
    assert app_settings.API_PORT == 9000
    assert app_settings.API_DOCS is True
    assert app_settings.IS_DEMO is False

    assert app_settings.REDOC_URL == "/redoc"
    assert app_settings.DOCS_URL == "/docs"


def test_non_default_settings(monkeypatch):
    monkeypatch.setenv("DEFAULT_GROUP", "Test Group")
    monkeypatch.setenv("DEFAULT_PASSWORD", "Test Password")
    monkeypatch.setenv("API_PORT", "8000")
    monkeypatch.setenv("API_DOCS", "False")

    get_app_settings.cache_clear()
    app_settings = get_app_settings()

    assert app_settings.DEFAULT_GROUP == "Test Group"
    assert app_settings.DEFAULT_PASSWORD == "Test Password"
    assert app_settings.API_PORT == 8000
    assert app_settings.API_DOCS is False

    assert app_settings.REDOC_URL is None
    assert app_settings.DOCS_URL is None


def test_default_connection_args(monkeypatch):
    monkeypatch.setenv("DB_ENGINE", "sqlite")
    get_app_settings.cache_clear()
    app_settings = get_app_settings()
    assert re.match(r"sqlite:////.*cena*.db", app_settings.DB_URL)


def test_pg_connection_args(monkeypatch):
    monkeypatch.setenv("DB_ENGINE", "postgres")
    monkeypatch.setenv("POSTGRES_SERVER", "postgres")
    get_app_settings.cache_clear()
    app_settings = get_app_settings()
    assert app_settings.DB_URL == "postgresql://cena:cena@postgres:5432/cena"


def test_smtp_enable(monkeypatch):
    monkeypatch.setenv("SMTP_HOST", "")
    monkeypatch.setenv("SMTP_PORT", "")
    monkeypatch.setenv("SMTP_TLS", "true")
    monkeypatch.setenv("SMTP_FROM_NAME", "")
    monkeypatch.setenv("SMTP_FROM_EMAIL", "")
    monkeypatch.setenv("SMTP_USER", "")
    monkeypatch.setenv("SMTP_PASSWORD", "")

    get_app_settings.cache_clear()
    app_settings = get_app_settings()

    assert app_settings.SMTP_ENABLE is False

    monkeypatch.setenv("SMTP_HOST", "email.cena.io")
    monkeypatch.setenv("SMTP_PORT", "587")
    monkeypatch.setenv("SMTP_TLS", "true")
    monkeypatch.setenv("SMTP_FROM_NAME", "Cena")
    monkeypatch.setenv("SMTP_FROM_EMAIL", "cena@cena.io")
    monkeypatch.setenv("SMTP_USER", "cena@cena.io")
    monkeypatch.setenv("SMTP_PASSWORD", "cena-password")

    get_app_settings.cache_clear()
    app_settings = get_app_settings()

    assert app_settings.SMTP_ENABLE is True
