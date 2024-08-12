from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.logger import get_logger
from app.routers import users, movies, comments, ratings
from app.database import Base, engine

logger = get_logger(__name__)

app = FastAPI()

# Create all tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(users.router)
app.include_router(movies.router)
app.include_router(comments.router)
app.include_router(ratings.router)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code} for {request.method} {request.url}")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )
