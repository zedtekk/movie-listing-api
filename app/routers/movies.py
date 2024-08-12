from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, auth
from app.database import get_db
from app.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.post("/movies/", response_model=schemas.Movie)
def create_movie_for_user(
    movie: schemas.MovieCreate, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(auth.get_current_user)
):
    logger.info(f"User {current_user.username} is creating a movie")
    new_movie = crud.create_movie(db=db, movie=movie, user_id=current_user.id)
    logger.info(f"Movie '{new_movie.title}' created successfully by {current_user.username}")
    return new_movie

@router.get("/movies/", response_model=list[schemas.Movie])
def read_movies(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(auth.get_current_user)
):
    logger.info(f"User {current_user.username} is fetching movies with skip={skip} and limit={limit}")
    movies = crud.get_movies(db=db, user_id=current_user.id, skip=skip, limit=limit)
    logger.info(f"Movies fetched successfully for user {current_user.username}")
    return movies

@router.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching movie with ID {movie_id}")
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        logger.warning(f"Movie with ID {movie_id} not found")
        raise HTTPException(status_code=404, detail="Movie not found")
    logger.info(f"Movie with ID {movie_id} fetched successfully")
    return db_movie

@router.put("/movies/{movie_id}", response_model=schemas.Movie)
def update_movie(movie_id: int, movie: schemas.MovieCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    logger.info(f"User {current_user.username} is updating movie with ID {movie_id}")
    updated_movie = crud.update_movie(db=db, movie_id=movie_id, movie=movie, user_id=current_user.id)
    logger.info(f"Movie with ID {movie_id} updated successfully by {current_user.username}")
    return updated_movie

@router.delete("/movies/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    logger.info(f"User {current_user.username} is deleting movie with ID {movie_id}")
    deleted_movie = crud.delete_movie(db=db, movie_id=movie_id, user_id=current_user.id)
    logger.info(f"Movie with ID {movie_id} deleted successfully by {current_user.username}")
    return deleted_movie
