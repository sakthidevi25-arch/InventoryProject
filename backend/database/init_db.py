from backend.database.base import Base
from backend.database.session import engine
from backend.models import asset, audit_log, api, role, user


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
