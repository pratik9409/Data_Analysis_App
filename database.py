from sqlalchemy import create_engine, Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')  # Use SQLite for local testing

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    subscription_level = Column(String, default="free")  # free or premium
    api_usage = Column(Integer, default=0)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Example function to check user subscription
def check_user_subscription(user_id):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user.subscription_level
    return None

# Example function to update API usage
def update_api_usage(user_id):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    user.api_usage += 1
    db.commit()

# Function to update user subscription level
def update_user_subscription(user_id, subscription_level):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.subscription_level = subscription_level
        db.commit()
        db.close()
