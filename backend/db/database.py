from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config.settings import settings

# SQLite needs check_same_thread=False for async
connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_async_engine(settings.DATABASE_URL, echo=False, connect_args=connect_args)
async_sessionmaker_instance = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker_instance() as session:
        yield session

async def init_db():
    # Import all models so Base.metadata knows about them
    import models.user
    import models.project
    import models.repository
    import models.chat
    import models.agent_run
    import models.workflow
    import models.audit_log
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

