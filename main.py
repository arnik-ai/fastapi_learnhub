from fastapi import FastAPI
from database import connect_to_mongo, close_mongo_connection
from routers import teacher, student, course, enrollment
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()  
    try:
        yield
    finally:
        await close_mongo_connection()

app = FastAPI(title="LearnHubAPI", lifespan=lifespan)

# Include routers
app.include_router(student.router,   prefix="/students",   tags=["students"])
app.include_router(teacher.router,   prefix="/teachers",   tags=["teachers"])
app.include_router(course.router,    prefix="/courses",    tags=["courses"])
app.include_router(enrollment.router,prefix="/enrollments",tags=["enrollments"])

@app.get("/")
async def root():
    return {"message": "LearnHubAPI is running!"}
