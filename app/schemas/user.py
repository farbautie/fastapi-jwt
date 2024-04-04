from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: Optional[int] | None = None
    username: str

class UserInDB(UserSchema):
    password: str