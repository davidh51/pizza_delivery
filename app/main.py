from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database import init_models
from app.routers import books, users, auth, reset_password, votes

@asynccontextmanager    # ayuda a saber que parte de codigo se esta ejecutando
async def lifespan(app: FastAPI):

    print ("server starting")
    await init_models()
    yield 
    print ("server shutting down")

app = FastAPI(
    title= "Book service",
    version= "0.1.0",
    description="Simple app",
    lifespan=lifespan
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(votes.router)
app.include_router(reset_password.router)


@app.get('/')
async def hello():

    return {"Message":"Hello world"}


