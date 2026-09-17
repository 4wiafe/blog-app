# Blog API

A _REST API_ for a simple blogging platform built with _FastAPI_. Users can register, publish posts, and browse other people's posts and profiles.

**Status**: Currently in development.
**Phase 0**: Application skeleton and configuration.

## Tech Stack

- Python 3.14
- FastAPI
- PostgreSQL
- SQLAlchemy / SQLModel
- Alembic (Migrations)

## Requirments

- Pyhton 3.14
- PostgreSQL 14 or newer, running locally

## Setup

1. Clone the repository
2. Create and activate the virtual environment
3. Install dependencies from pyprject.toml
4. Copy .env.example to .env and fill in real values
5. Create an empty database in PostgreSQL matching the name in your database url
6. Run the development server with uvicorn pointing at src.main:app, with reload enabled

The API will be available at _http://127.0.0.1:800_

## Environment Variables

- Database URL
- Secret key: To sign access tokens
- Access token expire minutes: How long a token stays valid
- Environment: Development or Production

## Project Structure

```
app/
  main.py         application entry point
  config.py       settings loaded and validated from the environment
  database.py     database engine and session dependency
  models/         database tables
  schemas/        request and response shapes
  crud/           database queries
  services/       business rules
  routers/        HTTP endpoints
  utils/          hashing, tokens, shared helpers
tests/            test suite
alembic/          database migrations
```

## API Documentation

Interactive docs are generated automatically while the server is running:

- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Endpoints

| Method | Path      | Description                                                   |
| ------ | --------- | ------------------------------------------------------------- |
| GET    | `/health` | Returns the service status. Used to check the app is running. |

More endpoints are added in later phases.

## Roadmap

- [x] Phase 0 — skeleton, configuration, health check
- [ ] Phase 1 — database models and migrations
- [ ] Phase 2 — users and authentication
- [ ] Phase 3 — posts and ownership
- [ ] Phase 4 — public browsing and pagination
- [ ] Phase 5 — error handling, logging, CORS
- [ ] Phase 6 — tests
- [ ] Phase 7 — Docker and deployment

## Author

Richmond Kwame Wiafe Gyebi — [@4wiafe](https://github.com/4wiafe)
