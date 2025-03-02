from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_async_engine(os.getenv("SQLALCHEMY_DATABASE_URL"))
Async_Session_Local = async_sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()


async def get_db() -> AsyncSession:
    async with Async_Session_Local() as session:
        yield session
