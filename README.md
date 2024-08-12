# Movie Listing API

This is a FastAPI project for listing movies, adding comments, and rating movies.

## Features
- User registration and login
- JWT-based authentication
- CRUD operations for movies
- Comment and rate movies
- API documentation with Swagger

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/zedtekk/movie_listing_api.git
    cd movie_listing_api
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Run the application:
    ```sh
    uvicorn app.main:app --reload
    ```

5. Open your browser and go to `http://127.0.0.1:8000/docs` to see the Swagger UI.

## Testing

1. Run tests:
    ```sh
    pytest
    ```

## Deployment

1. Install Gunicorn:
    ```sh
    pip install gunicorn
    ```

2. Create a `Procfile`:
    ```plaintext
    web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
    ```

3. Deploy to your chosen cloud provider.

## License

This project is licensed under the terms of the MIT license.
