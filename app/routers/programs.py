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

