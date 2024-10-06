from fastapi import FastAPI
from contextlib import asynccontextmanager

from .db.main import init_db

from .books.routes import router as books_router
from .auth.routes import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startedssd")
    from src.books.models import Book
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

app.include_router(books_router, prefix=f"{version_prefix}/books", tags=["books"])
app.include_router(auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])

