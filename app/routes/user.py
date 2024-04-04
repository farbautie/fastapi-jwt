from fastapi import APIRouter, Depends
from typing import Annotated

from ..schemas.user import UserInDB
from ..utils.jwt import get_current_user

router = APIRouter(prefix='/users')

@router.get('/me')
def me(
    current_user: Annotated[UserInDB, Depends(get_current_user)],
):
    del current_user.password
    return current_user