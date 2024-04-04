from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session

from ..schemas.user import UserInDB
from ..database import get_database, User
from ..utils.bcrypt import get_password_hash, verify_password
from ..utils.jwt import create_access_token, credentials_exception ,ACCESS_TOKEN_EXPIRE_MINUTES
from ..schemas.token import Token


router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/signup')
def signup(request: UserInDB, db: Annotated[Session, Depends(get_database)]):
    user = db.query(User).filter(User.username == request.username).first()
    if user: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='username already exists'
        )

    new_user = User(
        username=request.username,
        password=get_password_hash(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "status": status.HTTP_201_CREATED,
        "user": new_user
    }
    

@router.post('/signin')
def signup(
    request: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_database)]) -> Token:
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise credentials_exception

    if not verify_password(request.password, user.password):
        raise credentials_exception
    
    access_token_exp = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': user.username}, expires_data=access_token_exp)
    
    return Token(access_token=access_token, token_type='bearer')
