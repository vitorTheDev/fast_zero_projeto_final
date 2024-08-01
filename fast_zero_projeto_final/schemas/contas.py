from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContaSchema(BaseModel):
    username: str = Field(pattern=r'^[a-zA-Z][a-zA-Z0-9_]+')
    email: EmailStr
    senha: str


class ContaPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class ContaLista(BaseModel):
    contas: list[ContaPublic]
