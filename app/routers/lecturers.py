from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from typing import List

import app.schemas as schemas
import app.models as models
from app.databaseConnect import get_db


lecturers_router = APIRouter(
    prefix="/lecturers",
    tags=["Lecturers"],
)

titles_router = APIRouter(
    prefix="/titles", 
    tags=["Titles"],
)

departments_router = APIRouter(
    prefix = "/departments", 
    tags=["Departments"]
)

positions_router = APIRouter(
    prefix="/positions",
    tags=["Positions"]
)


# =========================== Lecturers ===========================

@lecturers_router.post("/add_lecturer", status_code=status.HTTP_201_CREATED, response_model=schemas.LecturerResponse)
def add_lecturer(lecturer_data: schemas.LecturerCreate, db: Session = Depends(get_db)):
    new_lecturer = models.Lecturers(**lecturer_data.dict())
    db.add(new_lecturer)
    db.commit()
    db.refresh(new_lecturer)
    return new_lecturer


@lecturers_router.get("/get_all_lecturers", response_model=List[schemas.LecturerResponse])
def get_all_lecturers(db: Session = Depends(get_db)):
    lecturers = db.query(models.Lecturers).all()
    return lecturers


@lecturers_router.get("/get_single_lecturers/{lecturer_id}", response_model=schemas.LecturerResponse)
def get_single_lecturer(lecturer_id: int, db: Session = Depends(get_db)):
    lecturer = db.query(models.Lecturers).filter(models.Lecturers.id == lecturer_id).first()
    if not lecturer:
        raise HTTPException(status_code=404, detail=f"Lecturer with ID {lecturer_id} not found.")
    return lecturer


@lecturers_router.put("/update_lecturers/{lecturer_id}", response_model=schemas.LecturerResponse)
def update_lecturer(lecturer_id: int, lecturer_data: schemas.LecturerCreate, db: Session = Depends(get_db)):
    lecturer = db.query(models.Lecturers).filter(models.Lecturers.id == lecturer_id).first()
    if not lecturer:
        raise HTTPException(status_code=404, detail=f"Lecturer with ID {lecturer_id} not found.")
    for key, value in lecturer_data.dict().items():
        setattr(lecturer, key, value)
    db.commit()
    db.refresh(lecturer)
    return lecturer


