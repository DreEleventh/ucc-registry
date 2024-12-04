from datetime import datetime
import random
import string
from sqlalchemy.orm import  Session
import models
import re


def generate_student_id(db: Session) -> str:
    """
        Generates a unique 9-character student ID.
        Args:
            db (Session): SQLAlchemy database session for checking uniqueness.
        Returns:
            str: A unique 9-character student ID.
        """

    while True:
        year_prefix = str(datetime.now().year)
        # Generate a random 9-character alphanumeric ID
        suffix = generate_suffix(4)

        student_id = f"{year_prefix}{suffix}"

        # Check if the generated ID already exists in the database
        existing_id = db.query(models.Students).filter_by(student_id=student_id).first()

        if not existing_id:
            return student_id


def generate_student_email(first_name: str, last_name: str, db: Session) -> str:
    """
    Generate a unique student email based on first and last name, 
    ensuring no duplication in the database.

    Args:
        first_name (str): The student's first name.
        last_name (str): The student's last name.
        db (Session): The database session.

    Returns:
        str: A unique student email address.
    """
    existing_emails = get_existing_emails(db)

    sanitized_first_name = re.sub(r'[^a-zA-Z]', '', first_name.strip()).lower()
    sanitized_last_name = re.sub(r'[^a-zA-Z]', '', last_name.strip()).lower()
    email_suffix = generate_suffix(2)

    base_email = f"{sanitized_first_name}.{sanitized_last_name}{email_suffix}@stu.ucc.edu.jm"

    student_email = base_email
    while student_email in existing_emails:
        suffix = generate_suffix(2)
        student_email = f"{sanitized_first_name}.{sanitized_last_name}{suffix}@stu.ucc.edu.jm"

    return student_email


def get_existing_emails(db: Session) -> set:
    """
    Fetch all existing student emails from the database.

    Args:
        db (Session): The database session.

    Returns:
        set: A set of all existing student emails.
    """
    emails = db.query(models.StudentContacts.student_email).all()
    return {email[0] for email in emails}


def generate_suffix(num_of: int) -> str:
    random_suffix = ''.join(random.choices(string.digits, k=num_of))
    return random_suffix


