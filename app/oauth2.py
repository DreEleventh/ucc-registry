import jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import app.schemas as schemas
import app.models as models

from app import databaseConnect


oauth2_scheme =  OAuth2PasswordBearer(tokenUrl='admin_login')

# Constants for JWT
SECRET_KEY = "jksownkdnaunrpahfuyenclaybpnwbqa4hei2098453erfgswknifbsxawqin6thfveomcswlxawsbbuy"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20

def create_access_token(payload: dict):
    """
    Create a JWT access token.

    Args:
        payload (dict): The payload data to include in the token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = payload.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token


def verify_access_token(token: str, credentials_exception):
    """
    Verify the JWT access token.

    Args:
        token (str): The JWT token to verify.
        credentials_exception (HTTPException): The exception to raise if the token is invalid.

    Returns:
        TokenData: The decoded token data.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        admin_id: int = payload.get("admin_id")

        if admin_id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=admin_id)
    except jwt.ExpiredSignatureError:
        raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(databaseConnect.get_db)):
    """
    Retrieve the current user based on the JWT token.

    Args:
        token (str): The JWT token provided in the request.
        db (Session): The database session.

    Returns:
        Admin: The admin object corresponding to the token.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        access_token = verify_access_token(token, credentials_exception)
    except HTTPException as e:
        print(f"Token verification failed: {e.detail}")
        raise

    admin = db.query(models.Admin).filter(models.Admin.admin_id == access_token.id).first()

    # print(access_token.donor_id)
    # print(donor.donor_id)
    if admin is None:
        print("Admin not found")
        raise credentials_exception

    return admin 
