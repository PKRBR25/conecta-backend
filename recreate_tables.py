"""Recreate database tables."""
from sqlmodel import SQLModel
from app.db.session import engine
from app.db.models.user import User, PasswordResetToken


def recreate_tables():
    """Drop and recreate all tables."""
    print("Dropping all tables...")
    SQLModel.metadata.drop_all(engine)
    print("Creating all tables...")
    SQLModel.metadata.create_all(engine)
    print("Done!")


if __name__ == "__main__":
    recreate_tables()
