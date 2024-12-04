from pydantic import  BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional, List


# Contact details schema
class ContactDetails(BaseModel):
    personal_email: EmailStr
    mobile_number: str
    home_number: Optional[str] = None
    work_number: Optional[str] = None
    home_address: str

class EmergencyContacts(BaseModel):
    contact_person_name: str
    relation: str
    contact_number: str

class StudentBase(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    program_of_study_id: int

class EnrolStudent(StudentBase):
    contact_details: ContactDetails
    emergency_contacts: List[EmergencyContacts]

class EnrolStudentResponse(BaseModel):
    id: int
    student_id: str
    date_registered: datetime

    class Config:
        orm_mode: True

class StudentResponse(StudentBase):
    id: int
    student_id: str
    date_registered: datetime
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    program_of_study_id: int
    contact_details: ContactDetails
    emergency_contacts: List[EmergencyContacts]

    class Config:
        orm_mode: True

class UpdateContactDetails(BaseModel):
    personal_email: Optional[EmailStr]
    mobile_number: Optional[str]
    home_number: Optional[str]
    work_number: Optional[str]
    home_address: Optional[str]

class UpdateEmergencyContact(BaseModel):
    contact_person_name: str  # Required to locate the contact
    relation: Optional[str]
    contact_number: Optional[str]
    
class UpdateStudent(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    program_of_study_id: Optional[int]
    contact_details: Optional[UpdateContactDetails]
    emergency_contacts: Optional[List[UpdateEmergencyContact]]