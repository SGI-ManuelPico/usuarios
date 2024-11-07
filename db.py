from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the database credentials
HOST = 'localhost'
USER = 'root'
PASSWORD = '12345678'
DATABASE = 'test2'

# Update the DATABASE_URL with PyMySQL
DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}"

# Create the engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Function to get a new session
def get_session():
    return Session()
