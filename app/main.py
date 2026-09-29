from fastapi import FastAPI, Header, HTTPException

from fastapi.middleware.cors import CORSMiddleware

from .schemas import LoginRequest

from sqlalchemy import select

from .database import SessionLocal

from .models import User

from .security import (
    verify_password,
    create_access_token,
    decode_access_token,
)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "User Access Security App"}


def get_user_by_email(email: str):
    db = SessionLocal()

    try:
        statement = select(User).where(User.email == email)
        return db.scalars(statement).first()

    finally:
        db.close()


def require_admin(authorization: str | None):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token manquant",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Format du token invalide",
        )

    token = authorization.split(" ", 1)[1]

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Token invalide",
        )

    if payload.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Accès réservé aux administrateurs",
        )

    return payload


@app.post("/login")
def login(data: LoginRequest):
    user = get_user_by_email(data.email)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Identifiants incorrects",
        )

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Identifiants incorrects",
        )

    access_token = create_access_token(
        user.email,
        user.role,
    )

    return {
        "message": "Connexion réussie",
        "access_token": access_token,
        "token_type": "bearer",
        "email": user.email,
        "role": user.role,
    }


@app.get("/users/me")
def users_me(
    authorization: str | None = Header(default=None),
):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token manquant",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Format du token invalide",
        )

    token = authorization.split(" ", 1)[1]

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Token invalide",
        )

    return {
        "message": "JWT valide",
        "email": payload.get("sub"),
        "role": payload.get("role"),
    }


@app.get("/admin")
def admin_area(
    authorization: str | None = Header(default=None),
):
    require_admin(authorization)

    return {
        "message": "Bienvenue dans la zone administrateur",
    }