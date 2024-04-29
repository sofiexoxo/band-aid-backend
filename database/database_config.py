from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

# Create async engine
async_engine = create_async_engine(DATABASE_URL, echo=False, future=True)
 
# Create async sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)
 
Base = declarative_base()