from fastapi import HTTPException, Response, Depends, status, APIRouter
from sqlalchemy.orm import Session, joinedload
from typing import List
import logging

import app.schemas as schemas, app.models as models
from app.databaseConnect import get_db


router = APIRouter(
    prefix="/courses", 
    tags=["Courses"],
)


@router.post("/create_course", status_code=status.HTTP_201_CREATED, response_model=schemas.AddCoursesResponse)
async def create_course(course_data: schemas.AddCourses, db: Session = Depends(get_db)): 
    new_course = models.Courses(**course_data.model_dump())
    
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    
    return new_course


@router.get("/get_courses", response_model=List[schemas.CourseResponse])
async def get_all_courses(db: Session = Depends(get_db)): 
    courses = db.query(models.Courses).order_by(models.Courses.id.desc()).all()
    
    courses_dict = [course.__dict__ for course in courses]
    
    return courses_dict


# @router.put("/update_course/{course_id}", response_model=schemas.CourseResponse)
# async def update_course(course_id: int, course_update: schemas.AddCourses, db: Session = Depends(get_db)):
#     # Fetch the course by ID
#     course = db.query(models.Courses).filter(models.Courses.id == course_id).first()
    
#     if course is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Course with id {course_id} does not exist."
#         )
    
#     try:
#         # Update the course attributes
#         for key, value in course_update.dict().items():
#             setattr(course, key, value)
        
#         db.commit()
#         db.refresh(course)  # Refresh to reflect updated state

#         return course
#     except Exception as e:
#         db.rollback()  # Rollback if any error occurs
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"An error occurred while updating the course: {str(e)}"
#         )


@router.put("/update_course/{course_id}")
async def update_course(course_id: int, course_update: schemas.AddCourses, db: Session = Depends(get_db)):
    update_course_query = db.query(models.Courses).filter(models.Courses.id == course_id)
    
    course = update_course_query.first()
    
    if course is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id {course_id} does not exist.")
    
    update_course_query.update(course_update.dict(), synchronize_session=False)
    db.commit()
    
    return update_course_query.first()


@router.delete("/delete_course/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int, db: Session = Depends(get_db)):
    # Query for the course
    course_query = db.query(models.Courses).filter(models.Courses.id == course_id)
    course = course_query.first()
    
    # Check if the course exists
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with ID {course_id} does not exist.")
    
    # Delete the course
    course_query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"Course with ID {course_id} has been successfully deleted."}


@router.get("/get_course_by_id/{course_id}", response_model=schemas.CourseResponse)
async def get_single_course(course_id: int, db: Session = Depends(get_db)):
    # Query the course by ID
    course = db.query(models.Courses).filter(models.Courses.id == course_id).first()
    
    # If the course doesn't exist, raise an exception
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with ID {course_id} not found.")
    
    # Return the course data
    return course


@router.get("/degree_program_courses/{program_id}", response_model=List[schemas.CourseResponse])
async def get_courses_by_degree_program(program_id: int, db: Session = Depends(get_db)):
    # Query to get courses for the specific degree program
    courses = db.query(models.Courses).filter(models.Courses.program_id == program_id).all()
    
    # Check if there are no courses for the given program
    if not courses:
        raise HTTPException(
            status_code=404, detail=f"No courses found for degree program with ID {program_id}."
        )
    
    # Return the list of courses
    return courses
