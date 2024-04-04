from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from typing import Annotated
from jose import jwt, JWTError

from app.database import User, get_database
from app.schemas.token import TokenData

SECRET_KEY = 'b222982bb89e09043bc487614864f45dc376f2a0611da87389c10671c8da33ef'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 5

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/signin')

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="invalid credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def create_access_token(data: dict, expires_data: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_data:
        expires = datetime.now(timezone.utc) + expires_data
    else:
        expires = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expires
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_database)]
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == token_data.username).first()
    if not user:
        raise credentials_exception
    
    return user