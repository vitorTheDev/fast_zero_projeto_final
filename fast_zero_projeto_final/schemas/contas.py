from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContaSchema(BaseModel):
    username: str = Field(pattern=r'^[a-zA-Z][a-zA-Z0-9_]+', max_length=40)
    email: EmailStr = Field(max_length=320)
    senha: str = Field(max_length=255)


class ContaPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)
