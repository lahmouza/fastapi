from fastapi import FastAPI
from . import model
from .database import engine
from .routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware




#model.Base.metadata.create_all(bind=engine)

import psycopg2
from psycopg2.extras import RealDictCursor
### pay attention of order of methods, they are important for the API structure

app = FastAPI()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)






app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}



 



