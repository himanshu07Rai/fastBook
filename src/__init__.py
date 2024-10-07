from fastapi import FastAPI
from contextlib import asynccontextmanager

from .db.main import init_db

from .books.routes import router as books_router
from .auth.routes import auth_router
from .reviews.routes import review_router
from .errors import register_all_errors

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startedssd")
    from src.db.models import Book
    await init_db()
    yield
    print("Application stopped")

version = "v1"

version_prefix =f"/api/{version}"

app = FastAPI(
    title= "Books API",
    description="A simple API that manages books.",
    version=version,
    #lifespan=lifespan    # using alembic for migrations
)

register_all_errors(app)

app.include_router(books_router, prefix=f"{version_prefix}/books", tags=["books"])
app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"{version_prefix}/reviews", tags=["reviews"])

