# app/rehash_passwords.py
import sys
import os
from sqlalchemy.orm import Session

# Adjust the path to include the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import SessionLocal
from app.utils import get_password_hash  # Updated import
from app import models

def rehash_passwords(db: Session):
    users = db.query(models.User).all()
    for user in users:
        if not user.hashed_password.startswith("$2b$"):  # bcrypt hashes start with $2b$
            user.hashed_password = get_password_hash(user.hashed_password)
    db.commit()

if __name__ == "__main__":
    db = SessionLocal()
    rehash_passwords(db)
