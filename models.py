from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, DATE, Text

from databaseConnect import Base


class DegreePrograms(Base):
    __tablename__ = "degree_programs"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    program_code = Column(String(6), nullable=False)
    program_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    department = Column(String(100), nullable=False)


class Students(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    student_id = Column(String(9), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    program_of_study_id = Column(Integer, ForeignKey('degree_programs.id'), nullable=False)
    gpa = Column(Float, nullable=True)
    date_registered = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    program = relationship("DegreePrograms")
    contact_details = relationship("StudentContacts", back_populates="student", uselist=False)
    emergency_contacts = relationship("EmergencyContacts", back_populates="student", cascade="all, delete")


class StudentContacts(Base):
    __tablename__ = "student_contacts"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    student_id = Column(String(9), ForeignKey('students.student_id', ondelete="CASCADE"), nullable=False)
    personal_email = Column(String(30), nullable=False)
    student_email = Column(String(30), nullable=False)
    mobile_number = Column(String(10), nullable=False)
    home_number = Column(String(10), nullable=True)
    work_number = Column(String(10), nullable=True)
    home_address = Column(String(150), nullable=False)

    student = relationship("Students", back_populates="contact_details")


class EmergencyContacts(Base):
    __tablename__ = "emergency_contacts"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    student_id = Column(String(9), ForeignKey('students.student_id', ondelete="CASCADE"), nullable=False)
    contact_person_name = Column(String(100), nullable=False)
    relation = Column(String(20), nullable=True)
    contact_number = Column(String(10), nullable=True)

    student = relationship("Students", back_populates="emergency_contacts")


class StudentCredentials(Base):
    __tablename__ = "student_credentials"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    student_id = Column(String(9), ForeignKey('students.student_id', ondelete="CASCADE"), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    last_login_time = Column(TIMESTAMP(timezone=True))

    student = relationship("Students")

