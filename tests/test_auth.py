from fastapi.testclient import TestClient

from app.main import app
from app.models import User
from app.security import create_access_token


client = TestClient(app)


def fake_admin_user():
    return User(
        id=1,
        email="admin@example.com",
        password_hash="fake-hash",
        role="admin",
    )


def fake_regular_user():
    return User(
        id=2,
        email="alice@example.com",
        password_hash="fake-hash",
        role="user",
    )


def test_admin_can_access_admin_area(monkeypatch):
    monkeypatch.setattr(
        "app.main.get_user_by_email",
        lambda email: fake_admin_user(),
    )

    token = create_access_token(
        "admin@example.com",
        "admin",
    )

    response = client.get(
        "/admin",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Bienvenue dans la zone administrateur",
    }


def test_regular_user_cannot_access_admin_area(monkeypatch):
    monkeypatch.setattr(
        "app.main.get_user_by_email",
        lambda email: fake_regular_user(),
    )

    token = create_access_token(
        "alice@example.com",
        "user",
    )

    response = client.get(
        "/admin",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Accès réservé aux administrateurs",
    }


def test_invalid_token_cannot_access_admin_area():
    response = client.get(
        "/admin",
        headers={
            "Authorization": "Bearer token-invalide",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Token invalide",
    }
