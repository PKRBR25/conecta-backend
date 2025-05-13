"""Script to check users in database."""
from sqlmodel import Session, select

from app.db.models.user import User
from app.db.session import engine


def check_users():
    """Check users in database."""
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        for user in users:
            print(f"\nUser ID: {user.id}")
            print(f"Email: {user.email}")
            print(f"Full Name: {user.full_name}")
            print(f"Language: {user.language}")
            print(f"Is Active: {user.is_active}")
            print(f"Is Superuser: {user.is_superuser}")
            print(f"Created At: {user.created_at}")
            print(f"Updated At: {user.updated_at}")


if __name__ == "__main__":
    check_users()
