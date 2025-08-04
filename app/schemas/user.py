from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    senha: str

class UserLogin(BaseModel):
    email: EmailStr
    senha: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = {
    "from_attributes": True
}
