# Name of Enterprise App: UCC Registry System
# Developers: [Your names here]
# Version: 1.0
# Version Date: 2024-11-23
# Purpose: FastAPI backend implementation for UCC's Registry Department to manage student records,
# course information, and academic operations.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


import app.schemas as schemas, app.models as models
from app.databaseConnect import engine, Base
from app.routers import students, courses, programs


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(courses.courses_router)
app.include_router(programs.programs_router)
app.include_router(courses.prerequisites_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}