from pydantic import BaseModel, ConfigDict, Field, EmailStr

class Username(BaseModel):
    email_address: EmailStr = Field(min_length=20, max_length=50)

class UserBase(Username):
    firstname:str = Field(min_length=1, max_length=200)
    lastname:str = Field(min_length=1, max_length=200)

class Password(Username):
    password:str = Field(min_length=8, max_length=40)
    
    
class UserCreate(UserBase, Password):
    pass

class UserUpdate(UserBase, Password):
    pass

class User(UserBase):
    id: int

class UserLogin(Username, Password):
    pass

class TokenResponse(BaseModel):
    access_token:str
    token_type:str


    