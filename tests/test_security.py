from app.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_and_verify():
    password = "Test1234"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password)
    assert not verify_password("WrongPassword", hashed_password)


def test_create_and_decode_access_token():
    token = create_access_token(
        "alice@example.com",
        "user",
    )

    payload = decode_access_token(token)

    assert payload is not None
    assert payload["sub"] == "alice@example.com"
    assert payload["role"] == "user"
    assert "exp" in payload


def test_invalid_access_token():
    payload = decode_access_token("token-invalide")

    assert payload is None
