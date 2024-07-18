from sqlmodel import Field, SQLModel
from pydantic import EmailStr, BaseModel


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=255)
    identity: str

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)
    identity: str = Field(default="內部使用者")

class UserPublic(UserBase):
    id: int

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

class Email(BaseModel):
    email: EmailStr


class UserLoginForm(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=40)