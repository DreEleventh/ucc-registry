import sched
from fastapi import HTTPException, Depends, status, APIRouter
from sqlalchemy.orm import Session
from typing import List

import app.schemas as schemas
import app.models as models
from app.databaseConnect import get_db
from app.utils import generate_admin_id, generate_admin_email, hash_password


admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@admin_router.post("/create_admin", status_code=status.HTTP_201_CREATED, response_model=schemas.AdminResponse)
async def create_admin(admin_data: schemas.RegisterAdmin, db: Session = Depends(get_db)):
    
    # Generate a unique admin id and email
    admin_id = generate_admin_id(db)  
    admin_email = generate_admin_email(admin_data.first_name, admin_data.last_name, db)
    
    # Extract data for the students table
    admin_dict = admin_data.model_dump(exclude={"admin_credentials"})
    new_admin = models.Admin(**admin_dict, admin_id=admin_id, admin_email=admin_email)
    db.add(new_admin)
    
    # Hash user password 
    hashed_password = hash_password(admin_data.admin_credentials.password)
    
    new_credentials = models.AdminCredentials(
            admin_id=admin_id, 
            username=admin_email,
            password=hashed_password,
        )
    db.add(new_credentials)
    
    db.commit()
    db.refresh(new_admin)
    
    return new_admin


@admin_router.get("/get_all_admins", response_model=List[schemas.AdminResponse])
async def get_all_admins(db: Session = Depends(get_db)):
    admins = db.query(models.Admin).all()
    return admins


@admin_router.get("/get_single_admin/{admin_id}", response_model=schemas.AdminResponse)
async def get_admin(admin_id: str, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.admin_id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin


# @admin_router.put("/update_admin/{admin_id}", response_model=schemas.AdminResponse)
# async def update_admin(admin_id: str, admin_data: schemas.UpdateAdmin, db: Session = Depends(get_db)):
#     admin_query = db.query(models.Admin).filter(models.Admin.admin_id == admin_id)
#     admin = admin_query.first()
    
#     if not admin:
#         raise HTTPException(status_code=404, detail="Admin not found")
    
#     admin_query.update(admin_data.model_dump(), synchronize_session=False)
    
#     update_username = models.AdminCredentials(
#             username=admin_data.admin_email,
        
#         )
#     db.update(update_username)
    
#     db.commit()
#     return admin_query.first()


@admin_router.put("/update_admin/{admin_id}", response_model=schemas.AdminResponse)
async def update_admin(admin_id: str, admin_data: schemas.UpdateAdmin, db: Session = Depends(get_db)):
    # Fetch the admin to update
    admin_query = db.query(models.Admin).filter(models.Admin.admin_id == admin_id)
    admin = admin_query.first()
    
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    # Update admin information
    admin_query.update(admin_data.model_dump(), synchronize_session=False)

    # Fetch the related credentials
    credentials_query = db.query(models.AdminCredentials).filter(models.AdminCredentials.admin_id == admin_id)
    credentials = credentials_query.first()

    if credentials:
        # Update username in AdminCredentials
        credentials_query.update({"username": admin_data.admin_email}, synchronize_session=False)
    else:
        # Create new credentials if not found
        new_credentials = models.AdminCredentials(
            admin_id=admin_id,
            username=admin_data.admin_email,
            password=hash_password("DefaultPassword"),  # Set a default hashed password
        )
        db.add(new_credentials)

    db.commit()

    # Return the updated admin
    return admin_query.first()
