from fastapi import HTTPException, Response, Depends, status, APIRouter
from sqlalchemy.orm import Session, joinedload
from typing import List
import logging

import app.schemas as schemas
import app.models as models
from app.databaseConnect import get_db
from app.utils import generate_student_id, generate_student_email, hash_password

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.EnrolStudentResponse)
async def register_student(student_data: schemas.EnrolStudent, db: Session = Depends(get_db)):
    try: 
        # Generate unique student ID and email
        student_id = generate_student_id(db)
        student_email = generate_student_email(student_data.first_name, student_data.last_name, db)

        # Extract data for the students table
        student_dict = student_data.model_dump(exclude={"contact_details", "emergency_contacts", "student_credentials"})
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

        # Get Credentials 
        # Hash user password  and get username
        hashed_password = hash_password(student_data.student_credentials.password)
    
        new_credentials = models.StudentCredentials(
            student_id=student_id, 
            username=student_email,
            password=hashed_password,
        )
        db.add(new_credentials)
        
        # Commit changes to the database
        db.commit()
        db.refresh(new_student)
        
        # Fetch minimal student info
        result = db.query(
            models.Students.id,
            models.Students.student_id,
            models.StudentContacts.student_email,
            models.Students.date_registered,
        ).join(
            models.StudentContacts,
            models.Students.student_id == models.StudentContacts.student_id,
        ).filter(models.Students.id == new_student.id).first()

        # Return minimal info
        return {
            "id": result.id,
            "student_id": result.student_id,
            "student_email": result.student_email,
            "date_registered": result.date_registered
        }
    
    except Exception as e:
        db.rollback()  # Rollback in case of errors
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.get("/get_all",response_model=List[schemas.StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(
        models.Students
    ).join(models.StudentContacts, models.Students.student_id == models.StudentContacts.student_id
    ).join(models.EmergencyContacts, models.Students.student_id == models.EmergencyContacts.student_id, isouter=True
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


@router.get("/get", response_model=List[schemas.StudentResponse])
def get_all_students(db: Session = Depends(get_db)):  # noqa: F811
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
    

@router.put("/update/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: str, student_data: schemas.UpdateStudent, db: Session = Depends(get_db)):
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


@router.delete("/delete_by_id/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_by_id(student_id: str, db: Session = Depends(get_db)):
    """
    Deletes a student and related records using student_id.
    """
    # logging.info(f"Attempting to delete student {student_id}")
    
    # Fetch the student by student_id
    student = db.query(models.Students).filter(models.Students.student_id == student_id).first()
    
    if not student:
        # logging.error(f"Student {student_id} not found.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student with student_id {student_id} not found."
        )
    
    try:
        # Delete related contacts first
        db.query(models.StudentContacts).filter(models.StudentContacts.student_id == student_id).delete()
        
        # Then delete the student
        db.delete(student)
        
        # logging.info(f"Student {student_id} deleted successfully. Committing transaction.")
        db.commit()
    except Exception as e:
        db.rollback()
        logging.error(f"Error deleting student {student_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting student: {str(e)}"
        )
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/emergency-contact/{student_id}", response_model=List[schemas.EmergencyContacts])
def read_emergency_contacts(student_id: str, db: Session = Depends(get_db)):

    contact_query = db.query(models.EmergencyContacts).filter(models.EmergencyContacts.student_id == student_id).all()

    if not contact_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Emergency contact with Student ID {student_id} not found")
    return contact_query


@router.get("/student-info/{student_id}", response_model = schemas.StudentInfo)
def read_student_info(student_id: str, db: Session = Depends(get_db)):

    student = db.query(models.Students).filter(models.Students.student_id ==student_id).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details = f"Student with Student ID {student_id} not found")
    return student        


@router.get("/all-student-info", response_model = List[schemas.StudentInfo])
def read_all_student_info( db: Session = Depends(get_db)):

    students = db.query(models.Students).all()
    
    students_dict = (student.__dict__ for student in students)

    return students_dict       