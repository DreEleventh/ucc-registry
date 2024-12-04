# Name of Enterprise App: UCC Registry System
# Developers: [Your names here]
# Version: 1.0
# Version Date: 2024-11-23
# Purpose: FastAPI backend implementation for UCC's Registry Department to manage student records,
# course information, and academic operations.

from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import time
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import schemas, models
from databaseConnect import get_db, engine, Base
from utils import generate_student_id, generate_student_email

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/register_student", status_code=status.HTTP_201_CREATED, response_model=schemas.EnrolStudentResponse)
async def register_student(student_data: schemas.EnrolStudent, db: Session = Depends(get_db)):

    # Generate unique student ID and email
    student_id = generate_student_id(db)
    student_email = generate_student_email(student_data.first_name, student_data.last_name, db)

    # Extract data for the students table
    student_dict = student_data.model_dump(exclude={"contact_details", "emergency_contacts"})
    new_student = models.Students(**student_dict, student_id=student_id)
    db.add(new_student)
    
    # Add student contact details
    contact_dict = student_data.contact_details.model_dump()
    new_contact = models.StudentContacts(**contact_dict,
                                         student_id=student_id, student_email=student_email)
    db.add(new_contact)

    # Add emergency contact details
    for emergency_contact_data in student_data.emergency_contacts:
        emergency_contact_dict = emergency_contact_data.model_dump()
        new_emergency_contact = models.EmergencyContacts(
            **emergency_contact_dict, student_id=student_id)
        db.add(new_emergency_contact)

    db.commit()
    db.refresh(new_student)

    return new_student


@app.get("/get_all_students",response_model=List[schemas.StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(
        models.Students
    ).join(
        models.StudentContacts, models.Students.student_id == models.StudentContacts.student_id
    ).join(
        models.EmergencyContacts, models.Students.student_id == models.EmergencyContacts.student_id, isouter=True
    ).all()

    response = []
    
    for student in students:
        response.append(schemas.StudentResponse(
            id=student.id,
            student_id=student.student_id,
            date_registered=student.date_registered,
            first_name=student.first_name,  # Add these lines
            middle_name=student.middle_name,
            last_name=student.last_name,
            program_of_study_id=student.program_of_study_id,
            contact_details={
                "personal_email": student.contact_details.personal_email,
                "student_email": student.contact_details.student_email,
                "mobile_number": student.contact_details.mobile_number,
                "home_number": student.contact_details.home_number,
                "work_number": student.contact_details.work_number,
                "home_address": student.contact_details.home_address,
            },
            emergency_contacts=[
                {
                    "contact_person_name": ec.contact_person_name,
                    "relation": ec.relation,
                    "contact_number": ec.contact_number,
                } for ec in student.emergency_contacts
            ]
        ))
        
    return response


@app.get("/get_students", response_model=List[schemas.StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    students = (
        db.query(models.Students)
        .options(
            joinedload(models.Students.contact_details),
            joinedload(models.Students.emergency_contacts)
        )
        .join(models.StudentContacts, models.Students.student_id == models.StudentContacts.student_id)
        .join(models.EmergencyContacts, models.Students.student_id == models.EmergencyContacts.student_id, isouter=True)
        .all()
    )
    
    return [
        schemas.StudentResponse(
            id=student.id,
            student_id=student.student_id,
            date_registered=student.date_registered,
            first_name=student.first_name,  # Add these lines
            middle_name=student.middle_name,
            last_name=student.last_name,
            program_of_study_id=student.program_of_study_id,
            contact_details={
                "personal_email": student.contact_details.personal_email,
                "student_email": student.contact_details.student_email,
                "mobile_number": student.contact_details.mobile_number,
                "home_number": student.contact_details.home_number,
                "work_number": student.contact_details.work_number,
                "home_address": student.contact_details.home_address,
            },
            emergency_contacts=[
                {
                    "contact_person_name": ec.contact_person_name,
                    "relation": ec.relation,
                    "contact_number": ec.contact_number,
                } 
                for ec in student.emergency_contacts
            ]
        ) 
        for student in students
    ]
    

@app.put("/update_student/{student_id}", response_model=schemas.StudentResponse)
def update_student(
    student_id: str,
    student_data: schemas.UpdateStudent,  # New schema for updates
    db: Session = Depends(get_db)
):
    # Fetch the student by student_id
    student = db.query(models.Students).filter(models.Students.student_id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with student_id {student_id} not found."
        )

    # Update student details
    if student_data.first_name:
        student.first_name = student_data.first_name
    if student_data.middle_name:
        student.middle_name = student_data.middle_name
    if student_data.last_name:
        student.last_name = student_data.last_name
    if student_data.program_of_study_id:
        student.program_of_study_id = student_data.program_of_study_id

    # Update contact details
    if student_data.contact_details:
        contact = student.contact_details
        if student_data.contact_details.personal_email:
            contact.personal_email = student_data.contact_details.personal_email
        if student_data.contact_details.mobile_number:
            contact.mobile_number = student_data.contact_details.mobile_number
        if student_data.contact_details.home_number is not None:
            contact.home_number = student_data.contact_details.home_number
        if student_data.contact_details.work_number is not None:
            contact.work_number = student_data.contact_details.work_number
        if student_data.contact_details.home_address:
            contact.home_address = student_data.contact_details.home_address

    # Update emergency contacts
    if student_data.emergency_contacts:
        for update_contact in student_data.emergency_contacts:
            emergency_contact = db.query(models.EmergencyContacts).filter(
                models.EmergencyContacts.student_id == student_id,
                models.EmergencyContacts.contact_person_name == update_contact.contact_person_name
            ).first()

            if emergency_contact:
                if update_contact.relation:
                    emergency_contact.relation = update_contact.relation
                if update_contact.contact_number:
                    emergency_contact.contact_number = update_contact.contact_number

    # Commit changes to the database
    db.commit()
    db.refresh(student)

    # Return updated student
    return schemas.StudentResponse(
        id=student.id,
        student_id=student.student_id,
        date_registered=student.date_registered,
        first_name=student.first_name,
        middle_name=student.middle_name,
        last_name=student.last_name,
        program_of_study_id=student.program_of_study_id,
        gpa=student.gpa,
        contact_details=schemas.ContactDetails(
            personal_email=student.contact_details.personal_email,
            student_email=student.contact_details.student_email,
            mobile_number=student.contact_details.mobile_number,
            home_number=student.contact_details.home_number,
            work_number=student.contact_details.work_number,
            home_address=student.contact_details.home_address
        ),
        emergency_contacts=[
            schemas.EmergencyContacts(
                contact_person_name=ec.contact_person_name,
                relation=ec.relation,
                contact_number=ec.contact_number
            ) for ec in student.emergency_contacts
        ]
    )


@app.delete("/delete_student/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: str, db: Session = Depends(get_db)):
    """
    Deletes a student and related records using student_id.
    """
    # Fetch the student by student_id
    student = db.query(models.Students).filter(models.Students.student_id == student_id).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with student_id {student_id} not found."
        )

    # Delete the student
    db.delete(student)
    db.commit()
    return {"message": f"Student with student_id {student_id} has been deleted successfully."}
