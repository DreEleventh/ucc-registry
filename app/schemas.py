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
    
    
#------------------- Courses Schemas ---------------------

class CoursesBase(BaseModel):
    course_code: str 
    course_title: str 
    course_credits: int
    degree_level_id: int
    program_id: int 
    description: str
    active: Optional[str]
    
    class Config: 
        orm_mode = True
        
class AddCourses(CoursesBase): 
    pass 

class AddCoursesResponse(BaseModel):
    id: int
    course_code: str
    date_added: datetime
    
    class Config:
        orm_mode: True
        
class CourseResponse(CoursesBase): 
    id: int 
    date_added: datetime
    
    class Config: 
        orm_mode: True 


#------------------- Prerequisites Schemas ---------------------

class PrerequisitesBase(BaseModel):
    course_id: int 
    prerequisite_course_id: int 
    is_mandatory: str 
    
class AddPrerequisites(PrerequisitesBase):
    pass 

class AddPrerequisitesResponse(BaseModel):
    id: int 
    course_id: int
    
    class Config: 
        orm_mode: True
        
class PrerequisitesResponse(PrerequisitesBase):
    id: int 
    
    class Confog: 
        orm_mode: True    


#------------------- Programs Schemas ---------------------

class DegreeProgramsBase(BaseModel):
    program_code: str
    program_name: str
    description: str 
    department: str 
    
class AddDegreePrograms(DegreeProgramsBase):
    pass 

class AddDegreeProgramResponse(BaseModel): 
    id: int 
    program_code: str 
    
    class Config:
        orm_mode: True
        
class DegreeProgramResponse(DegreeProgramsBase):
    id: int 
    
    class Config:
        orm_mode: True
        


