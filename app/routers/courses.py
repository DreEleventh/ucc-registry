from fastapi import HTTPException, Response, Depends, status, APIRouter
from sqlalchemy.orm import Session, joinedload
from typing import List
import logging

import app.schemas as schemas, app.models as models
from app.databaseConnect import get_db


courses_router = APIRouter(
    prefix="/courses", 
    tags=["Courses"],
)

prerequisites_router = APIRouter(
    prefix= "/prerequisites",
    tags=['Prerequisites']
)


@courses_router.post("/create_course", status_code=status.HTTP_201_CREATED, response_model=schemas.AddCoursesResponse)
async def create_course(course_data: schemas.AddCourses, db: Session = Depends(get_db)): 
    new_course = models.Courses(**course_data.model_dump())
    
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    
    return new_course


@courses_router.get("/get_courses", response_model=List[schemas.CourseResponse])
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


@courses_router.put("/update_course/{course_id}")
async def update_course(course_id: int, course_update: schemas.AddCourses, db: Session = Depends(get_db)):
    update_course_query = db.query(models.Courses).filter(models.Courses.id == course_id)
    
    course = update_course_query.first()
    
    if course is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"course with id {course_id} does not exist.")
    
    update_course_query.update(course_update.dict(), synchronize_session=False)
    db.commit()
    
    return update_course_query.first()


@courses_router.delete("/delete_course/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
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


@courses_router.get("/get_course_by_id/{course_id}", response_model=schemas.CourseResponse)
async def get_single_course(course_id: int, db: Session = Depends(get_db)):
    # Query the course by ID
    course = db.query(models.Courses).filter(models.Courses.id == course_id).first()
    
    # If the course doesn't exist, raise an exception
    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with ID {course_id} not found.")
    
    # Return the course data
    return course


@courses_router.get("/degree_program_courses/{program_id}", response_model=List[schemas.CourseResponse])
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


@courses_router.get("/get_all_courses_with_prerequisites", response_model=List[schemas.CourseWithPrerequisitesResponse])
async def get_courses_with_prerequisites(db: Session = Depends(get_db)):
    courses = (
        db.query(
            models.Courses,
            models.CoursePrerequisites.prerequisite_course_id,
            models.CoursePrerequisites.is_mandatory,
        )
        .join(
            models.CoursePrerequisites,
            models.Courses.id == models.CoursePrerequisites.course_id,
            isouter=True,
        )
        .order_by(models.Courses.id)
        .all()
    )

    response = {}
    for course, prerequisite_course_id, is_mandatory in courses:
        course_id = course.id
        if course_id not in response:
            response[course_id] = {
                "course_id": course_id,
                "course_code": course.course_code,
                "course_title": course.course_title,
                "prerequisites": [],
            }
        if prerequisite_course_id:
            response[course_id]["prerequisites"].append(
                {
                    "prerequisite_course_id": prerequisite_course_id,
                    "is_mandatory": is_mandatory == True,
                }
            )

    return list(response.values())



@courses_router.get("/get_single_course_with_prerequisites/{course_id}", response_model=schemas.CourseWithPrerequisitesResponse)
async def get_course_with_prerequisites(course_id: int, db: Session = Depends(get_db)):
    course_with_prerequisites = (
        db.query(
            models.Courses,
            models.CoursePrerequisites.prerequisite_course_id,
            models.CoursePrerequisites.is_mandatory,
        )
        .join(
            models.CoursePrerequisites,
            models.Courses.id == models.CoursePrerequisites.course_id,
            isouter=True,
        )
        .filter(models.Courses.id == course_id)
        .all()
    )

    if not course_with_prerequisites:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course with ID {course_id} not found",
        )

    # Prepare response
    course_info = None
    prerequisites = []

    for course, prerequisite_course_id, is_mandatory in course_with_prerequisites:
        if not course_info:
            course_info = {
                "course_id": course.id,
                "course_code": course.course_code,
                "course_title": course.course_title,
            }
        if prerequisite_course_id:
            prerequisites.append(
                {
                    "prerequisite_course_id": prerequisite_course_id,
                    "is_mandatory": is_mandatory == True,
                }
            )

    return {
        **course_info,
        "prerequisites": prerequisites,
    }


#------------------------------------------- Prerequisites Endpoints -------------------------------------------

@prerequisites_router.post("/add_prerequisite", status_code=status.HTTP_201_CREATED, response_description=schemas.AddPrerequisitesResponse)
async def add_course_prerequisite(prerequisite_data: schemas.AddPrerequisites, db: Session = Depends(get_db)): 
    
    new_prerequisite = models.CoursePrerequisites(**prerequisite_data.model_dump())
    
    db.add(new_prerequisite)
    db.commit()
    db.refresh(new_prerequisite)
    
    return new_prerequisite


@prerequisites_router.get("/get_prerequisites", response_model=List[schemas.PrerequisitesResponse])
async def get_all_prerequisites(db: Session = Depends(get_db)):
    
    prerequisites = db.query(models.CoursePrerequisites).order_by(models.CoursePrerequisites.id.desc()).all()
    
    prerequisites_dict = [prerequisite.__dict__ for prerequisite in prerequisites]
    
    return prerequisites_dict


@prerequisites_router.put("/update_prerequisite/{prerequisite_id}", response_model=schemas.PrerequisitesResponse)
async def update_prerequisite(prerequisite_id: int, updated_data: schemas.AddPrerequisites, db: Session = Depends(get_db)):
    
    prerequisite_query = db.query(models.CoursePrerequisites).filter(models.CoursePrerequisites.id == prerequisite_id)
    prerequisite = prerequisite_query.first()
    
    if not prerequisite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Prerequisite with ID {prerequisite_id} not found.")
    
    prerequisite_query.update(updated_data.model_dump(), synchronize_session=False)
    
    db.commit()

    return prerequisite_query.first()


@prerequisites_router.delete("/delete_prerequisite/{prerequisite_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prerequisite(prerequisite_id: int, db: Session = Depends(get_db)):
    
    prerequisite_query = db.query(models.CoursePrerequisites).filter(models.CoursePrerequisites.id == prerequisite_id)
    prerequisite = prerequisite_query.first()
    
    if not prerequisite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Prerequisite with ID {prerequisite_id} not found.")
    
    prerequisite_query.delete(synchronize_session=False)
    db.commit()
    
    return {"detail": f"Prerequisite with ID {prerequisite_id} deleted successfully."}


@prerequisites_router.get("/get_single_prerequisite/{prerequisite_id}", response_model=schemas.PrerequisitesResponse)
async def get_single_prerequisite(prerequisite_id: int, db: Session = Depends(get_db)):
    
    prerequisite = db.query(models.CoursePrerequisites).filter(models.CoursePrerequisites.id == prerequisite_id).first()
    
    if not prerequisite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Prerequisite with ID {prerequisite_id} not found.")
    
    return prerequisite


@prerequisites_router.get("/get_prerequisites_for_course/{course_id}", response_model=List[schemas.PrerequisitesResponse])
async def get_prerequisites_for_course(course_id: int, db: Session = Depends(get_db)):
    
    prerequisites = db.query(models.CoursePrerequisites).filter(models.CoursePrerequisites.course_id == course_id).all()
    
    if not prerequisites:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No prerequisites found for course with ID {course_id}.")
    
    return prerequisites
