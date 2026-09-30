from fastapi import FastAPI
from contextlib import asynccontextmanager  # helps to run asyc queries nnothing related to fastapi
from database import create_table
from routes.reviews import router as reviews_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_table()
    print("database table  created")
    yield
    # shutdown : cleanup
    print("Shutting down the app")



app=FastAPI(
    title="Welcome to the Rangmanch reviews API",
    description="Rangmanch reviews api used to create, update , delete ",
    lifespan=lifespan
)

app.include_router(reviews_router)

@app.get("/")
def root():
    return {
        "message":"Welcome to the reviews of Rangmach API "
    }