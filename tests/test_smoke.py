"""Базовые проверки доступности маршрутов (для раздела 3.3 диплома)."""
from app import create_app


def test_public_pages_return_200():
    app = create_app()
    client = app.test_client()
    assert client.get("/").status_code == 200
    assert client.get("/catalog").status_code == 200


def test_login_page_returns_200():
    app = create_app()
    client = app.test_client()
    assert client.get("/auth/login").status_code == 200


def test_booking_requires_login():
    app = create_app()
    client = app.test_client()
    response = client.get("/booking/1", follow_redirects=False)
    assert response.status_code in (302, 401, 403)