@lecturers_router.delete("/delete_lecturers/{lecturer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lecturer(lecturer_id: int, db: Session = Depends(get_db)):
    lecturer = db.query(models.Lecturers).filter(models.Lecturers.id == lecturer_id).first()
    if not lecturer:
        raise HTTPException(status_code=404, detail=f"Lecturer with ID {lecturer_id} not found.")
    db.delete(lecturer)
    db.commit()
    return {"message": "Lecturer deleted successfully."}


# =========================== Lecturers Titles ===========================

@titles_router.post("/add_lecturer_titles", status_code=status.HTTP_201_CREATED, response_model=schemas.LecturerTitleResponse)
def add_lecturer_title(title_data: schemas.LecturerTitleBase, db: Session = Depends(get_db)):
    new_title = models.LecturerTitles(**title_data.dict())
    db.add(new_title)
    db.commit()
    db.refresh(new_title)
    return new_title


@titles_router.get("/get_lecturer_titles", response_model=List[schemas.LecturerTitleResponse])
def get_all_lecturer_titles(db: Session = Depends(get_db)):
    titles = db.query(models.LecturerTitles).all()
    return titles


@titles_router.get("/lecturer_titles_by_id/{title_id}", response_model=schemas.LecturerTitleResponse)
def get_single_lecturer_title(title_id: int, db: Session = Depends(get_db)):
    title = db.query(models.LecturerTitles).filter(models.LecturerTitles.id == title_id).first()
    if not title:
        raise HTTPException(status_code=404, detail=f"Lecturer title with ID {title_id} not found.")
    return title


@titles_router.put("/update_lecturer_titles/{title_id}", response_model=schemas.LecturerTitleResponse)
def update_lecturer_title(title_id: int, title_data: schemas.LecturerTitleBase, db: Session = Depends(get_db)):
    title = db.query(models.LecturerTitles).filter(models.LecturerTitles.id == title_id).first()
    if not title:
        raise HTTPException(status_code=404, detail=f"Lecturer title with ID {title_id} not found.")
    for key, value in title_data.dict().items():
        setattr(title, key, value)
    db.commit()
    db.refresh(title)
    return title


@titles_router.delete("/delete_lecturer_titles/{title_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lecturer_title(title_id: int, db: Session = Depends(get_db)):
    title = db.query(models.LecturerTitles).filter(models.LecturerTitles.id == title_id).first()
    if not title:
        raise HTTPException(status_code=404, detail=f"Lecturer title with ID {title_id} not found.")
    db.delete(title)
    db.commit()
    return {"message": "Lecturer title deleted successfully."}


# =========================== Departments ===========================

@departments_router.post("/add_departments", status_code=status.HTTP_201_CREATED, response_model=schemas.DepartmentResponse)
def add_department(department_data: schemas.DepartmentBase, db: Session = Depends(get_db)):
    new_department = models.Departments(**department_data.dict())
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department


@departments_router.get("/get_all_departments", response_model=List[schemas.DepartmentResponse])
def get_all_departments(db: Session = Depends(get_db)):
    departments = db.query(models.Departments).all()
    return departments


@departments_router.get("/get_single_departments/{department_id}", response_model=schemas.DepartmentResponse)
def get_single_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(models.Departments).filter(models.Departments.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail=f"Department with ID {department_id} not found.")
    return department


@departments_router.put("/update_departments/{department_id}", response_model=schemas.DepartmentResponse)
def update_department(department_id: int, department_data: schemas.DepartmentBase, db: Session = Depends(get_db)):
    department = db.query(models.Departments).filter(models.Departments.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail=f"Department with ID {department_id} not found.")
    for key, value in department_data.dict().items():
        setattr(department, key, value)
    db.commit()
    db.refresh(department)
    return department


@departments_router.delete("/delete_departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(department_id: int, db: Session = Depends(get_db)):
    department = db.query(models.Departments).filter(models.Departments.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail=f"Department with ID {department_id} not found.")
    db.delete(department)
    db.commit()
    return {"message": "Department deleted successfully."}


# =========================== Positions ===========================

@positions_router.post("/position_types", status_code=status.HTTP_201_CREATED, response_model=schemas.PositionTypeResponse)
def add_position_type(position_data: schemas.PositionTypeBase, db: Session = Depends(get_db)):
    new_position = models.PositionTypes(**position_data.dict())
    db.add(new_position)
    db.commit()
    db.refresh(new_position)
    return new_position


@positions_router.get("/get_position_types", response_model=List[schemas.PositionTypeResponse])
def get_all_position_types(db: Session = Depends(get_db)):
    positions = db.query(models.PositionTypes).all()
    return positions


@positions_router.get("/position_types/{position_id}", response_model=schemas.PositionTypeResponse)
def get_single_position_type(position_id: int, db: Session = Depends(get_db)):
    position = db.query(models.PositionTypes).filter(models.PositionTypes.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail=f"Position type with ID {position_id} not found.")
    return position


@positions_router.put("/position_types/{position_id}", response_model=schemas.PositionTypeResponse)
def update_position_type(position_id: int, position_data: schemas.PositionTypeBase, db: Session = Depends(get_db)):
    position = db.query(models.PositionTypes).filter(models.PositionTypes.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail=f"Position type with ID {position_id} not found.")
    for key, value in position_data.dict().items():
        setattr(position, key, value)
    db.commit()
    db.refresh(position)
    return position


@positions_router.delete("/position_types/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_position_type(position_id: int, db: Session = Depends(get_db)):
    position = db.query(models.PositionTypes).filter(models.PositionTypes.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail=f"Position type with ID {position_id} not found.")
    db.delete(position)
    db.commit()
    return {"message": "Position type deleted successfully."}

