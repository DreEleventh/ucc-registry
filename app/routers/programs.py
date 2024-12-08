from fastapi import HTTPException, Response, Depends, status, APIRouter
from sqlalchemy.orm import Session, joinedload
from typing import List
import logging

import app.schemas as schemas, app.models as models
from app.databaseConnect import get_db

router = APIRouter(
    prefix="/programs", 
    tags=["Programs"],
)

@router.post("/add_program", status_code=status.HTTP_201_CREATED, response_model=schemas.AddDegreeProgramResponse)
async def add_degree_program(program_data: schemas.AddDegreePrograms, db: Session = Depends(get_db)):
    new_program = models.DegreePrograms(**program_data.model_dump())
    
    db.add(new_program)
    db.commit()
    db.refresh(new_program)
    
    return new_program


@router.get("/get_programs", response_model=List[schemas.DegreeProgramResponse])
async def get_all_programs(db: Session = Depends(get_db)):
    programs = db.query(models.DegreePrograms).order_by(models.DegreePrograms.id.desc()).all()
    
    programs_dict = [program.__dict__ for program in programs]
    
    return programs_dict
    
    
@router.put("/update_degree_program/{program_id}")
def update_degree_program(program_id: int, program_update: schemas.AddDegreePrograms, db: Session = Depends(get_db)):
    # Fetch the degree program by its ID
    degree_program = db.query(models.DegreePrograms).filter(models.DegreePrograms.id == program_id).first()

    if not degree_program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Degree program with ID {program_id} not found.",
        )

    # Update the degree program
    for key, value in program_update.dict(exclude_unset=True).items():
        setattr(degree_program, key, value)

    db.commit()
    db.refresh(degree_program)
    
    return degree_program


@router.delete("/delete_degree_program/{program_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_degree_program(program_id: int, db: Session = Depends(get_db)) -> None:
    # Fetch the degree program by ID
    degree_program = db.query(models.DegreePrograms).filter(models.DegreePrograms.id == program_id).first()

    if not degree_program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Degree program with ID {program_id} not found."
        )

    # Delete the program
    db.delete(degree_program)
    db.commit()


@router.get("/get_program_by_id/{program_id}", response_model=schemas.DegreeProgramResponse)
async def get_single_program(program_id: int, db: Session = Depends(get_db)): 
    
    program = db.query(models.DegreePrograms).filter(models.DegreePrograms.id == program_id).first()
    
    if program is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Degree program with ID {program_id} was not found.")
    
    return program