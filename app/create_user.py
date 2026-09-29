import sys

from .database import SessionLocal
from .models import User
from .security import hash_password


if len(sys.argv) != 4:
    print(
        "Utilisation : "
        "python -m app.create_user <email> <mot_de_passe> <role>"
    )
    sys.exit(1)


email = sys.argv[1]
password = sys.argv[2]
role = sys.argv[3]


db = SessionLocal()

try:
    user = User(
        email=email,
        password_hash=hash_password(password),
        role=role,
    )

    db.add(user)
    db.commit()

    print("Utilisateur créé avec succès")

finally:
    db.close()