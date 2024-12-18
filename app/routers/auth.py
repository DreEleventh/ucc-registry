from datetime import datetime

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import app.schemas as schemas
import app.models as models
import app.oauth2 as oauth2
import app.utils as utils
from app.databaseConnect import get_db


router = APIRouter(
    tags=["Authentication"]
)


@router.post("/admin_login", response_model=schemas.Token)
def admin_login(admin_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Handle donor login and token generation.

    Args:
        admin_credentials (schemas.DonorLogin): The donor's login credentials.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary containing the access token and its type.

    Raises:
        HTTPException: If the credentials are invalid.
    """
    admin = db.query(models.AdminCredentials).filter(models.AdminCredentials.username
                                                     == admin_credentials.username).first()

    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    if not utils.verify_passcode(admin_credentials.password, admin.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    # Update last_login_time
    admin.last_login_time = datetime.now()
    db.commit()

    access_token = oauth2.create_access_token(payload={"admin_id": admin.admin_id})
    return {"access_token": access_token, "token_type": "bearer"}
