from fastapi import FastAPI

from database import close_mongo_connection, connect_to_mongo

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    """Initialize MongoDB connection and start background tasks on application startup."""
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on application shutdown."""
    await close_mongo_connection()


