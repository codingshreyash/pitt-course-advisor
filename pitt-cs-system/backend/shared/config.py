import os

# The root of the backend project
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE_NAME = "pitt_courses.db"
DATABASE_PATH = os.path.join(BACKEND_ROOT, 'database', DATABASE_NAME)

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"