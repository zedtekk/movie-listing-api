# app/crud.py
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app import models, schemas
from app.utils import get_password_hash  # Updated import

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()

def create_movie(db: Session, movie: schemas.MovieCreate, user_id: int):
    db_movie = models.Movie(**movie.model_dump(), owner_id=user_id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def update_movie(db: Session, movie_id: int, movie: schemas.MovieCreate, user_id: int):
    db_movie = get_movie(db, movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    if db_movie.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this movie")
    db_movie.title = movie.title
    db_movie.description = movie.description
    db.commit()
    db.refresh(db_movie)
    return db_movie

def delete_movie(db: Session, movie_id: int, user_id: int):
    db_movie = get_movie(db, movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    if db_movie.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this movie")
    
    # Delete associated comments and ratings
    db.query(models.Comment).filter(models.Comment.movie_id == movie_id).delete()
    db.query(models.Rating).filter(models.Rating.movie_id == movie_id).delete()
    
    db.delete(db_movie)
    db.commit()
    return db_movie


def get_movies(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return db.query(models.Movie).filter(models.Movie.owner_id == user_id).offset(skip).limit(limit).all()


def create_comment(db: Session, comment: schemas.CommentCreate, movie_id: int, user_id: int):
    db_comment = models.Comment(**comment.model_dump(), movie_id=movie_id, user_id=user_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments(db: Session, movie_id: int):
    return db.query(models.Comment).filter(models.Comment.movie_id == movie_id).all()

def create_rating(db: Session, rating: schemas.RatingCreate, movie_id: int, user_id: int):
    db_rating = models.Rating(**rating.model_dump(), movie_id=movie_id, user_id=user_id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_ratings(db: Session, movie_id: int):
    return db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()
