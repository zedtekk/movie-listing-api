from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class MovieBase(BaseModel):
    title: str
    description: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    owner_id: int
    comments: List['Comment'] = []
    ratings: List['Rating'] = []

    model_config = {
        "from_attributes": True
    }

class CommentBase(BaseModel):
    text: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    movie_id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }

class RatingBase(BaseModel):
    rating: int

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int
    movie_id: int
    user_id: int

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
