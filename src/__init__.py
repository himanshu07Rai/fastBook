from fastapi import FastAPI, Header

from .books.routes import router as books_router

version = "v1"

version_prefix =f"/api/{version}"

app = FastAPI(
    title= "Books API",
    description="A simple API that manages books.",
    version=version,
)

app.include_router(books_router, prefix=f"{version_prefix}/books", tags=["books"])

