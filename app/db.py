"""Database connection and session management."""
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# MySQL Database URL
# Format: mysql+mysqlconnector://user:password@localhost/database_name
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+mysqlconnector://root:@localhost/green"
)

# Create engine
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(12), nullable=False)
    registered_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


def get_db() -> Session:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database (create tables)."""
    Base.metadata.create_all(bind=engine)

