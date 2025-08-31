
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database.models import Base
from backend.shared.config import DATABASE_URL

class CoursesDatabase:
    def __init__(self, database_url: str = DATABASE_URL):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.create_tables()

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        return self.SessionLocal()

if __name__ == '__main__':
    # This allows running `python -m backend.database.courses_db` to initialize the db
    print(f"Initializing database at {DATABASE_URL}...")
    db = CoursesDatabase()
    print("Database initialized successfully.")
