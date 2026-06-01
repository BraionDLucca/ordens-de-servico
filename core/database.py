from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
<<<<<<< HEAD
from dotenv import load_dotenv
import os

load_dotenv()

# Variável de ambiente necessária
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("Variável de ambiente 'DATABASE_URL' é obrigatória")
=======

DATABASE_URL = "sqlite:///./estoque.db"
>>>>>>> origin/main

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()