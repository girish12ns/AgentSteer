from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import Request, HTTPException
from contextlib import asynccontextmanager
from app.config.settings import settings
from app.config.logging import logger
from app.core.exceptions import MongoDBConnectionError
from typing import AsyncGenerator


class MongoDBConnectionManager:
    """Manages MongoDB connection lifecycle with connection pooling"""
    
    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name
        self.client: AsyncIOMotorClient | None = None
        self.db: AsyncIOMotorDatabase | None = None

    async def connect(self) -> AsyncIOMotorDatabase:
        """Establish connection to MongoDB with health check"""
        if not self.client:
            try:
                logger.info(f"Attempting to connect to MongoDB: {self.db_name}")
                self.client = AsyncIOMotorClient(self.uri)
                self.db = self.client[self.db_name]
                
                # Verify connection with ping
                await self.client.admin.command('ping')
                logger.info(f"✓ MongoDB connected successfully: {self.db_name}")
                
            except Exception as e:
                logger.exception(f"✗ Failed to connect to MongoDB: {e}")
                self.client = None
                self.db = None
                raise MongoDBConnectionError(f"Could not connect to MongoDB: {e}") from e
        
        return self.db

    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            logger.info("MongoDB disconnected")

    async def health_check(self) -> bool:
        """Check if MongoDB connection is healthy"""
        if not self.client:
            return False
        try:
            await self.client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"MongoDB health check failed: {e}")
            return False


async def get_db(request: Request) -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    """
    Dependency that provides MongoDB database instance to endpoints.
    Uses the application-level connection pool (no per-request connections).
    """
    # Check if mongo_manager exists
    if not hasattr(request.app.state, 'mongo_manager'):
        logger.error("CRITICAL: mongo_manager not found in app.state!")
        logger.error("This means the lifespan/startup event did not run.")
        logger.error("Available app.state attributes: %s", dir(request.app.state))
        raise HTTPException(
            status_code=500,
            detail="Database not initialized. Server configuration error."
        )
    
    db_manager: MongoDBConnectionManager = request.app.state.mongo_manager
    
    # Return the already-established database connection
    if db_manager.db is None:
        logger.warning("Database not connected, attempting to connect...")
        await db_manager.connect()
    
    yield db_manager.db


@asynccontextmanager
async def lifespan(app):
    """
    Manages application lifespan events.
    Use this in your FastAPI app initialization:
    app = FastAPI(lifespan=lifespan)
    """
    # Startup
    logger.info("=" * 60)
    logger.info("STARTUP: Initializing MongoDB connection...")
    logger.info("=" * 60)
    
    try:
        mongo_manager = MongoDBConnectionManager(
            uri=settings.mongodb_uri,
            db_name=settings.mongodb_db_name
        )
        await mongo_manager.connect()
        app.state.mongo_manager = mongo_manager
        logger.info("✓ MongoDB connection established and stored in app.state")
        logger.info(f"✓ Database: {settings.mongodb_db_name}")
    except Exception as e:
        logger.exception("✗ FATAL: Failed to initialize MongoDB connection")
        raise
    
    logger.info("=" * 60)
    logger.info("Application startup complete")
    logger.info("=" * 60)
    
    yield  # Application runs here
    
    # Shutdown
    logger.info("=" * 60)
    logger.info("SHUTDOWN: Closing MongoDB connection...")
    logger.info("=" * 60)
    await mongo_manager.close()
    logger.info("✓ MongoDB connection closed")


# Alternative: Legacy event handlers (if using older FastAPI)
async def startup_event(app):
    """
    LEGACY: Use this if you can't use lifespan.
    Call from: @app.on_event("startup")
    """
    logger.info("=" * 60)
    logger.info("STARTUP EVENT: Initializing MongoDB connection...")
    logger.info("=" * 60)
    
    try:
        mongo_manager = MongoDBConnectionManager(
            uri=settings.mongodb_uri,
            db_name=settings.mongodb_db_name
        )
        await mongo_manager.connect()
        app.state.mongo_manager = mongo_manager
        logger.info("✓ MongoDB connection established and stored in app.state")
        logger.info(f"✓ Database: {settings.mongodb_db_name}")
    except Exception as e:
        logger.exception("✗ FATAL: Failed to initialize MongoDB connection")
        raise


async def shutdown_event(app):
    """
    LEGACY: Use this if you can't use lifespan.
    Call from: @app.on_event("shutdown")
    """
    logger.info("=" * 60)
    logger.info("SHUTDOWN EVENT: Closing MongoDB connection...")
    logger.info("=" * 60)
    
    if hasattr(app.state, 'mongo_manager'):
        await app.state.mongo_manager.close()
        logger.info("✓ MongoDB connection closed")
    else:
        logger.warning("No mongo_manager found in app.state during shutdown")