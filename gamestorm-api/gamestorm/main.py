from fastapi import FastAPI
from gamestorm.routers.auth_router import auth_router
from gamestorm.routers.subscription_router import subscription_router
from gamestorm.models.base import Base
from gamestorm.database import engine

# Create the database tables
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI(title="GameStorm API")

# Include the routers
app.include_router(auth_router)
app.include_router(subscription_router)

