from pydantic import  BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


#----------------------- Student Schemas -----------------------
# Contact details schema
class ContactDetails(BaseModel):
    personal_email: EmailStr
    mobile_number: str
    home_number: Optional[str] = None
    work_number: Optional[str] = None
    home_address: str

class ContactDetailsResponse(ContactDetails): 
    student_email: EmailStr
    
    class Config: 
        from_attributes = True
        
    
class EmergencyContacts(BaseModel):
    contact_person_name: str
    relation: str
    contact_number: str

class StudentCredentials(BaseModel):
    # username: Optional[EmailStr]
    password: str
    
class StudentCredentialsResponse(StudentCredentials):
    username: str
    
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    program_of_study_id: int

class EnrolStudent(StudentBase):
    contact_details: ContactDetails
    student_credentials: StudentCredentials
    emergency_contacts: List[EmergencyContacts]

class EnrolStudentResponse(BaseModel):
    id: int
    student_id: str
    student_email: str
    date_registered: datetime

    class Config:
       from_attributes = True

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
       from_attributes = True
       
class StudentInfo(StudentBase):
    student_id: str
    date_registered: datetime
    gpa: Optional[float] = None

    class Config:
        form_attributes = True

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
       from_attributes = True
        
class AddCourses(CoursesBase): 
    pass 

class AddCoursesResponse(BaseModel):
    id: int
    course_code: str
    date_added: datetime
    
    class Config:
        from_attributes = True
        
class CourseResponse(CoursesBase): 
    id: int 
    date_added: datetime
    
    class Config: 
        from_attributes = True 

class CoursePrerequisiteInfo(BaseModel):
    prerequisite_course_id: int
    is_mandatory: bool

class CourseWithPrerequisitesResponse(BaseModel):
    course_id: int
    course_code: str
    course_title: str
    prerequisites: List[CoursePrerequisiteInfo]

    class Config:
        from_attributes = True

class DegreeLevel(BaseModel): 
    level_name: str
    level_code: str 

#------------------- Prerequisites Schemas ---------------------

class PrerequisitesBase(BaseModel):
    course_id: int 
    prerequisite_course_id: int 
    is_mandatory: Optional[bool] = True 
    
class AddPrerequisites(PrerequisitesBase):
    pass 

class AddPrerequisitesResponse(BaseModel):
    id: int 
    course_id: int
    
    class Config: 
        from_attributes = True
        
class PrerequisitesResponse(PrerequisitesBase):
    id: int 
    
    class Config: 
        from_attributes = True    


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
        from_attributes = True
        
class DegreeProgramResponse(DegreeProgramsBase):
    id: int 
    
    class Config:
        from_attributes = True
        
class ProgramNamesResponse(BaseModel): 
    id: int
    program_name: str

    class Config: 
        from_attribute = True 


#------------------- Lecturers Schemas ---------------------

class LecturerTitleBase(BaseModel):
    title_name: str


class LecturerTitleResponse(LecturerTitleBase):
    id: int

    class Config:
        from_attributes = True


class DepartmentBase(BaseModel):
    department_name: str
    department_code: str


class DepartmentResponse(DepartmentBase):
    id: int

    class Config:
        from_attributes = True


class PositionTypeBase(BaseModel):
    position_type: str
    description: Optional[str]


class PositionTypeResponse(PositionTypeBase):
    id: int

    class Config:
        from_attributes = True


class LecturerBase(BaseModel):
    id_number: str
    title_id: int
    first_name: str
    last_name: str
    department_id: int
    position_type_id: int


class LecturerCreate(LecturerBase):
    pass


class LecturerResponse(LecturerBase):
    id: int
    hire_date: datetime
    title: Optional[LecturerTitleResponse]
    department: Optional[DepartmentResponse]
    position: Optional[PositionTypeResponse]

    class Config:
        from_attributes = True
        
        
#=============================== Token =============================

class AdminBase(BaseModel):
    first_name: str
    last_name: str
    status: Optional[str] = "Active"

class CreateAdmin(AdminBase):
    pass

class AdminResponse(AdminBase):
    id: int
    admin_id: str
    admin_email: EmailStr
    hire_date: datetime

    class Config:
        from_attributes = True

class AdminCredentialsBase(BaseModel):
    # username: EmailStr
    password: str

class AdminCredentialsResponse(AdminCredentialsBase):
    id: int
    admin_id: str
    last_login_time: Optional[datetime] = None

    class Config:
        from_attributes = True

class RegisterAdmin(AdminBase):
    admin_credentials: AdminCredentialsBase
    
class UpdateAdmin(BaseModel): 
    first_name: Optional[str]
    last_name: Optional[str]
    status: Optional[str]
    admin_email: Optional[EmailStr]
    
    class Config:
        from_attributes = True
        
class AdminLogin(BaseModel): 
    username: EmailStr
    password: str
    
        
#=============================== Token =============================

class Token(BaseModel):
    """
    Model to represent an authentication token.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Model to represent token data.
    """
    id: Optional[str] = None

