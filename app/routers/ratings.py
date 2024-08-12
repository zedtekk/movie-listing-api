from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, auth
from app.database import get_db
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.post("/movies/{movie_id}/ratings/", response_model=schemas.Rating)
def create_rating_for_movie(movie_id: int, rating: schemas.RatingCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    logger.info(f"User {current_user.username} is rating movie ID {movie_id}")
    new_rating = crud.create_rating(db=db, rating=rating, movie_id=movie_id, user_id=current_user.id)
    logger.info(f"Rating for movie ID {movie_id} added by user {current_user.username}")
    return new_rating

@router.get("/movies/{movie_id}/ratings/", response_model=list[schemas.Rating])
def read_ratings(movie_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching ratings for movie ID {movie_id}")
    ratings = crud.get_ratings(db, movie_id=movie_id)
    logger.info(f"Ratings fetched for movie ID {movie_id}")
    return ratings
