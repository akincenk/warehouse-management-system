"""Create (or promote) an admin user: python create_admin.py <username>"""

import getpass
import sys

from pydantic import ValidationError

from auth.security import hash_password
from database import Base, SessionLocal, engine
from models import User
from schemas import UserCreate


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: python create_admin.py <username>")
    try:
        data = UserCreate(username=sys.argv[1], password=getpass.getpass("Password: "))
    except ValidationError as e:
        sys.exit(str(e))
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        user = db.query(User).filter(User.username == data.username).first()
        if user is None:
            user = User(username=data.username)
            db.add(user)
        user.password = hash_password(data.password)
        user.role = "admin"
        db.commit()
    print(f"Admin user '{data.username}' is ready.")


if __name__ == "__main__":
    main()
