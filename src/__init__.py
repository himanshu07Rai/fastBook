from fastapi import FastAPI
from contextlib import asynccontextmanager
from .books.routes import router as books_router
from .db.main import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application started")
    await init_db()
    yield
    print("Application stopped")

version = "v1"

version_prefix =f"/api/{version}"

app = FastAPI(
    title= "Books API",
    description="A simple API that manages books.",
    version=version,
    lifespan=lifespan
)

app.include_router(books_router, prefix=f"{version_prefix}/books", tags=["books"])

