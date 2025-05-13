"""Check database tables."""
from sqlmodel import Session, inspect
from app.db.session import engine


def check_tables():
    """Check if tables exist."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables in database:", tables)

    # Try to query the user table
    with Session(engine) as session:
        try:
            result = session.execute('SELECT * FROM "user" LIMIT 1')
            print("\nUser table structure:")
            for row in result:
                print(row)
        except Exception as e:
            print("\nError querying user table:", str(e))


if __name__ == "__main__":
    check_tables()
