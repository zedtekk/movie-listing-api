from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, auth
from app.database import get_db
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.post("/movies/{movie_id}/comments/", response_model=schemas.Comment)
def create_comment_for_movie(movie_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    logger.info(f"User {current_user.username} is adding a comment to movie ID {movie_id}")
    new_comment = crud.create_comment(db=db, comment=comment, movie_id=movie_id, user_id=current_user.id)
    logger.info(f"Comment added to movie ID {movie_id} by user {current_user.username}")
    return new_comment

@router.get("/movies/{movie_id}/comments/", response_model=list[schemas.Comment])
def read_comments(movie_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching comments for movie ID {movie_id}")
    comments = crud.get_comments(db, movie_id=movie_id)
    logger.info(f"Comments fetched for movie ID {movie_id}")
    return comments
